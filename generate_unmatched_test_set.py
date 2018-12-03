import sys, string, random
import json

random.seed(999)

test_file = open(sys.argv[1], 'rb')
out_file = open(sys.argv[2], 'wb')
slot_values = json.load(open(sys.argv[3])) # They are collected from only training set.

slot_relation = {}
for slot in slot_values:
    if '.' in slot:
        head, tail = slot.split('.')
    else:
        head, tail = 'O', slot
    if tail not in slot_relation:
        slot_relation[tail] = [head]
    else:
        slot_relation[tail].append(head)
for key in slot_relation.keys():
    if len(slot_relation[key]) == 1:
        del slot_relation[key]

diff_slot_values = {}
for tail in slot_relation:
    all_values = set()
    for head in slot_relation[tail]:
        if head == 'O':
            slot = tail
        else:
            slot = head+'.'+tail
        all_values |= set(slot_values[slot].keys())
    for head in slot_relation[tail]:
        if head == 'O':
            slot = tail
        else:
            slot = head+'.'+tail
        my_values = set(slot_values[slot].keys())
        diff_values = all_values - my_values
        diff_slot_values[slot] = diff_values

data = []
slot_values = {}
sentence = []
for line in test_file:
    word_slot_seq, intents = line.strip().split(' <=> ')
    sentence = [item.split(':') for item in word_slot_seq.split(' ')]
    sentence = [['BOS', 'O']] + sentence + [['EOS', 'O']]
    chunks = [intents]
    start_idx, end_idx = 0, 0
    prevTag, prevType = 'O','O'
    Tag, Type = 'O','O'
    nextTag, nextType = 'O','O'
    for idx in range(1, len(sentence)-1):
        chunkStart, chunkEnd = False, False
        if sentence[idx-1][-1] != 'O':
            prevTag, prevType = sentence[idx-1][-1].split('-')
        else:
            prevTag, prevType = 'O', 'O'
        if sentence[idx][-1] != 'O':
            Tag, Type = sentence[idx][-1].split('-')
        else:
            chunks.append([sentence[idx][0], 'O'])
            Tag, Type = 'O', 'O'
        if sentence[idx+1][-1] != 'O':
            nextTag, nextType = sentence[idx+1][-1].split('-')
        else:
            nextTag, nextType = 'O', 'O'

        if Tag == 'B' or (prevTag == 'O' and Tag == 'I'):
            chunkStart = True
        if Tag != 'O' and prevType != Type:
            chunkStart = True
        if (Tag == 'B' or Tag == 'I') and (nextTag == 'B' or nextTag == 'O'):
            chunkEnd = True
        if Tag != 'O' and Type != nextType:
            chunkEnd = True

        if chunkStart:
            start_idx = idx
        if chunkEnd:
            end_idx = idx
            values = []
            for i in range(start_idx, end_idx+1):
                values.append(sentence[i][0])
            values = ' '.join(values)
            chunks.append(['['+Type+']', values])
            sub_slot = Type.split('.')[-1]
            if '['+sub_slot+']' in slot_values:
                if values not in slot_values['['+sub_slot+']']:
                    slot_values['['+sub_slot+']'][values] = 1
            else:
                slot_values['['+sub_slot+']'] = {values:1}
            start_idx, end_idx = 0, 0
    data.append(chunks)

#print len(data)
#print data[-1]
#print slot_values
idx2la = {}
for pattern in data:
    intents = pattern[0]
    pattern = pattern[1:]
    for i in range(1):
        out_sentence = []
        for word, old_value in pattern:
            if word[0] != '[':
                out_sentence.append(word+':O')
            else:
                slot = word[1:-1]
                if slot in diff_slot_values and len(diff_slot_values[slot]) > 0:
                    new_values = random.choice(list(diff_slot_values[slot]))
                else:
                    new_values = old_value
                new_words = new_values.split(' ')
                out_sentence.append(new_words[0]+':B-'+word[1:-1])
                if 'B-'+word[1:-1] not in idx2la.values():
                    idx2la[len(idx2la)] = 'B-'+word[1:-1]
                for new_word in new_words[1:]:
                    if 'I-'+word[1:-1] not in idx2la.values():
                        idx2la[len(idx2la)] = 'I-'+word[1:-1]
                    out_sentence.append(new_word+':I-'+word[1:-1])
        out_file.write(' '.join(out_sentence)+' <=> '+intents+'\n')
#for key in idx2la:
#    print idx2la[key]
