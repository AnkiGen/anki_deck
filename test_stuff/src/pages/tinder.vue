<script> 
import BaseButton from '@/components/Basebutton.vue';
import router from '@/router';
import {shuffle} from '@/scripts/shuffle'
import { useAPIStore } from '@/stores/API';
import { useUserTextStoreV } from '@/stores/userTextV';

export default {
    data() {
        return {
            countleft: 0,
            countadded: 0,
            words: [],
            currentIndex: 0,
            currentWord: '',
            resp: {
                unknown_words: [],
                known_words: [],
                count: 0,
                context_sentences: []
            },
            skips: 0,
        }
    },
    computed: {
        store() {
            return useUserTextStoreV();
        }
    },
    mounted() { 
        this.initializeGame();
    },
    components: {
        BaseButton
    },
    methods: {
        initializeGame() {
            this.words = this.store.words;
            shuffle(this.words);
            this.countleft = this.words.length;
            this.countadded = 0;
            this.currentIndex = 0;
            this.updateCurrentWord();
        },
        updateCurrentWord() {
            if (this.currentIndex < this.words.length) {
                this.currentWord = this.words[this.currentIndex].word;
            } else {
                this.currentWord = '';
            }
        },
        likeWord() {
            let contextSentences = useUserTextStoreV().context;
            if (this.currentIndex < this.words.length) {
                this.resp.unknown_words.push(this.currentWord);
                this.resp.context_sentences.push(contextSentences[this.words[this.currentIndex].sentenceIndex]);
                this.countadded++;
                this.nextWord();
            }
        },
        dislikeWord() {
            if (this.currentIndex < this.words.length) {
                this.resp.known_words.push(this.currentWord);
                this.nextWord();
            }
        },
        starWord() {
            if (this.currentIndex < this.words.length) {
                // Add skipped words to known_words as well
                this.resp.known_words.push(this.currentWord);
                this.skips++;
                this.nextWord();
            }
        },
        nextWord() {
            this.currentIndex++;
            this.countleft = this.words.length - this.currentIndex;
            this.updateCurrentWord();
            if (this.currentIndex >= this.words.length) {
                this.finishGame();
            }
        },
        goBack() {
            if (this.currentIndex > 0) {
                this.currentIndex--;
                this.countleft = this.words.length - this.currentIndex;
                // Remove from the correct list if going back
                const prevWord = this.words[this.currentIndex].word;
                if (this.resp.unknown_words.length > 0 && this.resp.unknown_words[this.resp.unknown_words.length - 1] === prevWord) {
                    this.resp.unknown_words.pop();
                    this.countadded--;
                } else if (this.resp.known_words.length > 0 && this.resp.known_words[this.resp.known_words.length - 1] === prevWord) {
                    this.resp.known_words.pop();
                }
                this.updateCurrentWord();
            } else {
                router.push({name: 'Filter'});
            }
        },
        finishGame() {
            // Save lists to store explicitly (in case of reactivity issues)
            this.store.setYes(this.resp.unknown_words);
            this.store.setNo(this.resp.known_words);
            this.store.setKnown(this.resp.known_words);
        },
        redirect() {
            // Store all words in the API store
            const apiStore = useAPIStore();
            this.resp.count = 10;
            apiStore.setState(this.resp);
            router.push({name: 'Review'});
        },
        goFilter() {
            router.push({name: "Filter"})
        }
    },
    watch: {
    }
}
</script>

<template>
   <main>
    <header>
        <h2 @click="goFilter"><-- Вернуться к фильтрам</h2>
    </header>
        <div class = "header">Тиндер слов</div>
        <div class = "card-container">
            <div class = "goBack" @click="goBack">
                Вернуться к предыдущему слову
            </div>
            <div class = "card" v-if="currentWord">
                <button class="star-btn" @click="starWord"><img class="corner-img" src="/star.png" alt="star"></button>
                <div class="word">{{ currentWord.toLowerCase() }}</div>
                <div class = "button-container">
                    <button class = "like left" @click="dislikeWord"><img src="/dislike.png" alt="dislike"></button>
                    <button class = "like right" @click="likeWord"><img src="/like.png" alt="like"></button>
                </div>
            </div>
            <div class="game-finished" v-else>
                <h2>Все слова обработаны!</h2>
                <p>Слов добавлено в деку: {{ resp.unknown_words.length }}</p>
                <p>Слов пропущено: {{ skips }}</p>
            </div>
            <div v-if ="currentWord">
              <h2>Слов осталось: {{ countleft }}</h2>
            <h2>Слов добавлено в деку: {{ countadded }}</h2>  
            </div>
            <div v-else>
                <BaseButton class = "submit" @click="redirect">Начать генерацию</BaseButton>
            </div>
        </div>
   </main>
</template>

<style scoped> 
    header h2 {
        font-size: 15px;
        font-weight: 100;
    }
    header h2:hover {
        cursor: pointer;
        text-decoration: underline;
        text-decoration-color: #fff;
        text-underline-offset: 4px;
    }
    main {
        margin: 0 px;
        font-family: "Roboto", sans-serif;
        font-optical-sizing: auto;
        font-weight: 300;
        font-style: normal;
        color: white;
        font-size: 17px;
    }
    header {
        font-family: "Inter", sans-serif;

    }
    .header {
        font-family: "Roboto", sans-serif;
        font-optical-sizing: auto;
        font-weight: 400;
        font-style: normal;
        font-variation-settings:      
        "wdth" 100;
        text-align: center;
        font-size: 32px;
    }
    .card-container {
        margin: 0 auto;
        width: 570px;
        margin-top: 88px;
    }
    .goBack {
        padding-left: 15px;
        font-size: 15px;
    }
    .goBack:hover {
        cursor: pointer;
        text-decoration:underline;
        text-decoration-color: #fff;
        text-underline-offset: 3px;
    }
    
    .card {
        width:100%;
        height: 230px;
        border: 2px solid white;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    .word {
        flex: 1 1 auto;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        font-family: "Roboto", sans-serif;
        font-size: 60px;
        font-weight: 350;
    }
    .button-container {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        display: flex;
        justify-content: space-between;
        padding: 0 20px 20px 20px;
        box-sizing: border-box;
    }
    .like.left {
        align-self: flex-end;
    }
    .like.right {
        align-self: flex-end;
    }
    .like {
        background-color: transparent;
        border: 0px;
    }
    .corner-img {
        position: absolute;
        top: 15px;
        right: 25px;
    }
    .card-container h2{
        text-align: center;
        font-size: 20px;
        font-weight: 350;
    }
    .card-container h2{
        text-align: center;
        font-size: 20px;
        font-weight: 350;
    }
    .game-finished {
        width: 100%;
        height: 230px;
        border: 2px solid white;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .game-finished h2 {
        font-size: 28px;
        margin-bottom: 20px;
        font-weight: 400;
    }
    .game-finished p {
        font-size: 18px;
        margin: 5px 0;
        opacity: 0.9;
    }
    .submit {
        margin: 0 auto;
        margin-top: 3em;
        width: 255px;
        height: 60px;   
        border-radius: 0px;
        padding: 0;
    }
    .star-btn {
        background: transparent;
        border: none;
        position: absolute;
        top: 15px;
        right: 25px;
        padding: 0;
        cursor: pointer;
        z-index: 2;
    }
</style>