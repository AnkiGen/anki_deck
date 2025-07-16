### Unit tests: 
1. **TestSplittingFunction** class contains tests for the splitting function, which split text into tokens and filter them:
  - *test_basic_sentence*:\
  Checks that from the sentence, the words are satisfied to conditions.
  Ensures that punctuation marks ,, !, . are not included in the resulting list.
  - *test_stopwords_and_punctuation*:\
  Verifies that stopwords and punctuation are excluded from the results.
Confirms that key words are present.
  - *test_word_with_hyphen_and_apostrophe*
  
    Checks handling of words with hyphens and apostrophes.

  - *test_non_matching_tokens_excluded*:  
  Validates that when input is a string of symbols and numbers, the result is an empty list.
  - *test_empty_string*:\
Tests the function with an empty string, expecting an empty list as output.
2. **TestLemmatization** class contains tests for the lemmatization function, which uses spaCy to lemmatize words.
   - *test_lemmatization_basic*:\
   Mocks spaCy loading and returns lemmas for words.\
    Checks that lemmas are correctly added to the respective categories: known_words, unknown_words, unwanted_words.
   - *test_multiple_words*:\
    Mocks processing multiple words.
Validates correct lemmatization and categorization.
3. **TestAppearance** class tests whether a word appears in a list of sentences.
   - *test_word_found_exact_match*:\
Checks that the word is found in the sentence.
   - *test_word_found_case_insensitive*:\
Validates that word is detected in regardless of case.
   - *test_word_not_found*:\
Confirms that word is not found in.
   - *test_multiple_sentences_some_match*:\
Verifies that in sentences the word is not detected.
In another sentences the word is detected.

   - *test_empty_sentences*:\
Tests that an empty list of sentences yields False.
4. **TestGPT** class tests functions involved in prompt creation, response parsing, and CSV making.
    - *test_generate_prompt*:\
Creates a prompt with given data.\
Checks that the prompt contains the phrase "Unknown words:", includes all unknown words, and references the count.
   - *test_parse_response_to_dicts*:\
Parses a sample GPT response into a list of dictionaries.
Validates that each dictionary contains keys:
*word, word_translation, context_sentence, sentence1, sentence1_translation*.\
Confirms the correctness of the first and second entries.
   - *test_write_cards_to_csv*:\
   Checks that the function generates a PlainTextResponse object with content including the needed words.\
   Verifies that the content contains headers like "word" and "lemma".

### Integration tests:
- *test_root*:\
Verify that the root endpoint responds with a status code 200 and a message indicating the server is running.
  - **Expected Behavior**:\
  Returns status code 200 with JSON: {"message": "FastAPI is working!"}.
- *test_post_and_get_user*:\
Test user creation via POST request and subsequent retrieval via GET request.\
  - **Expected Behavior**:\
  User is successfully created and retrievable with correct data fields.
- *test_get_deck*:\
Verify fetching a deck by deck_id.
  - **Expected Behavior**:
  Returns deck data matching the provided ID with associated cards and user information.
- *test_post_deck*:\
Test creating a new deck with specified user ID and list of card IDs.
  - **Expected Behavior**:
  Deck creation acknowledged successfully.
- *test_get_card*:\
Verify fetching a card by card_id.
  - **Expected Behavior**:
  Correct card data is returned for the specified ID.
- *test_post_card*:\
Test adding a new card with specified word_id and sentences.
  - **Expected Behavior**:
  Confirmation "status": "ok" upon successful creation.
- *test_get_by_word*:\
Retrieve word data by word string.
  - **Expected Behavior**:
  Returns the correct word data if it exists.
- *test_get_by_id*:\
  Retrieve word data by word_id.
  - **Expected Behavior**:
  Returns data for the specified word ID.
- *test_post_word*:\
Create a new word entry with relevant details.
  - **Expected Behavior**:
  New word entry is successfully stored.
- *test_wordlist_regeneration_with_empty_current_stuff*:\
  Test regenerating a word list with an empty currentStuff.
  - **Expected Behavior**:
  Operation completes successfully with no current data.
- *test_wordlist_regeneration_invalid_payload*:\
  Test handling of invalid payload lacking required fields.
  - **Expected Behavior**:
  Request fails validation due to missing data.
- *test_get_user_not_found*:\
  Verify response when requesting a nonexistent user.
  - **Expected Behavior**:
  Indicates user not found.
- *test_get_deck_not_found*:\
  Verify response when requesting a nonexistent deck.
  - **Expected Behavior**:
  Indicates deck not found.
- *test_get_card_not_found*:\
  Verify response when requesting a nonexistent card.
  - **Expected Behavior**:
  Indicates card not found.
- *test_get_by_word_not_found*:\
  Verify response when searching for a nonexistent word.
  - **Expected Behavior**:
  Indicates word not found.
- *test_get_by_id_not_found*:\
  Verify response when requesting a nonexistent word ID.
  - **Expected Behavior**:
  Indicates data not found.
