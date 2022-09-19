import os
import pathlib
from nltk import word_tokenize, ngrams
import pickle
import sys


# Process file to create and return lists of unigrams and bigrams
# Accepts filename as input
def process_language_file(requested_file):
    directory = 'data'  # Assuming files are within a directory entitled data
    file_path = os.path.join(directory, requested_file)

    # Read text from file
    if os.path.isfile(file_path):
        # Read file using pathlib to ensure cross platform support
        file_path = pathlib.Path(file_path)
        with open(file_path, 'r') as myFile:
            file_contents = myFile.read()

    file_contents = file_contents.rstrip('\n').lower()  # Removing newlines
    tokens = word_tokenize(file_contents)  # Tokenizing text

    # Creating lists of unigrams and bigrams using ngrams method of NLTK library
    unigrams = list(ngrams(tokens, 1))
    bigrams = list(ngrams(tokens, 2))

    # Creating dictionaries of unique unigrams and bigrams along with count of occurrences
    unigram_dict = {u: unigrams.count(u) for u in set(unigrams)}
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}
    return unigram_dict, bigram_dict


if __name__ == '__main__':
    #  Create unigram and bigram dictionaries for each language and save to pickle file
    languages = ['English', 'French', 'Italian']
    for language in languages:
        unigram_counts, bigram_counts = process_language_file('LangId.train.' + language)
        # Serialize unigram and bigram dictionaries to pickle files for use in Program 2
        pickle.dump(unigram_counts, open(language + '_unigrams', 'wb'))  # writing binary
        pickle.dump(bigram_counts, open(language + '_bigrams', 'wb'))  # writing binary

    sys.exit('Execution of Program 1 is complete')
