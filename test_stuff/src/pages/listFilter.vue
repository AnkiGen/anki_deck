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
            contextSentences: null,
            expandedSentences: [],
        }
    },
    components: {
        Basebutton
    },
    methods: {
        changeClass(index){
            let classes = ["wantLearn", "dontWantLearn", "default"];
            let word = this.wordList[index];
            let classNum = classes.indexOf(word.class);
            let nextClass = classes[(classNum+1)%3];
            word.class = nextClass;
        },
        toggleSentence(index) {
            if (this.expandedSentences.length === 0) {
                this.expandedSentences = new Array(this.wordList.length).fill(false);
            }

            this.expandedSentences[index] = !this.expandedSentences[index];
            this.expandedSentences = [...this.expandedSentences]; 
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
        this.contextSentences = useUserTextStoreV().context;
        // this.$nextTick(() => this.updateSizes());
        window.addEventListener("keydown", this.handleKeyDown)
        this.expandedSentences = new Array(this.wordList.length).fill(false);
    },
    unmounted(){
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
    </div> 
    <div class="table-container">
        <table class="word-table">
            <colgroup>
                <col>
                <col style="min-width: 400px">
            </colgroup>
            <thead>
                <tr>
                    <th>Слово</th>
                    <th>Предложение из текста</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="word, index in wordList" :key="index">
                    <td>
                        <div class="ceil">{{ word.word.toLowerCase() }}</div>
                    </td>
                    <td>
                        <div 
                            class="ceil sentence-cell" 
                            :class="!expandedSentences[index] ? 'collapsed' : ''"
                            @click="toggleSentence(index)"
                        >
                            {{ contextSentences[word.sentenceIndex] }}
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    
</template>

<style scoped>
    .main-container{
        display: flex;
        flex-direction: column;
        align-items: center;
        /* height: 100%; */
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
    .word-table {
        /* width: 70%; */
        table-layout: fixed;
        border-collapse: collapse;
        margin: 30px 0;
        background: rgba(255,255,255,0.05);
        color: white;
        font-size: 32px;
    }
    .word-table th {
        background: rgba(255,255,255,0.15);
        font-weight: 500;
    }
    .word-table tr:nth-child(even) {
        background: rgba(255,255,255,0.07);
    }
    .ceil {
        /* width: 100%; */
        background: rgba(255,255,255,0.1);
        color: #fff;
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 25px;
        box-sizing: border-box;
    }
    .word-table th, .word-table td {
        border: 1px solid #fff;
        padding: 8px 12px;
        text-align: center;
        width: 200px;
    }
    .sentence-cell {
        cursor: pointer;
        transition: all 0.3s ease;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .sentence-cell.collapsed {
        max-width: 400px;
    }
    
    .sentence-cell:not(.collapsed) {
        max-height: none;
        white-space: normal;
        width: 430px;
    }
    .table-container {
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>