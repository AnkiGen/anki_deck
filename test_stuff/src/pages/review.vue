<script> 
import BaseButton from '@/components/Basebutton.vue';
import router from '@/router';

import { useUserTextStore } from '@/stores/userText';
import { useUserTextStoreV } from '@/stores/userTextV';
import { useAPIStore } from '@/stores/API';

export default {
    data() {
        return {
            pickedWords: new Array(),
            userText: '',
            isDone: true,
            valid: true,
            store: null,
            validatedText: '',
            textStore: null,
            words: [], // Will be populated from API response
            currentPage: 1,
            pageSize: 20,
            copySuccess: false,
            markedForRegeneration: new Set(), // Set to track marked sentences
            isLoading: false, // Loading state for animations
        }
    },
    mounted() { 
        //this variable represents store, you can use all its actions as methods
        this.textStore = useUserTextStore();
        this.apiStore = useAPIStore();
        this.userTextStoreV = useUserTextStoreV();
        
        // Fetch initial data from API
        this.fetchWordList();
    },
    components: {
        BaseButton
    },
    computed: {
        paginatedWords() {
            const start = (this.currentPage - 1) * this.pageSize;
            return this.words.slice(start, start + this.pageSize);
        },
        totalPages() {
            return Math.ceil(this.words.length / this.pageSize);
        }
    },
    methods: {
        goToFilterText() {
            //using Store variable to set user text
            router.push({name: "Filter"});
        },
        goToFilter() {
            // Store the final words in userTextV store
            this.userTextStoreV.setCsv(this.words);
            router.push({name: "FinalPage"})
        },
        goBack() {
            this.textStore.startAgain();
            router.push({name: "Tinder"})
        },
        nextPage() {
            if (this.currentPage < this.totalPages) this.currentPage++;
        },
        prevPage() {
            if (this.currentPage > 1) this.currentPage--;
        },
        goToPage(page) {
            if (page >= 1 && page <= this.totalPages) this.currentPage = page;
        },
        copyWordsToCSV() {
            const csv = this.words.map(row => row.join(';')).join('\n');
            navigator.clipboard.writeText(csv).then(() => {
                this.copySuccess = true;
                setTimeout(() => { this.copySuccess = false; }, 1500);
            });
        },
        async fetchWordList() {
            try {
                this.isLoading = true;
                const apiData = this.apiStore.data;
                console.log('start')
                const response = await fetch("http://127.0.0.1:8000/wordlist/post", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(apiData),
                });
                console.log('end')
                if (response.ok) {
                    console.log('ok')
                    const blob = await response.blob();
                    const csvText = await blob.text();
                    this.parseCSVToWords(csvText);
                } else {
                    alert('Ошибка при получении списка слов');
                }
            } catch (error) {
                console.error('Error fetching word list:', error);
                alert('Ошибка при получении списка слов');
            } finally {
                this.isLoading = false;
            }
        },
        parseCSVToWords(csvText) {
            console.log(csvText)
            const lines = csvText.split('\n');
            this.words = [];
            
            // Skip the first row (header) and start from index 1
            for (let i = 1; i < lines.length; i++) {
                const line = lines[i];
                if (line.trim()) {
                    const columns = line.split(';');
                    console.log(`Row ${i}:`, columns);
                    console.log(`Columns length: ${columns.length}`);
                    
                    if (columns.length >= 5) {
                        this.words.push([
                            columns[1] || '', // Original word (skip index column)
                            columns[2] || '', // Lemma version
                            columns[3] || '', // Original sentence
                            columns[4] || '', // Russian translation
                            columns[5] || '', // Generated sentence
                            columns[6] || ''  // Generated sentence in Russian (might be empty)
                        ]);
                    }
                }
            }
            
            console.log('Parsed words:', this.words);
            // Reset to first page
            this.currentPage = 1;
        },
        async regenerateDeck() {
            try {
                this.isLoading = true;
                // Get data from API store
                const apiData = this.apiStore.data;
                
                // Get current sentences for marked indices
                const currentStuff = {};
                this.markedForRegeneration.forEach(index => {
                    if (this.words[index]) {
                        currentSentences[index] = {
                            originalWord: this.words[index][0],
                            lemmaVersion: this.words[index][1],
                            originalSentence: this.words[index][2],
                            russianTranslation: this.words[index][3],
                            generatedSentence: this.words[index][4],
                            generatedSentenceRussian: this.words[index][5]
                        };
                    }
                });
                
                // Add marked sentences and current data to the request
                const requestData = {
                    currentStuff: currentStuff
                };
                
                const response = await fetch("http://127.0.0.1:8000/wordlist/regenerate/post", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData)
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const csvText = await blob.text();
                    this.parseCSVToWords(csvText);
                    // Clear marked sentences after regeneration
                    this.markedForRegeneration.clear();
                    alert('Колода успешно перегенерирована!');
                } else {
                    alert('Ошибка при перегенерации колоды');
                }
            } catch (error) {
                console.error('Error regenerating deck:', error);
                alert('Ошибка при перегенерации колоды');
            } finally {
                this.isLoading = false;
            }
        },
        toggleMarkForRegeneration(wordIndex) {
            const globalIndex = (this.currentPage - 1) * this.pageSize + wordIndex;
            if (this.markedForRegeneration.has(globalIndex)) {
                this.markedForRegeneration.delete(globalIndex);
            } else {
                this.markedForRegeneration.add(globalIndex);
            }
        },
    },
    watch: {
        isDone(newIsDone) {

        }
    }
}
</script>

<template>
   <main>
    <div class="copy-csv-row">
      <button class="copy-csv-btn" @click="copyWordsToCSV">Скопировать как CSV</button>
      <button class="regenerate-btn" @click="regenerateDeck">Перегенерировать колоду</button>
      <span v-if="copySuccess" class="copy-success">Скопировано!</span>
    </div>
    <header>
        <h2 @click="goBack"><-- Вернуться к подбору слов</h2>
    </header>
        <div class = "header">Предварительный просмотр деки</div>
        
        <!-- Loading overlay -->
        <div v-if="isLoading" class="loading-overlay">
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Генерация колоды...</p>
            </div>
        </div>
        <table class="word-table">
  <thead>
    <tr>
      <th>Исходное слово</th>
      <th>Лемм. версия слова</th>
      <th>Исходное предложение</th>
      <th>Перевод слова на русский</th>
      <th>Сгенерированное предложение</th>
      <th>Сгенерированное предложение на русском</th>
    </tr>
    <!-- 
      слово ориг
      лемм. версия слова (н.ф)
      исходное предложение
      перевод слова на русское
      сгенерированное предложение
      перевод сгенерированного предложения

      сделать все инпутами
      отметка перегенирации колоды

      передавать в стор измененный массив words
      сделать отметку для предложений которые были плохо сделаны, отмечать эту отметку в
      -->
  </thead>
  <tbody>
    <tr v-for="(word, idx) in paginatedWords" :key="word[0]">
      <td>
        <input
          v-model="words[(currentPage-1)*pageSize+idx][0]"
          class="edit-input"
          type="text"
          :placeholder="'Исходное слово'"
        />
      </td>
      <td>
        <input
          v-model="words[(currentPage-1)*pageSize+idx][1]"
          class="edit-input"
          type="text"
          :placeholder="'Лемм. версия слова'"
        />
      </td>
      <td>
        <input
          v-model="words[(currentPage-1)*pageSize+idx][2]"
          class="edit-input"
          type="text"
          :placeholder="'Исходное предложение'"
        />
      </td>
      <td>
        <input
          v-model="words[(currentPage-1)*pageSize+idx][3]"
          class="edit-input"
          type="text"
          :placeholder="'Перевод слова на русский'"
        />
      </td>
      <td>
        <div class="sentence-cell">
          <input
            v-model="words[(currentPage-1)*pageSize+idx][4]"
            class="edit-input"
            type="text"
            :placeholder="'Сгенерированное предложение'"
          />
          <button 
            @click="toggleMarkForRegeneration(idx)"
            :class="['mark-btn', { 'marked': markedForRegeneration.has((currentPage-1)*pageSize+idx) }]"
            :title="markedForRegeneration.has((currentPage-1)*pageSize+idx) ? 'Убрать отметку' : 'Отметить для регенерации'"
          >
            {{ markedForRegeneration.has((currentPage-1)*pageSize+idx) ? '✓' : '!' }}
          </button>
        </div>
      </td>
      <td>
        <input
          v-model="words[(currentPage-1)*pageSize+idx][5]"
          class="edit-input"
          type="text"
          :placeholder="'Сгенерированное предложение на русском'"
        />
      </td>
    </tr>
  </tbody>
</table>
        <div class="pagination">    
          <button @click="prevPage" :disabled="currentPage === 1">Назад</button>
          <span>Страница {{ currentPage }} из {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">Вперёд</button>
        </div>
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
    .word-table {
        width: 100%;
        border-collapse: collapse;
        margin: 30px 0;
        background: rgba(255,255,255,0.05);
        color: white;
        font-size: 16px;
    }
    .word-table th, .word-table td {
        border: 1px solid #fff;
        padding: 8px 12px;
        text-align: center;
    }
    .word-table th {
        background: rgba(255,255,255,0.15);
        font-weight: 500;
    }
    .word-table tr:nth-child(even) {
        background: rgba(255,255,255,0.07);
    }
    .edit-input {
        width: 100%;
        background: rgba(255,255,255,0.1);
        color: #fff;
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 15px;
        box-sizing: border-box;
    }
    .edit-input:focus {
        outline: 1.5px solid #fff;
        background: rgba(255,255,255,0.2);
    }
    td input{
        text-align: center;
    }
    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
        gap: 16px;
        font-size: 16px;
    }
    .pagination button {
        background: #222;
        color: #fff;
        border: 1px solid #fff;
        border-radius: 4px;
        padding: 6px 16px;
        font-size: 15px;
        cursor: pointer;
        transition: background 0.2s;
    }
    .pagination button:disabled {
        background: #555;
        color: #aaa;
        cursor: not-allowed;
    }
    .copy-csv-row {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 18px;
        margin-top: 10px;
        justify-content: flex-end;
    }
    .copy-csv-btn {
        background: #222;
        color: #fff;
        border: 1px solid #fff;
        border-radius: 4px;
        padding: 6px 16px;
        font-size: 15px;
        cursor: pointer;
        transition: background 0.2s;
    }
    .copy-csv-btn:hover {
        background: #444;
    }
    .regenerate-btn {
        background: #2a4a2a;
        color: #fff;
        border: 1px solid #4a7c4a;
        border-radius: 4px;
        padding: 6px 16px;
        font-size: 15px;
        cursor: pointer;
        transition: background 0.2s;
    }
    .regenerate-btn:hover {
        background: #3a5a3a;
    }
    .copy-success {
        color: #7fff7f;
        font-size: 15px;
        font-weight: 500;
    }
    .sentence-cell {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .sentence-cell .edit-input {
        flex: 1;
    }
    .mark-btn {
        background: #444;
        color: #fff;
        border: 1px solid #666;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.2s;
        min-width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .mark-btn:hover {
        background: #555;
    }
    .mark-btn.marked {
        background: #d32f2f;
        border-color: #f44336;
        color: #fff;
    }
    .mark-btn.marked:hover {
        background: #b71c1c;
    }
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }
    .loading-spinner {
        text-align: center;
        color: white;
    }
    .spinner {
        width: 50px;
        height: 50px;
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-top: 4px solid #fff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 20px;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .loading-spinner p {
        font-size: 18px;
        margin: 0;
        opacity: 0.9;
    }
</style>