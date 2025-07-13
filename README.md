

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img src="./images/danko.png" alt="Logo" width="350" height="350">
  <h3 align="center"> Anki Deck Generator<br></h3>

  <p align="center">
    What if you could learn a new language with Anki cards—using your favorite songs or book passages, in the easy and creative way?<br/><br>
    <a href="https://github.com/AnkiGen/anki_deck/deployments/github-pages"><strong>Check it out!</strong></a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
<li><a href="#hyperlinks-to-docs">Hyperlinks to docs</a></li>    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Whether you're a language enthusiast, a curious learner, or a developer exploring NLP-powered tools,  **Anki Deck Generator**  helps you learn languages in context—sentence by sentence. 

With our project you can turn your *favorite songs* or *books* into **personalized Anki flashcards.** 


### Built With
* [![Vue][Vue.js]][Vue-url]  
* [![Python][Python.com]][Python-url] 
* [![OpenAI][OpenAI.com]][OpenAI-url]  
* [![spaCy][spaCy.com]][spaCy-url]  
* [![FastAPI][FastAPI.com]][FastAPI-url]  
* [![Node.js][Node.js.com]][Node.js-url]
### Project Context Diagram
<img src="./images/Context Diagram.jpg" alt="context diagram" width="800" height="650">

<!-- GETTING STARTED -->
## Getting Started

You can run our project in these ways:
### 1. Use the Deployed Web Version
The easiest way!
Just access this [link.](https://github.com/AnkiGen/anki_deck/deployments/github-pages)

### 2. Run with Docker (Recommended)
#### Prerequisites
* docker

#### Installation
1. Download docker deskop on your computer.
2. Launch docker desktop application.
3.  Create ``.env`` with
```python
OPENAI_API_KEY=TOKEN
```
and replace ``TOKEN`` with your GPT token.
4. Open terminal in directory with `.env` file.
5. 
```bash
docker pull dkddjdjjfjdj/anki-deck
```
6.
```bash
docker run --env-file .env -p 8000:8000 dkddjdjjfjdj/anki-deck
```
7. After that in browser go to https://localhost:8000/
### 3. Run Locally with Node.js (Dev. Mode)
#### Prerequisites
* npm
* node.js
* git
#### Installation
1. Clone our repository: ```git clone https://github.com/AnkiGen/anki_deck.git```
2. Get into the directory: ```cd anki_deck```
3. Install all dependencies: ```npm install```
4. Start the app: ```npm run dev```

Link to the Docker Hub: [Click me!](https://hub.docker.com/repository/docker/dkddjdjjfjdj/anki-deck/general)



<!-- USAGE EXAMPLES -->
## Usage

*In the very beggining...*
You have the opportunity to choose the way of creating an Anki deck!
1) Create deck using the most common and must-known words in English (Great for beginners!)
2) Create deck using the text from your book or song.
(Good for learners who know the basics and want to move further!)
<img src = "./images/1.png" width = "1000" height = "1000"> <!--- Основная вкладка -->

If you go with the **first choice**, the deck is automatically generated and you are welcome to download the deck in ```.csv``` or ```.apkg``` format

If you choose the **second choice**, you need to submit the text in raw format.
<img src = "./images/2.png" width = "1000" height = "1000"> <!--- Ввод текста -->
Then proceed to *filters*, choose maximal count of words in text and the amount of unknown words in deck.
<img src = "./images/7.png" width = "1000" height = "1000"> <!--- Фильтр -->
Then you have these ways of choosing words into the deck:
1) Tinder
2) Manual
3) Word List
Let us go by each of these:
#### Tinder
Very simple to use, mobile, but does not let you control every word in the proposed text. 
- Swipe to the **left** to mark the word as don't want to learn (won't be added to deck)
- Swipe to the **right** to make the word as want to learn (will be added to deck)
- Click on the **top-right** to mark the word as already known.
<img src = "./images/3.png" width = "1000" height = "1000"> <!--- Тиндер -->
#### Manual 
Somewhat complex, but yet, very powerful way of choosing words for the deck.
You are presented with the whole text you've submitted.
- By **one-time clicking** the word, you mark it green as want to learn
- By **double clicking** the word, you mark it as read as don't want to learn
- By **clicking thrice** you unmark the word
- <img src = "./images/8.png" width = "1000" height = "1000"> <!--- Ручной ввод -->
#### Word List
Presents list of multiple word cards!
Same as in manual:
- By **one-time clicking** the card, you mark it green as want to learn
- By **double clicking** the card, you mark it as read as don't want to learn
- By **clicking thrice** you unmark the card
<img src = "./images/4.png" width = "1000" height = "1000"> <!--- Список слов -->

After finishing choosing words, you are presented to the preliminary view of your generated Anki deck card. You could manually change the word translation and context if needed. 
Also, there is a possibility to **copy** the table in ```.csv``` format for manual change.
<img src = "./images/5.png" width = "1000" height = "1000"> <!--- Предварительный просмотр карт -->
When everything is done, you can proceed further for the download in ```.csv``` or ```.apkg``` formats!
<img src = "./images/6.png" width = "1000" height = "1000"> <!--- Скачать колоду в формате ... -->
<!-- ROADMAP -->
## Roadmap
 - [x] Working website run with docker
 - [x] User can mark words as known/unknown to improve quality of sentences
 - [x] Tinder-style selecting is provided
 - [x] User can choose number of words he want to learn and length of generated sentence
 - [x] Sentences are generated considering context
 - [x] On the final page user can download csv file with proper fields
 - [x] Review for the generated deck
 - [x] Change the design for the website
 - [x] Remove automatically redundant symbols, s.a. [1], the, a, an, etc...
 - [x] Finish the documentation
 - [x] Improved deck generation logic
 - [ ] Make filter limitations work correctly
 - [ ] Add possibility to fetch text by writing author and song name
 - [ ] Voicover for words
 - [ ] Teacher student system
 - [ ] Add possibility to fetch text by writing author and song name
 See all our tasks [here](https://github.com/orgs/AnkiGen/projects/3)


<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**!

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a **star**! 

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top contributors:

<a href="https://github.com/AnkiGen/anki_deck/graphs/contributors">
  <img src="./images/sc1.png" alt="contrib image"/>
</a>




<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<!-- LINKS -->
##  Hyperlinks to Docs
- ```Contributing.MD``` with the information about the project: [click me!](https://github.com/AnkiGen/anki_deck/blob/master/CONTRIBUTING.md)
- ```Git Graph``` with the information about the git process: [click me!](https://github.com/AnkiGen/anki_deck/blob/master/docs/GitGraph.png)
- ```Quality Attribute Scenarios``` with the information about the user scenarios for quality: [click me!](https://github.com/AnkiGen/anki_deck/blob/master/docs/quality-attributes/quality-attribute-scenarios.md)
- ```User Acceptance Tests``` with the information about the user tests: [click me!](https://github.com/AnkiGen/anki_deck/blob/master/docs/quality-assurance/user-acceptance-tests.md)
- ```Architecture``` with the information of views: deployment, dynamic, static: [click me!](https://github.com/AnkiGen/anki_deck/tree/master/docs/architecture)



<!-- CONTACT -->
## Contact
Viktor K. – Team lead, Frontend developer <br>
telegram: @vitec_321 <br> <br>
Ivan K. – UX/UI designer, Frontend developer  <br>
telegram: @vanyaspapayas <br> <br>
Anastasia P. – Designer, Tester <br>
telegram: @anastayshaa_a <br> <br>
Ilya S. – Backend developer <br>
telegram: @ISNJI <br> <br>
Albert M. – Backend developer <br>
telegram: @NeuroticExistentialDissonance <br> <br>
Vadim G. – Backend developer <br>
telegram: @FleshTeaml <br>








<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: ./images/sc1.png
[contributors-url]: https://github.com/AnkiGen/anki_deck/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Python.com]: https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/

[OpenAI.com]: https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white
[OpenAI-url]: https://openai.com/

[spaCy.com]: https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white
[spaCy-url]: https://spacy.io/

[FastAPI.com]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/

[Node.js.com]: https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white
[Node.js-url]: https://nodejs.org/
