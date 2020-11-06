import re

f = open('recognised_text.txt', 'r')
f1 = open('resources/text_of_test.txt', 'r')
content = f.read()
content1 = f1.read()

content = re.sub("[^a-zA-Z' ]+", '', content)
content1 = re.sub("[^a-zA-Z'\n ]+", '', content1)
content = content.lower()
content1 = content1.lower()

divider = content1.find('\n')
first_paragraph = content1[:divider]
second_paragraph = content1[divider + 2:]

last_word_of_first = re.finditer(" [^ ]* ", first_paragraph)
indexes_of_last_words = [m.end(0) for m in last_word_of_first]
last_word_of_first = indexes_of_last_words[len(indexes_of_last_words) - 1]
print(last_word_of_first)
word_to_match = first_paragraph[last_word_of_first - 1:]
print(word_to_match)
divider_of_audio_paragraphes = content.find(word_to_match, divider - 40, divider + 40)
if divider_of_audio_paragraphes == - 1:
    print('error')
else:
    divider_of_audio_paragraphes += len(word_to_match) - 1
    print(divider_of_audio_paragraphes)

first_word_of_second = re.finditer(" [^ ]+ ", first_paragraph)
indexes_of_first_words = [m.end(0) for m in first_word_of_second]
word_to_match_again = second_paragraph[:indexes_of_first_words[0] - 1]
print(word_to_match_again)
divider_of_audio_paragraphes2 = content.find(word_to_match_again, divider - 40, divider + 40)
print(divider_of_audio_paragraphes2)

if divider_of_audio_paragraphes2 == divider_of_audio_paragraphes:
    print('YES')
