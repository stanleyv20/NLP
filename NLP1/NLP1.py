import sys
import pathlib
import re
import pickle

class Person:
    def __init__(self, last, first, middle, p_id, phone):
        self.last_name = last
        self.first_name = first
        self.middle_initial = middle
        self.person_id = p_id
        self.phone_number = phone

    def display(self):
        print(f'Employee id: {self.person_id}')
        print(f'{self.first_name} {self.middle_initial} {self.last_name}')
        print(f'{self.phone_number}')

# Used to process lines from input file
# Returns dictionary of person objects once entries in invalid format are corrected via user input
def process_data(data_list):
    person_dict = {}

    # Format first name, last name, and mid initial
    for line in data_list:
        line_element = line.split(',')
        l_name = line_element[0].capitalize()
        f_name = line_element[1].capitalize()
        if line_element[2]:
            m_initial = line_element[2].upper()
        else:
            m_initial = 'X'
        e_id = line_element[3]

        # Validate ID format using regex, prompts user for input until valid entry detected
        id_pattern = re.compile("[a-zA-Z]{2}[0-9]{4}")
        id_format_match = bool(re.match(id_pattern, e_id.strip()))
        while id_format_match is not True:
            current_input = e_id
            print(f'{current_input} is not valid. ID is two letters followed by 4 digits')
            e_id = input('Please enter a valid id:')
            id_format_match = bool(re.match(id_pattern, e_id.strip()))

        # Validate phone format using regex, prompts user for input until valid entry detected
        phone_format = re.compile("\d{3}-\d{3}-\d{4}")
        office_phone = line_element[4]
        phone_format_match = bool(re.match(phone_format, office_phone.strip()))
        while phone_format_match is not True:
            current_phone = office_phone
            print(f'Phone {current_phone} is invalid')
            print('Enter phone number in form 123-456-7890')
            office_phone = input('Enter valid phone number:')
            phone_format_match = bool(re.match(phone_format, office_phone.strip()))

        # Check for duplicate ID and save person object to dictionary
        if e_id in person_dict:
            print('Duplicate Key Error! An existing value in dictionary will be replaced')
        person_dict[e_id] = (Person(l_name, f_name,m_initial,e_id, office_phone))
    return person_dict

if __name__ == '__main__':

    # Check if sys arg was provided indicating data file path
    if len(sys.argv) < 2:
        sys.exit('Please provide sysarg indicating path of data file!')
    dataFilePath = sys.argv[1]

    # Read file using pathlib to ensure cross platform support
    with open(pathlib.Path.cwd().joinpath(dataFilePath), 'r') as myFile:
        next(myFile) #Skipping header line
        # creating list containing elements for each line and removing newline character
        line_list = [line.rstrip('\n') for line in myFile]

    # Invoke function to process data file
    my_people = process_data(line_list)

    # Serialize person dictionary to pickle file
    pickle.dump(my_people, open('my_pickle', 'wb'))  # writing binary

    # Deserialize from pickle file
    unpickle_people = pickle.load(open('my_pickle', 'rb'))  # reading binary

    # Output dict elements by invoking display method on each employee object
    print('\n\n**************')
    print('Employee list:')
    for person_id in unpickle_people.keys():
        unpickle_people[person_id].display()
