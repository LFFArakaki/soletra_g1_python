import numpy as np

def remove_line_break(array):
    for i, x in enumerate(array):
        array[i] = x.strip()
def find_unwanted_letters(alphabet, useful_letters):
    unwanted_letters = []
    for letter in alphabet:
        if letter not in useful_letters:
            unwanted_letters.append(letter)
    return unwanted_letters
def find_unwanted_words(all_words, unwanted_letters):
    unwanted_words = []
    for word in all_words:
        for letter in unwanted_letters:
            if letter in word or len(word) < 4:
                unwanted_words.append(word)
    unwanted_words = list(set(unwanted_words))
    return unwanted_words
def remove_unwanted_words(all_words, unwanted_words):
    placeholder = np.asarray(all_words)
    unwanted_words = np.asarray(unwanted_words)
    mask = ~np.isin(placeholder, unwanted_words)
    return placeholder[mask].tolist()
def find_required_words(filtered_words, required_letter):
    useful_words = []
    for word in filtered_words:
        if required_letter in word:
            useful_words.append(word)
    return useful_words