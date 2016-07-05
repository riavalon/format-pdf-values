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
        return questions

    with open('data.txt', 'r') as f:
        for line in f.readlines():
            if 'persuade' in line.lower():
                HEADERS = line.strip().split(' ')

            match = question_pattern.match(line)
            if match:
                quiz_keys.append(dict(
                    question_num=match.group(),
                    line=line, ))

    fdata = format_values(quiz_keys)
    for k, v in enumerate(fdata):
        fdata[k] = v[1:-1]

    # {
    #     'question_text': 'some text',
    #     'question_num': 2,
    #     'answers': {
    #         'a': 'Persuade',
    #         'b': 'Collaborate'
    #     }
    # }

    # questions = []
    # for item in fdata:



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
