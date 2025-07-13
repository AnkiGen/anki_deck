//This file represents the store for data.
//It is used to transfer user text from textarea between input.vue and filterFromText.vue

import { defineStore } from "pinia";

export const useUserTextStoreV = defineStore('userTextV', {
    state: () => ({
        words: [],  // to choose from in tinder and etc
        yesLearn: [], // want to learn
        noLearn: [], // dont want to learn
        countLearn: 0, // max amount of words in text
        known: [], // list of already known words
        unknown: 0, // max amount of unknown words in sentence
        context: [], //source sentences from original text
        csvData: [] // final CSV data for the deck
    }),
    actions: {
        setText(text) {
            this.words = text;
        },
        setYes(yes) {
            this.yesLearn = yes;
        },
        setNo(no) {
            this.noLearn = no;
        },
        setCount(count) {
            this.countLearn = count;
        },
        setKnown(known) {
            this.known = known;
        },
        setUnknown(unknown) {
            this.unknown = unknown;
        },
        setContext(context) {
            this.context = context;
        },
        setCsv(csvData) {
            // Store the final CSV data
            this.csvData = csvData;
        },
        resetStore() {
            this.words = [];
            this.yesLearn = [];
            this.noLearn = [];
            this.countLearn = 0;
            this.known = [];
        },
        startAgain() {
            this.yesLearn = [];
            this.noLearn = [];
            this.known = [];
        }
    },
    persist: {
        enabled: true,
        strategies: [
            {
                key: "userText",
                storage: sessionStorage,
                paths: ['words', 'yesLearn', 'noLearn', 'known']
            }
        ]
    }
});