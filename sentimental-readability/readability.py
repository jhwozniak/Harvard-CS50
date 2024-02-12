# Computes the approximate grade level needed to comprehend some text
from cs50 import get_string

def main():
    text = get_string("Text: ")

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    L = letters / words * 100
    S = sentences / words * 100
    grade = int(0.0588 * L - 0.296 * S - 15.8)

    # Printing results
    if grade < 1:
        print("Before Grade 1\n")
    elif grade >= 16:
        print("Grade 16+\n")
    else:
        print("Grade ", grade)

def count_letters(text):
    letters = 0
    # Splitting text into list of words
    words_list = text.split()
    # Looping over each word, counting length of each word
    for word in words_list:
        letters += len(word)
    return letters

def count_words(text):
    words = 0
    # Splitting text into list of words
    words_list = text.split()
    # Retunrning length of the list
    words = len(words_list)
    return words

def count_sentences(text):
    sentences = 0
    # Splitting text into list of words
    words_list = text.split()
    # Looping over each word, counting length of each word
    for word in words_list:
        # Looping over each character
        for c in word:
            if c == "." or c == "!" or c == "?":
                sentences += 1
    return sentences

main()