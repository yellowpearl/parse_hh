import collections
import os
dir_name = 'backup_cpo/cpo'
c = collections.Counter()

cwd = os.getcwd()
print(cwd)

full_path_dir = cwd+f'/{dir_name}'
os.chdir(full_path_dir)

files = os.listdir(full_path_dir)
print(files)
for filetxt in files:
    print(filetxt)
    file = open(f'{filetxt}', 'r')
    text = file.read()
    text_list = text.split(' ')

    for word in text_list:
        c[word] += 1

    result = '\n'.join([f'{key.capitalize()}: {value}' for key, value in c.most_common() if len(key)>2])

    file_n = open(f'ANS_{filetxt[:-4]}.txt', 'w')
    file_n.write(result)
    file_n.close()
    file.close()
os.chdir(cwd)