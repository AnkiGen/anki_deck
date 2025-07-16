<script> 
import BaseButton from '@/components/Basebutton.vue';
import router from '@/router';
import { useUserTextStoreV } from '@/stores/userTextV';
import { useUserTextStore } from '@/stores/userText';


export default {
    data() {
        return {
            pickedWords: new Array(),
            userText: '',
            isDone: true,
            valid: true,
            store: null,
            validatedText: '',
        }
    },
    mounted() {
        // this.fatchdata();
        //this variable represents store, you can use all its actions as methods
        this.textStoreV = useUserTextStoreV();
        this.textStore = useUserTextStore();
    },
    components: {
        BaseButton
    },
    methods: {
    //this function is not need and should be deleted later
    //when all features on this page will be finished
        async fatchdata() {
            this.pickWords();            
            const resp = { // add
                unknown_words: ["give","survive","climb"],
                known_words:["dog","cat","emansipation","Russia"],
                count:6,
                context_sentences: ["I will never give up", "He will survive", "This mount is too high to climb"],
            };
            const response = await fetch("http://127.0.0.1:8000/wordlist/post", {
                method: "POST",
                headers: {
                    'Content-Type' : 'application/json'
                },
                body: JSON.stringify(resp),
            })
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.setAttribute("download", "Anki_deck.csv");
            document.body.appendChild(a);
            a.click();
            a.remove();
        },
        pickWords() {
            this.pickedWords = [];
            let words = this.userText.split(" ");
            let length = words.length;
            for (let i = 0; i < 10; i++) {
                this.pickedWords.push(words[Math.floor(Math.random() * length)])
            }
        },
        goToFilterText() {
            //using Store variable to set user text
            router.push({name: "Filter"});
        },
        showProccessingTitle() {
            let div = document.createElement('div');
            div.innerHTML = "Proccessing...";
        },
        goToFilter() {
            const regex = /[a-zA-Z'`’-]+/;
            const endSentenctRegexp = /[!?\.]+/;
            let sentenceIndex = 0;
            let prevWord = "";
            let words = this.userText.split(/(\s+|\n)/)
                                        .map((word) => {
                                            let currentIndex = sentenceIndex;
                                            let endOfSentance = endSentenctRegexp.exec(word);
                                            if (endOfSentance != null) {
                                                sentenceIndex++;
                                            }
                                            if (word == "\n" && endSentenctRegexp.exec(prevWord) == null) {
                                                sentenceIndex++;
                                            }
                                            let newWord = regex.exec(word);
                                            prevWord = word
                                            if (newWord != null) {
                                                return {
                                                    word: newWord[0],
                                                    sentenceIndex: currentIndex,
                                                    class: "default"
                                                    }
                                            } else {
                                                return {word: ''};
                                            }
                                        })
                                        .filter((word) =>  word.word.length > 2);
            words = this.toSet(words);
            const wordCount = words.length;
            let sentences = this.userText.split(/[\.!?\n]+/)
                                    .filter((sentance) => sentance.length > 0)
                                    .map((sentance) => {
                                    return sentance.trim();
                                    });
                            

            if (wordCount < 5) {
                alert('Пожалуйста, введите как минимум 5 слов.');
                return;
            }
            
            if (wordCount > 500) {
                alert('Пожалуйста, введите не более 500 слов.');
                return;
            }
            else {
                this.textStoreV.setText(words);
                this.textStore.setText(this.userText);
                this.textStoreV.setContext(sentences);
                router.push({name: "Filter"})
            }
        },
        goBack() {
            router.push({name: "Welcom"})
        },
        toSet(array) {
            let map = new Map()
            let newArr = [];
            for (let word of array) {
                if (map.has(word.word))
                    continue;
                newArr.push(word);
                map.set(word.word, 0);
            }
            return newArr;
        }
    },
    watch: {
        isDone(newIsDone) {

        }
    }
}
</script>

<template>
   <main>
    <header>
        <h2 @click="goBack"><-- Вернуться назад</h2>
    </header>
        <div class = "header">Введите текст песни или книги</div>
        <div class = "form-container">
            <form>
                <textarea id = "text" v-model="userText" placeholder="Например:
To be, or not to be, that is the question. 
Whether..."></textarea>
            </form>
        </div>
        <!-- <BaseButton class = "submit" @click="fatchdata()">Сгенерировать деку</BaseButton> -->
        <BaseButton :onClick="goToFilter" class = "submit">Перейти к генерации деки</BaseButton>
   </main>
</template>

<style scoped> 

    main {
        margin: 0 px;
        font-family: "Inter", sans-serif;
        font-optical-sizing: auto;
        font-weight: 300;
        font-style: normal;
        color: white;
        font-size: 17px;
    }
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
    .form-container {
        align-self: center;
        width: 600px;
        margin: 0 auto;
        margin-top:20px;
    }
    #text {
        background-color: transparent;
        border-radius: 10px;
        padding-top:0.5em;
        height: 150px;
        border: 2px solid whitesmoke;
        width: 100%;
        color: white;
        box-sizing: border-box;
        padding-left: 0.5em;
        font-size: 14px;
        resize: vertical;
        scrollbar-width: thin;
        scrollbar-color: #888 var(--color-background);
        font-size: 15px;
    }
    #text::placeholder {
        text-align: left;
        color: white;
        opacity: 0.8;
        font-size: 15px;
    }
    #text:focus {
        outline: none;
        box-shadow: none;
    }
    .submit {
        align-self: center;
        width: 255px;
        height: 60px;
        border-radius: 0;

        margin: 0 auto; 
        margin-top: 35px;
        
    }
    
</style>