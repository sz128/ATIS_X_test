import sys

file = open(sys.argv[1], 'rb')

for line in file:
    line = line.strip()
    if len(line.split(' <=> ')) == 2:
        ali, unali = line.split(' <=> ')
    else:
        ali, unali = line, None
    new_ali = []
    for item in ali.split(' '):
        word, label = item.split(':')
        if set(word) & set('1234567890') != set([]) and set(word) & set('abcdefghijklmnopqrstuvwxyz') != set([]):
            pass
            #word = "DIGIT_CHARACTER"
        elif word.isdigit() == True:
            word = "DIGIT"*len(word)
        new_ali.append(word+':'+label)
    if unali:
        print ' '.join(new_ali) +' <=> '+unali
    else:
        print ' '.join(new_ali)
