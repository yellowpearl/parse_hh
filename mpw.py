import os
import string
import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
dir_name = 'pm'
spec_chars = string.punctuation + '\n\xa0«»\t—…' + string.digits[:2] + string.digits[3:]
cwd = os.getcwd()

full_path_dir = cwd+f'/{dir_name}'
os.chdir(full_path_dir)

files = os.listdir(full_path_dir)
for filetxt in files:
    file = open(f'{filetxt}', 'r')
    text = file.read()
    text = text.lower()
    text = "".join([ch for ch in text if ch not in spec_chars])
    len_text = len(text)
    text_tokens = word_tokenize(text)
    text = nltk.Text(text_tokens)
    russian_stopwords = stopwords.words("russian")
    filtered_sentence = [w for w in text_tokens if not w in russian_stopwords]
    fdist = FreqDist(filtered_sentence)
    fdist = fdist.most_common(150)
    result = '\n'.join([f'{key.capitalize()}: {value}' for key, value in fdist if len(key) > 2])
    file_n = open(f'ANS_{filetxt}.txt', 'w')
    file_n.write(result)
    file_n.close()
    file.close()
os.chdir(cwd)