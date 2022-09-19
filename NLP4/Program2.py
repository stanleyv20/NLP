# Language Models
import os
import pathlib
import sys
import pickle
from nltk import word_tokenize, ngrams


def calculate_probability(test_line, language_unigrams, language_bigrams, vocab_size):
    # Creating lists of unigrams and bigrams for current line provided from test file
    test_line_unigrams = word_tokenize(test_line)
    test_line_bigrams = list(ngrams(test_line_unigrams, 2))

    probability = 1  # Using 1 for calculating probability with Laplace smoothing
    v = vocab_size  # Total length of all three languages

    # For each bigram found in the test line, get bigram count and unigram count of first word in the bigram
    for bigram_instance in test_line_bigrams:
        b = language_bigrams[bigram_instance] if bigram_instance in language_bigrams else 0
        u = language_unigrams[bigram_instance[0]] if bigram_instance[0] in language_unigrams else 0
        # Perform bigram probability calculation using Laplace smoothing
        probability = probability * ((b + 1) / (u + v))
    return probability


if __name__ == '__main__':
    # Read and deserialize language dictionaries
    english_unigrams = pickle.load(open('English_unigrams', 'rb'))
    english_bigrams = pickle.load(open('English_bigrams', 'rb'))

    french_unigrams = pickle.load(open('French_unigrams', 'rb'))
    french_bigrams = pickle.load(open('French_bigrams', 'rb'))

    italian_unigrams = pickle.load(open('Italian_unigrams', 'rb'))
    italian_bigrams = pickle.load(open('Italian_bigrams', 'rb'))

    #  Calculate total vocab size for use in probability calculation by adding lengths of unigram dictionaries
    total_vocab_length = len(english_unigrams) + len(french_unigrams) + len(italian_unigrams)

    #  Read test file into a list of lines
    directory = 'data'  # Assuming files are within a directory entitled data
    test_file_path = os.path.join(directory, 'LangId.test')
    if os.path.isfile(test_file_path):
        file_path = pathlib.Path(test_file_path)
        with open(file_path, 'r') as myFile:
            # creating list containing elements for each line and removing newline character
            line_list = [line.rstrip('\n') for line in myFile]
    else:
        sys.exit('Unable to locate test file!')

    output_file_name = 'probable_language_predictions.txt'
    solution_file_name = 'LangId.sol'

    # Performing calculation for each line and writing most likely language per line to output file
    with open(output_file_name, 'w') as output_file:
        for iteration, line in enumerate(line_list):
            # Determine each languages probability
            line_prob_english = calculate_probability(line, english_unigrams, english_bigrams, total_vocab_length)
            line_prob_french = calculate_probability(line, french_unigrams, french_bigrams, total_vocab_length)
            line_prob_italian = calculate_probability(line, italian_unigrams, italian_bigrams, total_vocab_length)

            # Determine language with highest probability and write to file
            lang_calculations = {'English': line_prob_english, 'French': line_prob_french, 'Italian': line_prob_italian}
            most_likely_lang = max(lang_calculations, key=lang_calculations.get)
            output_file.write(f'{iteration + 1} {most_likely_lang}\n')

    #  Validate language classifications
    correct = 0
    incorrect = 0
    output_file_path = os.path.join(sys.path[0], output_file_name)
    solution_file_path = os.path.join('data', solution_file_name)
    incorrect_line_numbers = []

    # Opening output file containing predicted languages and solution file
    if os.path.isfile(output_file_path) and os.path.isfile(solution_file_path):
        output_file = pathlib.Path(output_file_path)
        solution_file = pathlib.Path(solution_file_path)
        with open(output_file, 'r') as output:
            with open(solution_file, 'r') as solution:
                for output_line in output:
                    # Compare each line in output to solution file and increment correct or incorrect count accordingly
                    for solution_line in solution:
                        if output_line != solution_line:
                            incorrect += 1
                            # Keep track of incorrectly classified line numbers by appending to list
                            incorrect_line_numbers.append(int(output_line.split()[0]))
                            break
                        else:
                            correct += 1
                            break

    else:
        sys.exit('Output or solution file not found')

    #  Calculating and print accuracy along with miss classified line numbers
    percentage = "{:.2%}".format((correct / (correct + incorrect)))
    print(f'Accuracy: {percentage}')
    print(f'Incorrectly Classified Lines: \n{incorrect_line_numbers}')
