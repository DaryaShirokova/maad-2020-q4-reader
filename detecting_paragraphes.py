import re


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
recognised_content = unpack('recognised_text.txt')
initial_content = unpack('resources/text_of_test.txt')


# deleting punctuation from the files and removing capital letters
recognised_content = cleaning_text(recognised_content)
initial_content = cleaning_text(initial_content)


recognised_dividers = []
dividers = [divider.start() for divider in re.finditer('\n\n', initial_content)]
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

    print(last_word_to_match)

    if first_divider_of_audio_paragraphs == - 1:
        pass
        # raise ValueError('There are no matches')
        # print('oops')  # just for test :)
    else:
        pass
        first_divider_of_audio_paragraphs += len(last_word_to_match) - 1
        # print(first_divider_of_audio_paragraphs)

    indexes_of_first_words = find_words(second_paragraph)
    # got the indexes of words in second paragraph
    first_word_to_match = first_word(indexes_of_first_words, second_paragraph)
    # got the first word before divider
    last_divider_of_audio_paragraphs = recognised_content.find(first_word_to_match,
                                                               divider - epsilon,
                                                               divider + epsilon)
    # got the second potential divider in recognised text

    print(first_word_to_match)

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
        recognised_dividers.append(last_divider_of_audio_paragraphs)
        ok += 1

    elif last_divider_of_audio_paragraphs == -1:
        recognised_dividers.append(first_divider_of_audio_paragraphs)
        ok += 1

    elif abs(last_divider_of_audio_paragraphs - first_divider_of_audio_paragraphs) < 63:
        recognised_dividers.append(last_divider_of_audio_paragraphs)
        good += 1

    else:
        bad += 1

"""
print(what)
print(good)
print(bad)
print(ok)
"""

print(*dividers)
print(*recognised_dividers)