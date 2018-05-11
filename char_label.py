
with open('./data_ch/Train_set.txt', mode='r', encoding='utf-8') as file:
    cons = file.readlines()

contents = []

for con in cons:
    a = con.split(' ')
    if len(a) != 1:
        b = a[1].split('-')
        if len(b) == 1:
            mark = 'O' + '\n'

        else:
            mark = b[1]

        if len(a[0]) != 1 and len(b) == 2:
            c = 1
            for i in a[0]:
                if b[0] == 'B':
                    if c == 1:
                        marks = 'B-' + mark
                        result = str(i) + "\t" + marks
                        c = 2
                    else:
                        marks = 'I-' + mark
                        result = str(i) + "\t" + marks
                else:
                    marks = 'I-' + mark
                    result = str(i) + "\t" + marks
                print(result)
                contents.append(result)
        elif len(a[0]) != 1 and len(b) == 1:
            for i in a[0]:
                result = str(i) + "\t" + mark
                print(result)
                contents.append(result)
        else:
            contents.append(con)

    else:
        contents.append(con)

with open('./data_ch/Train_set_1.txt', mode='w', encoding='utf-8') as file:
    for content in contents:
        file.write(content)
