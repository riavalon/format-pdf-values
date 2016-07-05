import csv
import re
import os

from tika import parser


if not os.path.exists('questions.txt'):
    parsed = parser.from_file('sample.pdf')
    data = parsed['content']
    contents = data.partition('Page 8 of 9')[0]
    with open('questions.txt', 'wb') as f:
        f.write(str.encode(contents))

if not os.path.exists('data.txt'):
    parsed = parser.from_file('sample.pdf')
    data = parsed['content']
    contents = data.partition('Page 8 of 9')[2]
    with open('data.txt', 'wb') as f:
        f.write(str.encode(contents))

question_pattern = re.compile('^\d+', flags=re.I)


def testing():
    questions_text = []
    quiz_keys = []
    with open('questions.txt', 'r') as f:
        for line in f.readlines():
            if line != '\n':
                questions_text.append(line)
        questions_text = ''.join(questions_text)

        questions = []
        for i in range(1, 46):
            try:
                idx1 = questions_text.index('Question {}'.format(i))
                idx2 = questions_text.index('Question {}'.format(i+1))
                questions.append(questions_text[idx1:idx2])
            except ValueError:
                idx = questions_text.index('Question {}'.format(i))
                questions.append(questions_text[idx:])
        # import pdb; pdb.set_trace()

    with open('data.txt', 'r') as f:
        for line in f.readlines():
            if 'persuade' in line.lower():
                HEADERS = line.strip().lower().split(' ')

            match = question_pattern.match(line)
            if match:
                quiz_keys.append(dict(
                    question_num=match.group(),
                    line=line, ))

    fdata = format_values(quiz_keys)
    for k, v in enumerate(fdata):
        fdata[k] = v[1:-1]

    objects = []
    for item in questions:
        items = item.splitlines()
        pattern = re.compile('\d+')
        q = {
            'question_num': pattern.search(items[0]).group(),
            'a': items[1][3:],
            'b': items[2][3:],
        }
        objects.append(q)


    if not os.path.exists('quiz_questions.csv'):
        # create CSV
        with open('quiz_questions.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=objects[0].keys())
            writer.writeheader()
            writer.writerows(objects)

    answer_key = []
    for k, v in enumerate(fdata):
        # import pdb; pdb.set_trace()
        answer = {
            'q_num': k + 1,
            'a_value': HEADERS[v.index('A')],
            'b_value': HEADERS[v.index('B')],
        }
        answer_key.append(answer)

    if not os.path.exists('answer_key.csv'):
        with open('answer_key.csv', 'w') as f:
            import pdb; pdb.set_trace()
            fieldnames = ['q_num', 'a_value', 'b_value']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(answer_key)

    return objects, answer_key


def format_values(arr):
    fquestions = []
    for question in arr:
        text = question['line'].strip('\n')
        match = question_pattern.match(text)
        if match:
            text = remove_one_space(text.replace(match.group(), ''))
        fquestions.append(text)

    return fquestions


def remove_one_space(string):
    pattern = re.compile('\w(\s+)\w')
    match = pattern.search(string)
    if match:
        start, end = match.start(), match.end()
        count = len(string[start+1:end-1])
        newstring = string[:start+1] + " " * (count-1) + string[end-1:]
        return newstring
    return string

testing()
