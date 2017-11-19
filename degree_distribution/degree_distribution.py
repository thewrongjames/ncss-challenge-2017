import csv
import sys


degrees_input = {}
with open('degrees.csv') as degrees_file:
    degrees_reader = csv.DictReader(degrees_file)
    for read_degree in degrees_reader:
        degrees_input[read_degree.get('code')] = read_degree
with open('students.csv') as students_file:
    highest_to_lowest_atar_students = sorted(
        list(csv.DictReader(students_file)),
        key=lambda student: (float(student.get('score')), student.get('name')),
        reverse=True
    )

print(degrees_input)
print()
degrees_output = {}
for key in degrees_input.keys():
    degrees_output[key] = {
        'code': key,
        'name': degrees_input[key].get('name'),
        'institution': degrees_input[key].get('institution'),
        'cutoff': -1,
        'offers': 0,
        'vacancies': 'Y'
    }
    # A degree that starts with no places available would be corrected later.
print(degrees_output)
print()
print(highest_to_lowest_atar_students)


def get_cutoff_and_vacancies(students_and_offers, code, degrees_input):
    cuttoff = -1
    student_count = 0
    for student, offer in students_and_offers:
        if offer == code:
            student_count += 1
            if student.get('score') > int(cuttoff):
                cuttoff = student.get('score')

    has_vacancies = student_count < degrees_input[code].get('places')

    return cuttoff, 'Y' if has_vacancies else 'N'


students_and_offers = []
while highest_to_lowest_atar_students:
    student = highest_to_lowest_atar_students.pop(0)

    preferences = student.get('preferences').split(';')
    offer_given = False

    for preference in preferences:
        if '+' in preference:
            preference, bonus_points = preference.split('+')
        else:
            bonus_points = 0

        degree = degrees_output[preference]
        if degree.get('vacancies') == 'Y':
            students_and_offers.append((student, preference))
            offer_given = preference
        else:
            score = int(student.get('score')) + int(bonus_points)
            if score > 99.95:
                score = 99.95
            if (score > int(degree.get('cutoff'))):
                students_and_offers.append(student, preference)

                for student, offer in students_and_offers:
                    if offer != preference:
                        continue

                    


    if offer_given:
        new_cutoff, new_vacancies = get_cutoff_and_vacancies(
            students_and_offers,
            offer_given,
            degrees_input
        )
        degrees_output[offer_given]['cuttoff'] = new_cutoff
        degrees_output[offer_given]['vacancies'] = new_vacancies


output_students_fieldnames = ['name, score, offer']
output_degree_fieldnames = [
    'code',
    'name',
    'institution',
    'cutoff',
    'offers',
    'vacancies'
]


writer = csv.DictWriter(sys.stdout, fieldnames=['example_one', 'example_two'])
writer.writeheader()
writer.writerow({'example_one': 'this', 'example_two': 'that'})
writer.writerow({'example_one': 'there', 'example_two': 'here'})
