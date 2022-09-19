# Word Guessing Game
import sys
import pathlib
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random


# Calculates and prints lexical diversity for input text
def calculate_lexical_diversity(raw_text):
    # Tokenize input
    lex_diversity_tokens = nltk.word_tokenize(raw_text)

    # Make tokens lower case
    lower_tokens = [word.lower() for word in lex_diversity_tokens]

    # Remove stopwords using nltk
    stoppers = set(stopwords.words('english'))
    stopless_tokens = [word for word in lower_tokens if word not in stoppers and word.isalpha()]
    unique_tokens = set(stopless_tokens)

    # Calculating lexical diversity by dividing count of unique tokens by total count of tokens
    lex_diversity = (len(unique_tokens) / len(stopless_tokens))
    print(f'\nLexical Diversity: {lex_diversity:.2f}')  # Formatting output to 2 decimal places


# Performs preprocessing on text and returns lists of processed tokens and nouns
def preprocess_text(raw_text):
    # Tokenize input and make lower-case
    tokens = nltk.word_tokenize(raw_text)
    lower_tokens = [word.lower() for word in tokens]

    # Remove words if in NLTK stop word list, less than 6 characters in length, or not alpha
    stoppers = set(stopwords.words('english'))
    stopless_tokens = [word for word in lower_tokens if word not in stoppers]
    filtered_words = [word for word in stopless_tokens if (word.isalpha() and (len(word) > 5))]

    # Making list of unique lemmas from tokens
    important_words_set = set(filtered_words)
    lemma_factory = WordNetLemmatizer()
    lemmas = [lemma_factory.lemmatize(token) for token in important_words_set]
    unique_lemmas = list(set(lemmas))

    # Part of Speech Tagging
    speech_tags = nltk.pos_tag(unique_lemmas)
    print(f'First 20 POS tags: {speech_tags[0:20]}')
    nouns = [word for (word, pos_tag) in nltk.pos_tag(unique_lemmas) if(pos_tag[:2] == 'NN')]
    print(f'Number of unique tokens: {len(filtered_words)}')
    print(f'Number of nouns: {len(nouns)}')
    return filtered_words, nouns


# Function to conduct guessing game, takes list of possible word choices and initial starting score as input
def guessing_game(words, score=5):
    # For each game run - randomly select new word, clear guessed letters, reset matched letter count and current guess
    selected_word = random.choice(words)
    guessed_letters = []
    current_guess = None
    print('Enter \'!\' to end game')
    matched_letters = 0

    # Uncomment below line to simplify game debugging
    # print(f'selected word: {selected_word}')

    # Game runs while score is not negative, letters are unguessed in current word, and user has not exited program
    while score >= 0 and matched_letters < len(selected_word) and current_guess != '!':
        # Print correctly guessed letters and remaining blanks
        for letter in selected_word:
            if letter in guessed_letters:
                print(letter, end='')
            else:
                print('_', end='')

        # Get user input, update score accordingly, start new run of game with another word if current word is complete
        current_guess = input('\n\nGuess a letter:')
        if current_guess != '!':
            if current_guess not in guessed_letters:
                guessed_letters.append(current_guess)
                if current_guess in selected_word:
                    score += 1
                    print(f'Right! Score is {score}')
                    matched_letters += selected_word.count(current_guess)
                else:
                    score -= 1
                    if score >= 0:
                        print(f'Sorry, guess again. Current score is: {score}')
                    else:
                        print('Sorry, score is negative - ending game!')
                        print(f'Selected Word was: {selected_word}')
                if matched_letters == len(selected_word):
                    print('You solved it!')
                    print(f'Word: {selected_word}')
                    print(f'Current score: {score}')
                    print('Guess another word')
                    guessing_game(words, score)  # Invoke guessing game again but with current score
            else:
                print('Please guess a letter not already tried!')
                print(f'Guessed Letters: {guessed_letters}')
                print(f'Current Score is {score}')
        else:
            print('Ending Game!')


if __name__ == '__main__':
    # Check if sys arg was provided indicating data file path
    if len(sys.argv) < 2:
        sys.exit('Please provide sysarg indicating path of data file!')
    dataFilePath = sys.argv[1]

    # Read file using pathlib to ensure cross platform support
    path = pathlib.Path(dataFilePath)
    with open(path, 'r') as myFile:
        contents = myFile.read()

    # Calculate and print lexical diversity
    calculate_lexical_diversity(contents)

    # Preprocess text and get list of tokens and nouns
    tokens, nouns = preprocess_text(contents)

    # Creating dictionary of {noun:count of noun in tokens}, printing top 50 words and their counts
    noun_occurrence_dict = dict((n, tokens.count(n)) for n in nouns)
    sorted_nouns = {k: v for k, v in sorted(noun_occurrence_dict.items(), key=lambda x: x[1], reverse=True)}
    print(f'Top 50 Nouns: {list(sorted_nouns.items())[:50]}')

    # Saving list of top 50 most common words (nouns) for word guessing game
    popular_nouns = list(sorted_nouns.keys())[:50]

    # Start word guessing game
    print('Lets play a word guessing game!')
    guessing_game(popular_nouns)
