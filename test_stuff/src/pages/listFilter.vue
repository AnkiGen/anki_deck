<script>
import Basebutton from '@/components/Basebutton.vue';
import { useAPIStore } from '@/stores/API';
import { useUserTextStore } from '@/stores/userText';
import { useUserTextStoreV } from '@/stores/userTextV';
import { nextTick } from 'vue';
import router from '@/router';
import {shuffle} from '@/scripts/shuffle'

export default {
    data() {    
        return {
            isVisible: false,
            cardNumStart: 1,
            cardNumTotal: useUserTextStoreV.unknown,
            counter: 0,
            wordList: [],
            scrollerWidth: 0,
            cardWidth: 0,
            gap: 0,
            currentPage: 0,
            maxPage: 0,
            direction: null, // 0 - next page for translation, 1 - previous page for translation
            resp: {
                unknown_words: [],
                known_words: [],
                count: useUserTextStoreV().count,
                context_sentences: []
            },
        }
    },
    components: {
        Basebutton
    },
    methods: {
        translate() {
            let distance = (this.cardWidth+this.gap)*4;
            switch (this.direction) {
                case 0:
                    this.$refs.scroller.style.transform = `translateX(-${(this.currentPage)*distance}px)`;
                    break;
                case 1:
                    this.$refs.scroller.style.transform = `translateX(-${(this.currentPage-1)*distance}px)`;
                    break;
                
            }
        },
        moveForward(){
            this.direction = 0;
            if (this.currentPage < this.maxPage-1){
                this.currentPage++;
                this.translate();
            }
        },
        moveBack(){
            this.direction = 1;
            if (this.currentPage > 0){
                this.translate();
                this.currentPage--;
            }
        },
        updateSizes(){
            if (!this.$refs.card[0] || !this.$refs.scroller || this.$refs.card[0].length === 0)
                return;
            this.gap = parseFloat(window.getComputedStyle(this.$refs.scroller).gap);
            this.cardWidth = this.$refs.card[0].offsetWidth;
            this.scrollerWidth = this.$refs.scroller.offsetWidth;
            let cardNum = this.wordList.length;
            // this.maxPage = Math.floor((this.cardWidth*cardNum+(cardNum-1)*this.gap) / ((this.cardWidth+this.gap)*4))
            this.maxPage = Math.ceil(this.wordList.length/4)
            
        },
        changeClass(index){
            let classes = ["wantLearn", "dontWantLearn", "default"];
            let word = this.wordList[index];
            let classNum = classes.indexOf(word.class);
            let nextClass = classes[(classNum+1)%3];
            word.class = nextClass;
        },
        validateWords() {
            this.wordList = useUserTextStoreV().words;
            this.wordList = shuffle(this.wordList);
            // this.wordList.forEach(element => {
            //     console.log(element)
            // });
            let sentenceIndex = 0;
            // this.wordList = wordArr.map((word) => {
            //     let currentIndex = sentenceIndex;
            //     let regex = /[a-zA-Z'`’-]+/;
            //     let newWord = regex.exec(word);
            //     if (newWord != null) {
            //         return {
            //         word: newWord[0],
            //         class: "default"
            //         }
            //     }else {
            //         return {
            //             word: "BAD WORD",
            //             class: ""
            //         }
            //     }
            // })
        },
        handleKeyDown(event){
            if (event.key === "ArrowRight") {
            this.moveForward();
            } else if (event.key === "ArrowLeft") {
            this.moveBack();
            }
        },
        startGen() {
            let contextSentences = useUserTextStoreV().context;
            for (let word of this.wordList) {
                switch (word.class) {
                    case "wantLearn":
                        this.resp.unknown_words.push(word.word);
                        this.resp.context_sentences.push(contextSentences[word.sentenceIndex]);
                        break;
                    case "dontWantLearn":
                        this.resp.known_words.push(word.word);
                        break;
                }
            }
            
            // Store data in API store like tinder.vue
            const apiStore = useAPIStore();
            apiStore.setState(this.resp);
            
            // Redirect to review page instead of final page
            router.push({name: "Review"});
        },
    },
    mounted() {
        this.validateWords();
        this.$nextTick(() => this.updateSizes());
        window.addEventListener("resize", this.updateSizes);
        window.addEventListener("keydown", this.handleKeyDown)
    },
    unmounted(){
        window.removeEventListener('resize', this.updateSizes);
        window.removeEventListener('keydown', this.handleKeyDown);
    },
}
</script>

<template>
    <div class="main-container">
        <h1>Выбор слов из текста
            <span class="question-mark" @mouseover="isVisible=true" @mouseout="isVisible=false">?
                <span v-if="isVisible" class="user-hint">Кликни по карточке со словом, чтобы задать ей статус:<br><span style="background-color: #71c686;">Зеленые карточки:</span>
                неизвестные слова, которые ты хочешь учить<br>
                <span style="background-color: #B74747;">Красные карточки:</span> слова, которые ты не хочешь учить</span>
            </span>
        </h1>
        <div class="nested-container">
            <!-- <span class="card-number">Слова {{cardNumStart}}-{{cardNumStart+4}} из {{cardNumTotal}}</span> -->
            <div class="card-container">
                <div class="scroller" ref="scroller">
                    <div ref="card"
                        @click="changeClass(index)" 
                        v-for="word, index in wordList" 
                        :key="index" 
                        :class="['card', word.class]">
                        {{word.word.toLowerCase()}}
                    </div>
                </div>
            </div>
            <div class="bottom-contaiter">
                <!-- <span class="card-picked">Выбрано слов {{counter}} из {{cardNumTotal}}</span> -->
                <div class="router-buttons-container">
                    <Basebutton class="router-button" @click="moveBack"> Прокрутка назад</Basebutton>
                    <Basebutton class="router-button" @click="moveForward">Прокрутка вперед</Basebutton>
                </div>
            </div>
            <div class="generation-container">
                <Basebutton class="start-generation" @click="startGen"> Начать генерацию </Basebutton> 
            </div>
        </div>
    </div>
</template>

<style scoped>
    .main-container{
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 100%;
    }
    h1{
        flex: 0 0 auto;
        font-size: 30px;
        position: relative;
        font-weight: 400;
        font-size: 40px;
    }
    .question-mark{
        border: #888 solid;
        border-radius: 24px;
        display: inline-block;
        width: 28px;
        height: 28px;
        text-align: center;
        position: absolute;
        top: 5px;
        right: -42px;
        font-size: 22px;
    }
    .user-hint{
        content: attr(data-text);
        min-width: 420px;
        z-index: 1;
        background-color: var(--color-background);
        position: absolute;
        border-radius: 10px;
        border: white solid;
        border-width: 1px;
        top: 35px;
        font-size: 18px;
        font-weight: 400;
        left: 30px;
    }
    .nested-container{
        display: flex;
        align-content: start;
        flex-direction: column;
        width: 932px;
    }
    .card-container{
        display: flex;
        width:932px;
        flex: 0 0 auto;
        overflow: hidden;
        /* transition: ; */

    }
    .card-number{
        font-size: 20px;
    }
    .card{
        height: 260px;
        width: 214px;
        box-sizing: border-box;
        border-radius: 28px;
        border: 2px solid #fff;
        font-size: 40px;
        flex-shrink: 0;
    }
    .scroller{
        display: flex;
        gap: 25px;
        flex-wrap:nowrap;
        width: 100%;
        transition: transform 0.5s cubic-bezier(0.255, 0.765, 0.575, 0.925);

    }
    .wantLearn{
        border-color: #71c686;
    }
    .dontWantLearn{
        border-color: #B74747;
    }
    .default{
        border-color: inherit;
    }
    .router-buttons-container{
        display: flex;   
        padding-top: 30px;
        justify-content: space-around;
    }
    .card-picked{
        flex-shrink: 0;
    }
    .router-button{
        width: 240px;
        height: auto;
    }
    .start-generation{
        width: 280px;
        height: auto; 
    }
    .generation-container{
        display: flex;
        justify-content: center;
        padding-top: 40px;
    }

</style>