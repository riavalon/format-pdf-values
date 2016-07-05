import csv


with open('quiz_questions.csv', 'r') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    questions = []

    for row in reader:
        qdict = {}
        qdict[fields[0]] = row[fields[0]]
        qdict[fields[1]] = row[fields[1]]
        qdict[fields[2]] = row[fields[2]]
        questions.append(qdict)

    print(questions)
