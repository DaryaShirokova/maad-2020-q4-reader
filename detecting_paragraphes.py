import re
import contextlib
import wave


def unpack(path_to):
    file_with_text = open(path_to, 'r')
    content = file_with_text.read()
    return content


def cleaning_text(text):
    text = re.sub("[^a-zA-Z' \n]+", '', text)
    text = text.lower()
    return text


def find_words(text):
    word = re.finditer("[^ ]* ", text)
    indexes = [m.end(0) for m in word]
    return indexes


def last_word(indexes, text):
    last_word_of_first = indexes[len(indexes) - 1]
    last_to_match = text[last_word_of_first:]
    last_to_match = ' ' + last_to_match + ' '
    return last_to_match


def first_word(indexes, text):
    if len(indexes) > 1:
        first_to_match = text[:indexes[1] - 1]
        first_to_match = first_to_match + ' '
    else:
        first_to_match = text
    return first_to_match


# unpacking the files
recognised_content = unpack('recognised_text1.txt')
initial_content = unpack('resources/text_of_test1.txt')
length_initial = len(initial_content)

count = 0
punct = []
for el in initial_content:
    if el in ('!', ",", "\'", ";", "\"", ".", "-", "?", ":"):
        count += 1
    punct.append(count)

initial_dividers = [divider.start() for divider in re.finditer(r'\n\n', initial_content)]
# deleting punctuation from the files and removing capital letters
recognised_content = cleaning_text(recognised_content)
initial_content = cleaning_text(initial_content)


recognised_dividers = []
dividers = [divider.start() for divider in re.finditer(r'\n\n', initial_content)]
# now we have a list of dividers
# thus, we know the potential indexes of dividers in recognised text


what = 0
good = 0  # for test
bad = 0
ok = 0


epsilon = 52
# let's find actual dividers in recognised text
for index, divider in enumerate(dividers):
    if index == 0:
        first_paragraph = initial_content[:divider]
        second_paragraph = initial_content[divider + 2:dividers[index + 1]]
    elif index == len(dividers) - 1:
        first_paragraph = initial_content[dividers[index - 1]:divider]
        second_paragraph = initial_content[divider + 2:]
    else:
        first_paragraph = initial_content[dividers[index - 1]:divider]
        second_paragraph = initial_content[divider + 2:dividers[index + 1]]
    # we have just divided our text into paragraphs

    indexes_of_last_words = find_words(first_paragraph)
    # got the indexes of words in first paragraph
    last_word_to_match = last_word(indexes_of_last_words, first_paragraph)
    # got the last word before divider
    first_divider_of_audio_paragraphs = recognised_content.find(last_word_to_match,
                                                                divider - epsilon,
                                                                divider + epsilon)
    # got the first potential divider in recognised text

    #print(last_word_to_match)

    if first_divider_of_audio_paragraphs == - 1:
        pass
        # raise ValueError('There are no matches')
        # print('oops')  # just for test :)
    else:
        pass
        first_divider_of_audio_paragraphs += len(last_word_to_match)
        # print(first_divider_of_audio_paragraphs)

    indexes_of_first_words = find_words(second_paragraph)
    # got the indexes of words in second paragraph
    first_word_to_match = first_word(indexes_of_first_words, second_paragraph)
    # got the first word before divider
    last_divider_of_audio_paragraphs = recognised_content.find(first_word_to_match,
                                                               divider - epsilon,
                                                               divider + epsilon)
    # got the second potential divider in recognised text

    #print(first_word_to_match)

    if last_divider_of_audio_paragraphs == - 1:
        pass
        # raise ValueError('There are no matches')
        # print('oops')  # just for test :)
    else:
        pass
        # print(last_divider_of_audio_paragraphs)

    if first_divider_of_audio_paragraphs == -1 and last_divider_of_audio_paragraphs == -1:
        recognised_dividers.append('ooops')
        what += 1

    elif first_divider_of_audio_paragraphs == -1:
        recognised_dividers.append(last_divider_of_audio_paragraphs + 1)
        ok += 1

    elif last_divider_of_audio_paragraphs == -1:
        recognised_dividers.append(first_divider_of_audio_paragraphs)
        ok += 1

    elif abs(last_divider_of_audio_paragraphs - first_divider_of_audio_paragraphs) < 63:
        recognised_dividers.append(last_divider_of_audio_paragraphs + 1)
        good += 1

    else:
        recognised_dividers.append(last_divider_of_audio_paragraphs + 1)
        bad += 1

"""
print(what)
print(good)
print(bad)
print(ok)
"""
print(*initial_dividers)
print(*recognised_dividers)
for index, el in enumerate(recognised_dividers):
    if (index != 0) & (el == 'ooops'):
        recognised_dividers[index] = dividers[index] + recognised_dividers[index - 1] - dividers[index - 1]
    elif (index != 0) & (el < recognised_dividers[index - 1]):
        recognised_dividers[index] = dividers[index] + recognised_dividers[index - 1] - dividers[index - 1]
    '''
    counter = -1
    memory_index = index
    boo = 0
    while recognised_dividers[memory_index] == 'ooops':
        boo = 1
        counter += 1
        memory_index += 1
    left = index
    right = index + counter
    for ind in range(left, right + 1):
        recognised_dividers[ind] = recognised_dividers[ind - 1] + dividers[ind] - dividers[ind - 1]
    if boo:
        recognised_dividers[:right + 1] = sorted(recognised_dividers[:right + 1])
        '''

#recognised_dividers = sorted(recognised_dividers)

#print(*initial_dividers)
#print(*recognised_dividers)


for index, el in enumerate(recognised_dividers):
    new_file = open("out.txt", "a")
    with open("recognised_text1.txt") as f:

        if index == 0:
            new_file.write(f.read()[:el])
            new_file.write('\n\n')
        else:
            new_file.write(f.read()[recognised_dividers[index - 1]:recognised_dividers[index]])
            new_file.write('\n\n')
    new_file.close()

new_file = open("out.txt", "a")
with open("recognised_text1.txt") as f:
    new_file.write(f.read()[recognised_dividers[-1]:])

new_file.close()

filename = 'resources/direct.wav'

with contextlib.closing(wave.open(filename, 'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = int(frames / float(rate))


real = [81, 169, 239, 264, 273, 276, 288, 291, 301, 331, 336, 394, 421, 438, 439, 441, 445, 448, 451, 487, 493,
        528, 535, 552, 558, 574, 582, 596, 599, 605, 657, 660, 696, 706, 723, 726, 736, 738, 749, 760, 763, 839, 855, 868, 890,
        903, 928, 931, 933, 950, 955, 977, 985, 1005, 1013, 1032, 1049, 1076, 1082, 1098, 1129, 1165, 1168, 1170, 1171, 1174, 1176, 1187, 1190, 1192, 1195, 1197, 1199, 1201, 1203,
        1204, 1207, 1215, 1218, 1222, 1229, 1231, 1233, 1238, 1240, 1241, 1256, 1258, 1260, 1266, 1273, 1278, 1280, 1282,
        1285, 1287, 1307, 1310, 1333, 1336, 1338, 1341, 1349, 1366, 1372, 1377, 1381, 1384, 1387, 1389, 1395, 1398, 1403, 1409, 1414, 1418, 1424, 1432, 1434]


res_file = open("timepoints1.txt", "a")

'''
for el, el2, el3, el4 in zip(recognised_dividers, initial_dividers, dividers, real):
    res_file.write(str(el2) + '\t' + str(int((el/len(recognised_content)) * duration)) + '\t' + str(int((el2/length_initial) * duration)) + '\t' + str(int((el3/len(initial_content) * duration))) + '\t' + str(el4) + '\n')

for el, el2, el3, el4 in zip(recognised_dividers, initial_dividers, dividers, real):
    res_file.write(str(el2) + '\t' + str(int((el/len(recognised_content)) * duration))  + '   ' + str(el4) + '\n')

res_file.close()

i = 0
for el, el2, el3, el4 in zip(recognised_dividers, initial_dividers, dividers, real):
    print(i, end=' ')
    #print(el4/(duration * el/len(recognised_content)), end=' ')
    i += 1


i = 1

i = 1
for el, el2, el3, el4 in zip(recognised_dividers, initial_dividers, dividers, real):
    res_file.write('(' + str(el2) + ';' + str(el4) + ')' + ' ')
    i += 1

'''

for el, el2 in zip(recognised_dividers, initial_dividers):
    res_file.write(str(el2) + '\t' + str(int((el/len(recognised_content)) * duration)) + '\n')




