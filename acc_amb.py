spaces = {',','…','.','"','-','(',')','!','?',':',';','_','%','/','$','№','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','v','w','x','y','z'}

output_list = [[''] * 2 for i in range(124000)]
test_list = [[''] * 2 for i in range(124000)]
big_list = [[''] * 2 for i in range(1294000)]

#FILLING THE LISTS

file = open('output_conll_file', 'r')
i = 0
tmp = []
for line in file:
	if line.startswith('#') or line == '\n': continue
	tmp = line.split('\t')
	if '.' in tmp[0]: continue
	output_list[i] = tmp
	i += 1
file.close()

file = open('ru_syntagrus-um-test.conllu', 'r')
i = 0
tmp = []
for line in file:
	if line.startswith('#') or line == '\n': continue
	tmp = line.split('\t')
	if '.' in tmp[0]: continue
	test_list[i] = tmp
	big_list[i][0] = tmp[1]
	big_list[i][1] = tmp[2]
	i += 1
file.close()

file = open('ru_syntagrus-um-dev.conllu', 'r')
j = i + 1
for line in file:
	if line.startswith('#') or line == '\n': continue
	tmp = line.split('\t')
	big_list[j][0] = tmp[1]
	big_list[j][1] = tmp[2]
	j += 1
file.close()

file = open('ru_syntagrus-um-train.conllu', 'r')
for line in file:
	if line.startswith('#') or line == '\n': continue
	tmp = line.split('\t')
	big_list[j][0] = tmp[1]
	big_list[j][1] = tmp[2]
	j += 1
file.close()

f = open('big_list','w')
for k in range(j):
	f.write(big_list[k][0] + ' ' + big_list[k][1] + '\n')

f = open('lists','w')
for k in range(i):
	f.write(output_list[k][1] + ' ' + output_list[k][2] + '	' + test_list[k][1] + ' ' + test_list[k][2] + '\n')

#FILTRATING
for k in range(i):
	count_spaces = 0
	count_letters = 0
	for m in range(len(output_list[k][1])):
		if output_list[k][1][m] in spaces:
			count_spaces += 1
		count_letters +=1
	if count_letters == count_spaces:
		output_list[k][1] = '0'
		output_list[k][2] = '0'
		test_list[k][1] = '0'
		test_list[k][2] = '0'

for k in range(j):
	count_spaces = 0
	count_letters = 0
	for m in range(len(big_list[k][0])):
		if big_list[k][0][m] in spaces:
			count_spaces += 1
		count_letters +=1
	if count_letters == count_spaces:
		big_list[k][0] = '0'
		big_list[k][1] = '0'
	else:
		big_list[k][0] = big_list[k][0].lower()
		big_list[k][1] = big_list[k][1].lower()
f = open('filtrated','w')
for k in range(i):
        f.write(output_list[k][1] + ' ' + output_list[k][2] + ' ' + test_list[k][1] + ' ' + test_list[k][2] + '\n')
f = open('big_list_filtrated','w')
for k in range(j):
        f.write(big_list[k][0] + ' ' + big_list[k][1] + '\n')

#CREATING AMB WORDS SET

import collections
from collections import defaultdict
amb_words = defaultdict(set)
for k in range(j):
	amb_words[big_list[k][0]].add(big_list[k][1])


for key in set(amb_words):
	if len(amb_words[key]) == 1:
		del amb_words[key]

f = open('amb_words','w')
for key in amb_words:
	f.write(key + '\n')


#COMPARING
correct = 0
all = 0
for k in range(i):
	if output_list[k][1] != '0':
		if output_list[k][1].lower() in amb_words:
			if output_list[k][2].lower() == test_list[k][2].lower():
				correct += 1
			all += 1
print(correct/all)
