import math
import sys
sys.stdin.reconfigure(encoding='utf-8')


def read_input():
    """
    Reads input line after line
    :return:
        input as string text
    """
    text = ""
    for line in sys.stdin:
        text += line
    return text


def compute_raw_size(text):
    """
    Calculating raw size of input in MB
    :param text:
        input as a string
    :return:
        float raw_size rounded to four decimal places
    """
    text_without_spaces = ""
    for c in text:
        if c.isspace():
            continue
        text_without_spaces += c
    raw_size = round(len(text_without_spaces.encode('utf-8'))/1024**2, 4)
    return raw_size


def characters_count(text):
    """
    Count frequency of characters (without spaces) in input
    :param text:
        input as a string
    :return:
        characters and their frequency in dictionary
    """
    characters = {}
    # character count
    for c in text:
        if c.isspace():
            continue
        if c in characters:
            characters[c] += 1
        else:
            characters[c] = 1
    return characters


def words_count(text):
    """
    Count frequency of words in input
    :param text:
        input as a string
    :return:
        words and their frequency in dictionary
    """
    words = {}
    for word in text.split():
        if word in words:
            words[word] += 1
        else:
            words[word] = 1
    return words


def print_top_ten(dictionary):
    """
    Sorts dictionary by values
    :return:
        10 most frequent keys
    """
    events = sorted(dictionary.items(), key=lambda item: -item[1])
    for i in range(10):
        print(events[i][1], events[i][0])


def calculate_entropy(dictionary):
    """
    Calculates dictionary entropy
    :return:
        dictionary entropy and total count of elements (without spaces)
    """
    elements_entropy = 0
    total_elements = sum(dictionary.values())
    for value in dictionary.values():
        p = value / total_elements
        elements_entropy += p * math.log2(1 / p)
    return elements_entropy, total_elements


def count_size_of_message_by_entropy(dictionary):
    """
    Count size of message by entropy of dictionary
    :return:
        characters entropy and distinct elements count
    """
    number_of_different_elements = len(dictionary)
    elements_entropy, total_elements = calculate_entropy(dictionary)
    size_of_message_by_entropy = total_elements * elements_entropy
    return size_of_message_by_entropy, number_of_different_elements


def compute_encoding_table_size(dictionary):
    """
    Calculates encoding table size
    :return:
        encoding table size
    """
    encoding_table_size = 0.0
    total_elements = sum(dictionary.values())

    # sum of key sizes plus size of values
    for key in dictionary.keys():
        encoding_table_size +=\
            8 * len(key.encode('utf-8')) +\
            math.log2(total_elements / dictionary[key])
    return encoding_table_size


if __name__ == '__main__':
    text = read_input()
    raw_size = compute_raw_size(text)

    characters = characters_count(text)  # dictionary of all input characters
    # size_ce is size of message calculated by characters entropy
    size_ce, distinct_characters = count_size_of_message_by_entropy(characters)
    characters_entropy, total_characters = calculate_entropy(characters)
    characters_encoding_table_size = compute_encoding_table_size(characters)
    print(raw_size,
          round(size_ce / (8 * 1024**2), 4),
          round(characters_encoding_table_size / (8 * 1024**2), 4))
    print(total_characters, distinct_characters,
          round(characters_entropy, 4))
    print_top_ten(characters)

    print()

    words = words_count(text)  # dictionary od all words from input
    # size_we is size of message calculated by words entropy
    size_we, distinct_words = count_size_of_message_by_entropy(words)
    words_entropy, total_words = calculate_entropy(words)
    words_encoding_table_size = compute_encoding_table_size(words)
    print(raw_size,
          round(size_we / (8 * 1024**2), 4),
          round(words_encoding_table_size / (8 * 1024**2), 4))
    print(total_words,
          distinct_words,
          round(words_entropy, 4))
    print_top_ten(words)

