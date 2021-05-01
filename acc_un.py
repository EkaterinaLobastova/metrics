spaces = {',','…','.','"','-','(',')','!','?',':',';','_',' ','%','/','[',']','$','№','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','v','w','x','y','z'}
#FILLING TRAIN WORDS SET
train_set = [[] for i in range(1294000)]

file = open('ru_syntagrus-um-train.conllu', 'r')
tmp = []
n = 0
for line in file:
	if line.startswith('#') or line == '\n': continue
	tmp = line.split('\t')
	train_set[n] = tmp[1]
	n += 1
file.close()

file = open('ru_syntagrus-um-dev.conllu', 'r')
for line in file:
	if line.startswith('#') or line == '\n': continue
	tmp = line.split('\t')
	train_set[n] = tmp[1]
	n += 1
file.close()

#FILLING TEST WORDS SET + LIST

file = open('ru_syntagrus-um-test.conllu', 'r')
test_list = [[''] * 2 for i in range(124000)]
i = 0
m = 0
for line in file:
	if line.startswith('#') or line == '\n': continue
	tmp = line.split('\t')
	if '.' in tmp[0]: continue
	test_list[i] = tmp
	i += 1
	n += 1
file.close()

#FILLING OUTPUT LIST

file = open('output_conll_file', 'r')
output_list = [[''] * 2 for i in range(124000)]
i = 0
tmp = []
for line in file:
	if line.startswith('#') or line == '\n': continue
	tmp = line.split('\t')
	if '.' in tmp[0]: continue
	output_list[i] = tmp
	i += 1
file.close()

f = open('lists','w')
for k in range(i):
	f.write(output_list[k][1] + ' ' + output_list[k][2] + '	' + test_list[k][1] + ' ' + test_list[k][2] + '\n')

#FILTRATING
train_set_set = set()
test_set_set = set()
for k in range(i):
	count_spaces = 0
	count_letters = 0
	for j in range(len(output_list[k][1])):
		if output_list[k][1][j] in spaces:
			count_spaces += 1
		count_letters +=1
	if count_letters == count_spaces:
		output_list[k][1] = '0'
		output_list[k][2] = '0'
		test_list[k][1] = '0'
		test_list[k][2] = '0'
	else:
		output_list[k][1] = output_list[k][1].lower()
		output_list[k][2] = output_list[k][2].lower()
		test_list[k][1] = test_list[k][1].lower()
		test_list[k][2] = test_list[k][2].lower()
		test_set_set.add(test_list[k][1])

for k in range(n):
	count_spaces = 0
	count_letters = 0
	for j in range(len(train_set[k])):
		if train_set[k][j] in spaces:
			count_spaces += 1
		count_letters +=1
	if count_letters == count_spaces:
		train_set[k] = '0'
	else:
		train_set_set.add(train_set[k].lower())

f = open('filtrated','w')
for k in range(i):
	f.write(output_list[k][1] + ' ' + output_list[k][2] + ' ' + test_list[k][1] + ' ' + test_list[k][2] + '\n')

#CREATING UNSEEN WORDS SET
unseen_set = set()
unseen_set = test_set_set.difference(train_set_set)
f = open('unseen','w')
for elem in unseen_set:
	f.write(elem + '\n')

#COMPARING
correct = 0
all = 0
for k in range(i):
	if output_list[k][2] != '0':
		if output_list[k][1] in unseen_set:
			if output_list[k][2].lower() == test_list[k][2].lower():
				correct += 1
			all += 1
print(correct/all)
