<script> 
import BaseButton from '@/components/Basebutton.vue';
import router from '@/router';
import { useUserTextStoreV } from '@/stores/userTextV';
import { useUserTextStore } from '@/stores/userText';


export default {
    data() {
        return {
            maxword: 90,
            lenword: 90,
            choice: 0 // 0 - tinder, 1 - manually, 2 - word list
        }
    },
    mounted() { 
            const sliders = this.$el.querySelectorAll('.slider');
            sliders.forEach(slider => {
                const min = Number(slider.min);
                const max = Number(slider.max);
                const percent = ((slider.value - min) / (max - min)) * 100;
                slider.style.background = `linear-gradient(to right, #34c759 ${percent}%, #fff ${percent}%)`;
            });
            this.textStoreV = useUserTextStoreV();
    },
    components: {
        BaseButton
    },
    methods: {
        progressScript(event) {
            const sliderEl = event.target;
            const min = Number(sliderEl.min);
            const max = Number(sliderEl.max);
            const percent = ((sliderEl.value - min) / (max - min)) * 100;
            sliderEl.style.background = `linear-gradient(to right, #34c759 ${percent}%, #fff ${percent}%)`;
        },
        goBack() {
            router.push({name: 'Input'});
        },
        redirect(event) {
            // event.preventDefault();
            const names = ["Tinder", "FilterFromText", "List"];
            this.textStoreV.setUnknown(this.lenword);
            this.textStoreV.setCount(this.maxword);
            router.push({ name: names[this.choice] });
        }
    },
    watch: {
    }
}
</script>

<template>
   <main>
    <header>
        <h2 @click="goBack"><-- Вернуться назад</h2>
    </header>
        <div class = "header">Параметры генерации</div>
        <form class = "filter-container">
            <div class = "max-words">
                <h2 id = "header">Количество слов для изучения</h2>
                <div class = "slider-container">
                    <input type="range" min = "1" max = "180" v-model = "maxword" value = "90" class = "slider" @input="progressScript">
                    <div class = "number-list">
                        <div class = "col">
                            1
                        </div>
                        <div class = "col">
                            {{ maxword }}
                        </div>
                        <div class = "col">
                            180
                        </div>
                    </div>
                </div>
            </div>
            <div class = "max-words">
                <h2 id = "header">Кол-во символов в сгенерированном предложении</h2>
                <div class = "slider-container">
                    <input type="range" min = "5" max = "180" v-model = "lenword" value = "90" class = "slider" @input="progressScript">
                    <div class = "number-list">
                        <div class = "col">
                            5
                        </div>
                        <div class = "col">
                            {{ lenword }}
                        </div>
                        <div class = "col">
                            180
                        </div>
                    </div>
                </div>
            </div>
            <div class = "choose">
                <h2 id = "header">Кол-во незнакомых слов</h2>
                <div class = "radio-container">
                    <label class="check" for="choice0">
                        <input type="radio" id="choice0" name="choice" value="0" v-model="choice">
                        <span class="radio-label">Тиндер</span>
                    </label>
                    <label class="check" for="choice1">
                        <input type="radio" id="choice1" name="choice" value="1" v-model="choice">
                        <span class="radio-label">Вручную</span>
                    </label>
                    <label class="check" for="choice2">
                        <input type="radio" id="choice2" name="choice" value="2" v-model="choice">
                        <span class="radio-label">Список</span>
                    </label>
                </div>
            </div>
        </form>
        <BaseButton class = "submit" @click="redirect">Перейти к выборке слов</BaseButton>
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
    .filter-container h2 {
        font-size: 20px;
        font-weight: 400;
    }
    .slider-container input {
        width: 100%;
    }
    .filter-container {
        margin: 0 auto;
        width: 50%;
        text-align: center;
        align-items: center;
    }
    .slider {
        -webkit-appearance: none;
        background-color: whitesmoke;
        border-radius: 25px;
        height: 18px;

    }
    .slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width:7px;
        height: 32px;
        background-color: #34c759;        
        border-radius: 20px;

    }
    .slider::-moz-range-thumb {
        transition: .2s ease-in-out;
    }
    .slider::webkit-slider-thumb:hover { 
        box-shadow: 0 0 0 10px #34c75928
    }
    .slider:active::webkit-slider-thumb { 
        box-shadow: 0 0 0 13px #34c7593d
    }
    .slider:hover::webkit-slider-thumb { 
        box-shadow: 0 0 0 13px #34c7593d
    }
    .number-list{
        margin-top:10px;
        display: flex;
        width: 100%;
        justify-content: space-between;
        align-items: center;
    }
    .number-list:nth-child(2){
        padding-left:10px;
    }
    .radio-container {
        display: flex;
        gap: 2em;
        align-items: center;
        width: 100%;
        justify-content: center;
    }
    .check {
        display: flex;
        justify-content:left;
        align-items: center;
        gap: 1em;
        cursor: pointer;
        transition: background 0.2s;   
    }
    .check input {
        appearance: none;
        width: 16px;
        height: 16px;
        border: 2px solid #fff;
        border-radius: 50%;
    }
    .check input:checked {
        background-color: #34c759;
        border: 2px solid #34c759;
    }
    .check span {
        width: auto;
    }
    .radio-label {
        margin-left: 0.5em;
        width: auto;
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
    .submit {
        margin: 0 auto;
        margin-top: 3em;
        width: 255px;
        height: 60px;   
        border-radius: 0px;
        padding: 0;
    }
</style>