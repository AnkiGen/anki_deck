<script>
import Basebutton from '@/components/Basebutton.vue';
import arrowSVG from '@/components/icons/buttonArrowFinalPage.vue';
import { useAPIStore } from '@/stores/API';
import { useUserTextStoreV } from '@/stores/userTextV';
export default {
    components: {
        Basebutton,
        arrowSVG
    },
    data() {
        return {
            resp: null,
            isGetResp: false,
            isErr: false,
            button: null,
            url: null,
            csvData: null
        }
    },
    mounted() {
        this.resp = useAPIStore().data;
        this.button = this.$refs.buttonRef;
        
        // Get CSV data from userTextV store
        const userTextStore = useUserTextStoreV();
        this.csvData = userTextStore.csvData;
        
        // If we have CSV data, create download URL
        if (this.csvData && this.csvData.length > 0) {
            this.createDownloadUrl();
            this.isGetResp = true;
        } else {
            this.isErr = true;
        }
    },
    methods: {
        createDownloadUrl() {
            try {
                // Convert CSV data to CSV string
                const csvContent = this.csvData.map(row => row.join(';')).join('\n');
                
                // Create blob and URL
                const blob = new Blob([csvContent], { type: 'text/csv' });
                this.url = window.URL.createObjectURL(blob);
            } catch (err) {
                this.isErr = true;
                console.log(err);
            }
        },
        downloadFile() {
            const a = document.createElement('a');
            a.href = this.url;
            a.download = "Anki_deck.csv";
            a.style.display = "none";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    }
}
</script>
<template>
    <div class="main-container">
        <h1 v-if="!isGetResp">Происходит генерация вашей колоды</h1>
        <h1 v-else>Ваша колода готова</h1>
        <div class="button-flex">
            <Basebutton  v-if="isGetResp" class="button-csv" @click="downloadFile()">
                <div class="inner-button-flex">
                    <arrowSVG class="arrow-icon"/>
                    <span>Скачать в формате .csv</span>
                </div>
            </Basebutton>
            <div v-else style="font-size: 50px;">Генерация...</div>
        </div>
        <div v-if="isErr">Упс, кажется что-то пошло не так</div>
        <Basebutton ref="buttonRef" class="back-button">Вернуться в начало</Basebutton>
    </div>
</template>

<style scoped>
    .main-container {
        display: flex;
        align-items: center;
        flex-direction: column;
        height: 100%;
        gap: 5%;
    }
    .button-flex {
        height: 70%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        width: 100%;

        /* background-color: aqua; */
    }
    .button-csv {
        width: 30%;
        border-radius: 70px;
        border-color: var(--color-green);
    }
    .inner-button-flex {
        display: flex;
        align-items: center;
        justify-content: space-evenly;
        width: 100%;
        font-size: 2vw;
    }
    .back-button {
        margin-bottom: 3%;
        width: 17%;
        border-radius: 0%;
    }
    @media(min-width: 1280px) {
        h1 {
            font-size: 40px;
        }
    }
    .arrow-icon {
        width: 8%;
    }
</style>


