
spaces = {',','…','.','"','-','(',')','!','?',':',';','_','%','/','$','№','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','v','w','x','y','z'}
output_list = [[''] * 2 for i in range(124000)]
test_list = [[''] * 2 for i in range(124000)]

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
	i += 1
file.close()

#FILTRATING
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

f = open('filtrated','w')
for k in range(i):
        f.write(output_list[k][1] + ' ' + output_list[k][2] + ' ' + test_list[k][1] + ' ' + test_list[k][2] + '\n')

#COMPARING
correct = 0
all = 0
f = open('mistakes','w')
for k in range(i):
	if output_list[k][2] != '0':
		if output_list[k][2].lower() == test_list[k][2].lower():
			correct += 1
		else:
			f.write(output_list[k][2]+'	'+ output_list[k][2].lower()+'	'+ test_list[k][2].lower()+'\n')
		all += 1
print(correct/all)
