import hashlib
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_lower(s):
    return s == s.lower()

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def create_attendee():
    clear_console()
    print('These entries are case-sensitive:')
    first_name = ''
    last_name = ''
    while len(first_name) == 0 and len(last_name) == 0:
        first_name = raw_input('First Name: ').strip()
        last_name = raw_input('Last Name: ').strip()
    if is_lower(first_name):
        first_name = first_name.title()
    if is_lower(last_name):
        last_name = last_name.title()
    gender = ''
    while len(gender) == 0:
        clear_console()
        gender = raw_input('Gender (M/F): ').strip().lower()
        if gender not in ['m', 'f']:
            gender = ''
    grade = ''
    while len(grade) == 0:
        clear_console()
        print('Class Grade symbols:')
        print('Cubbies: "cub"')
        print('Kindergarten: "k"')
        print('Use grade number for 1-6')
        print('No class/other: "misc"')
        print('* If two grades combined, use "_" to separate (ex. 1_2)')
        grade = raw_input('Class Grade: ').strip().lower()
        if grade not in ['cub', 'k', '1', '2', '3', '4', '5', '6', 'k_1', '1_2', '2_3', '3_4', '4_5', '5_6', 'misc']:
            grade = ''
    role = ''
    while len(role) == 0:
        clear_console()
        print('Role symbols:')
        print('Student: "s"')
        print('LIT: "lit"')
        print('Teacher: "t"')
        print('Other: "l"')
        role = raw_input('Role: ').strip().lower()
        if role not in ['s', 'lit', 't', 'l']:
            role = ''
    if grade == 'cub':
        gender = 'a'
    designation = grade.title() + '-' + gender.title() + '-' + role.upper()
    gen_role = 'Student'
    if role in ['lit', 't', 'l']:
        gen_role = 'Helper'
    user_hash = hashlib.md5(first_name + '-' + last_name + '-' + designation).hexdigest()
    return first_name, last_name, designation, gen_role, user_hash

def create_attendee_record(api):
    first_name = ''
    last_name = ''
    while len(first_name) == 0 and len(last_name) == 0:
        clear_console()
        full_name = raw_input('Full Name: ')
        first_name = full_name.split(' ')[0].strip()
        last_name = full_name.split(' ')[1].strip()
    matching_attendees = api.return_existing_attendee_info(first_name, last_name)
    attendee_index = -1
    if len(matching_attendees) > 1:
        while attendee_index < 0:
            clear_console()
            index_counter = 0
            for attendee in matching_attendees:
                print('Index: ' + str(index_counter))
                print(attendee['first_name'] + ' ' + attendee['last_name'] + '(G' + attendee['designation'].split('-')[0] + ')')
                print('')
                index_counter += 1
            attendee_index = raw_input('Correct Index Number: ')
            if is_int(attendee_index) and int(attendee_index) < len(matching_attendees) and int(attendee_index) >= 0:
                attendee_index = int(attendee_index)
            else:
                attendee_index = -1
    elif len(matching_attendees) == 1:
        attendee_index = 0
    elif len(matching_attendees) == 0:
        option = ''
        while len(option) == 0:
            option = raw_input('Attendee not found, would you like to create a new attendee? (y/n): ').lower().strip()
            if option not in ['y', 'n']:
                option = ''
        if option == 'y':
            first_name, last_name, designation, gen_role, user_hash = create_attendee()
            api.create_attendee(first_name, last_name, designation)
    sunday_school = None
    if attendee_index >= 0 and matching_attendees[attendee_index]['role'] == 'Student':
        while sunday_school == None:
            sunday_school = raw_input('Sunday School (y/n): ').strip().lower()
            if sunday_school not in ['y', 'n']:
                sunday_school = None
                continue
            sunday_school = sunday_school == 'y'
    if attendee_index >= 0:
        return matching_attendees[attendee_index]['user_hash'], sunday_school
    return False
