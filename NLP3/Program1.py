# Text Analysis
# Program 1 & Address Class File
import os
import pathlib
import sys
import nltk
import pickle
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Address class representing an inaugural address instance
class Address:
    def __init__(self, year, president, original_text):
        self.year = year
        self.president = president
        self.original_text = original_text
        original_tokens = nltk.tokenize.word_tokenize(original_text)
        original_alpha_tokens = [word for word in original_tokens if word.isalpha()]
        self.original_text_token_length = len(original_alpha_tokens)
        self.processed_token_list = preprocess_text(original_text)
        self.most_common_tokens = get_most_common_tokens(self.processed_token_list)
        self.readability_score = None
        self.readability_rating = None
        self.sentiment = None

    # Calculate readability score using Lasbarhetsindex (LIX) and assign score & rating attributes of Address instance
    def calculate_readability(self):
        readability_rating = None
        sentence_list = nltk.sent_tokenize(self.original_text)
        token_list = nltk.word_tokenize(self.original_text)
        total_word_count = len(token_list)
        sentence_count = len(sentence_list)
        long_words = [word for word in token_list if len(word) > 6]
        long_word_count = len(long_words)
        readability_score = (total_word_count / sentence_count) + ((long_word_count * 100) / total_word_count)

        # Determine readability_rating (string)
        if readability_score < 25:
            readability_rating = 'Children'
        elif 25 <= readability_score < 30:
            readability_rating = 'Simple'
        elif 30 <= readability_score < 40:
            readability_rating = 'Normal'
        elif 40 <= readability_score < 50:
            readability_rating = 'Factual'
        elif 50 <= readability_score < 60:
            readability_rating = 'Technical'
        elif readability_score > 60:
            readability_rating = 'Difficult'

        # Assign readability score and rating attributes for current Address instance
        self.readability_score = readability_score
        self.readability_rating = readability_rating

    # Calculate sentiment using VADAR and assign to sentiment attribute of Address instance
    def calculate_sentiment(self):
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(self.original_text)
        self.sentiment = vs

    # Print attributes for Address instance
    def display_attributes(self):
        print(f'\nYear: {self.year}', f'President: {self.president}',
              f'Original Text Word Length: {self.original_text_token_length}',
              f'Processed Tokens (first 25): {self.processed_token_list[:25]}',
              f'Top 25 most common tokens: {self.most_common_tokens}',
              f'Readability Score: {self.readability_score}',
              f'Readability Rating: {self.readability_rating}',
              f'First 300 characters of original Text: {self.original_text[:300]}',
              f'Sentiment: {self.sentiment}', sep="\n")


# Determines and returns 25 most commonly occurring tokens from preprocessed tokens
def get_most_common_tokens(filtered_tokens):
    token_occurrence_dictionary = dict((t, filtered_tokens.count(t)) for t in filtered_tokens)
    ordered_counts = {k: v for k, v in sorted(token_occurrence_dictionary.items(), key=lambda x: x[1], reverse=True)}
    most_common = list(ordered_counts.keys())[:25]
    return most_common


# preprocess text and return list of tokens that are lower case, alpha, and have stop words removed
def preprocess_text(raw_text):
    file_tokens = nltk.word_tokenize(raw_text)
    lower_tokens = [word.lower() for word in file_tokens]
    stoppers = set(nltk.corpus.stopwords.words('english'))
    stopless_tokens = [word for word in lower_tokens if word not in stoppers]
    filtered_words = [word for word in stopless_tokens if word.isalpha()]
    return filtered_words


if __name__ == '__main__':
    print('Program 1 execution has begun, please wait a few moments for processing!')
    directory = 'inaugural'  # Assuming files are within a directory entitled inaugural
    address_dictionary = {}

    # For each file in the inaugural directory:
    # read file, create Address instance, calculate readability & sentiment, and add to dictionary
    for file_instance in os.listdir(directory):
        current_file_path = os.path.join(directory, file_instance)
        if os.path.isfile(current_file_path):

            if current_file_path != 'inaugural/README':  # Condition to ignore attempting to parse README file name

                # Parse file path to retrieve president name and address year
                split_file_path = current_file_path[10:].replace(".txt", "", 1).split('-')
                address_year = split_file_path[0]
                address_president = split_file_path[1]

                # Read file using pathlib to ensure cross platform support
                path = pathlib.Path(current_file_path)

                with open(path, 'r', errors='ignore') as myFile:
                    file_content = myFile.read()

                    # Instantiate new Address instance
                    current_address = Address(address_year, address_president, file_content)

                    # Invoke methods for calculating readability and sentiment,
                    # all other attributes are determined and assigned via Address constructor
                    current_address.calculate_readability()
                    current_address.calculate_sentiment()

                    # Adding address instances to dictionary
                    address_dictionary[(address_president, address_year)] = current_address

    # Serialize person dictionary to pickle file
    pickle.dump(address_dictionary, open('InauguralPickle', 'wb'))  # writing binary

    sys.exit('Execution of Program1 is complete')
