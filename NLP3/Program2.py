# Text Analysis
# Program 2 File

import sys
from Program1 import Address
import pickle
import math
import nltk


# calculate and return point-wise mutual information score &
# string indicating if requested phrase is likely to be a collocation
def calculate_pmi(address_dictionary, collocation_phrase):
    # ensuring input phrase is lowercase to avoid missing matches due to capitalization discrepencies
    collocation_phrase_string = ' '.join(collocation_phrase).lower()

    # combine inaugural addresses to create one complete corpus of lowercase text for PMI calculation
    combined_corpus = ''
    for address in address_dictionary.values():
        combined_corpus += address.original_text
    combined_corpus = combined_corpus.lower()
    corpus_tokens = nltk.word_tokenize(combined_corpus)
    token_count = len(corpus_tokens)

    pmi_string = None
    # return 0 if not instances of 2 word phrase found together in corpus - also avoids divide by zero exception
    if combined_corpus.count(collocation_phrase_string) == 0:
        pmi = 0.00
        pmi_string = 'This is not a collocation'
        return pmi, pmi_string

    # Performing PMI calculation
    # taking log of ((instances of both words together) / ((instances of word 1) * (instances of word 2)))
    hg = combined_corpus.count(collocation_phrase_string) / token_count
    h = combined_corpus.count(collocation_phrase[0].lower()) / token_count
    g = combined_corpus.count(collocation_phrase[1].lower()) / token_count
    pmi = math.log2(hg / (h * g))

    # Positive PMI scores indicate that phrase is likely a collocation, negative indicates likely not a collocation
    if pmi > 0:
        pmi_string = 'point-wise mutual information measure indicates this is likely a collocation'
    else:
        pmi_string = 'point-wise mutual information measure indicates this is likely not a collocation'

    return pmi, pmi_string


if __name__ == '__main__':
    print('Welcome to Inaugural Address Explorer')
    presidents = []
    current_input = None

    # Read and deserialize dictionary of Addresses from pickle file
    inaugural_addresses = pickle.load(open('inauguralPickle', 'rb'))  # reading binary

    # Creating set of presidents - used for Address selection
    for president, year in inaugural_addresses.keys():
        presidents.append(president)
    presidents = set(presidents)

    while current_input != '9':
        print('\nSelection Menu:',
              '1. See a list of Presidents',
              '2. Look up addresses by President',
              '3. Look for collocations in the inaugural corpus',
              '9. Quit', sep="\n")
        current_input = input('Please enter your selection: ')

        # See list of presidents
        if current_input == '1':
            print('\nList of Presidents:')
            for president in presidents:
                print(president)

        # Lookup addresses for president
        elif current_input == '2':
            selected_president = None

            # Request user input until it matches a value within the president set
            while selected_president not in presidents:
                selected_president = input("Enter president\'s name: ")
                selected_president = selected_president.title()  # Ensures input is title case

            # Find addresses in dictionary matching president input by user
            matching_addresses = []
            matches = [v for (k1, _), v in inaugural_addresses.items() if k1 == selected_president]
            match_details = [(address.president, address.year) for address in matches]

            # Print address years available for provided president along with index for user selection
            for idx, match in enumerate(match_details):
                print(f'Index: {idx}: {match}')
            match_selection = input('Please input index number of desired inaugural address: ')
            selected_address = matches[int(match_selection)]
            selected_address.display_attributes()

        # Lookup collocations in inaugural corpus
        elif current_input == '3':
            input_phrase = ''
            while len(input_phrase) != 2:
                input_phrase = input('Enter two word phrase: ')
                input_phrase = input_phrase.split()
                if len(input_phrase) != 2:
                    print('Incorrect input phrase length. Please try again')
            pmi_score, pmi_statement = calculate_pmi(inaugural_addresses, input_phrase)
            print(f'pmi: {pmi_score}')
            print(pmi_statement)

        # Invalid input
        else:
            print('Please input a valid selection')

    sys.exit('Exiting Program')
