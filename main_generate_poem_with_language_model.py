# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 17:40:13 2022

@author: MIKLOS
"""


import numpy as np
import string
import pickle

# from striprtf.striprtf import rtf_to_text

# np.random.seed(1234)


def remove_punctuation(s):
    return s.translate(str.maketrans("", "", string.punctuation))


def add2dict(d, k, v):
    if k not in d:
        d[k] = []
    d[k].append(v)


def list2pdict(ts):
    """This function creates a dictionary of counts, then normalizes the ű
    counts to probabilities.
    Aka. turn each list of possibilities into a dictionary of probabilities
    """

    d = {}
    # n total number of sample
    n = len(ts)
    for t in ts:
        # count the tokens
        d[t] = d.get(t, 0.0) + 1
    # loop through each key-value pair and devide the count by the total
    for t, c in d.items():
        d[t] = c / n
    return d


def sample_word(d):
    # print "d:", d
    p0 = np.random.random()
    # print "p0:", p0
    cumulative = 0
    for t, p in d.items():
        cumulative += p
        if p0 < cumulative:
            return t
    assert False  # should never get here


def generate(verse_line_num):
    for i in range(verse_line_num):  # generate 4 lines
        if i % 4 == 0:
            print("")
        sentence = []

        # initial word
        w0 = sample_word(initial)
        sentence.append(w0)

        # sample second word
        w1 = sample_word(first_order[w0])
        sentence.append(w1)

        # second-order transitions until END
        while True:
            w2 = sample_word(second_order[(w0, w1)])
            if w2 == "END":
                break
            sentence.append(w2)
            w0 = w1
            w1 = w2
        print(" ".join(sentence))


def vowel_counter(in_list):
    vowels = "aáeéiíoóöőuúüűAÁEÉIÍOÓÖŐUÚÜŰ"
    count = sum([1 for char in "".join(in_list) if char in vowels])
    return count


def generate_with_rhyme(verse_line_num, num_of_syllables=8):
    for i in range(verse_line_num):  # generate verse_line_num lines
        if i % 2 == 0:
            print("")
        is_num_syllables = False
        is_ryme = False

        condition = is_num_syllables and is_ryme

        # first_sentence = ''
        poem = []

        while not condition:
            sentence = []

            # initial word
            w0 = sample_word(initial)
            if w0 not in first_order:
                while w0 not in first_order:
                    w0 = sample_word(initial)
            sentence.append(w0)

            # sample second word
            w1 = sample_word(first_order[w0])
            sentence.append(w1)

            # second-order transitions until END
            while True:
                w2 = sample_word(second_order[(w0, w1)])
                if w2 == "END":
                    break
                sentence.append(w2)
                if len(sentence) == is_num_syllables:
                    break
                w0 = w1
                w1 = w2
            line = " ".join(sentence)

            if vowel_counter(sentence) == num_of_syllables and len(poem) % 2 == 0:
                is_num_syllables = True
                # print(line)
                poem.append(line)
            elif vowel_counter(sentence) == num_of_syllables and len(poem) % 2 == 1:
                if line[-2:] == poem[len(poem) - 1][-2:]:
                    poem.append(line)
                    is_num_syllables = True
                    is_ryme = True
            condition = is_num_syllables and is_ryme

        for line in poem:
            print(line)


IN_PATH = "./datasets/"

if __name__ == "__main__":

    initial = {}  # start of a phrase
    first_order = {}  # second word only, like the A matrix
    second_order = {}

    filepath = IN_PATH + "ady_attila.txt" # ANCSI coding

    for line in open(filepath):
        tokens = remove_punctuation(line.rstrip().lower()).split()

        T = len(tokens)
        for i in range(T):
            t = tokens[i]
            if i == 0:
                # measure the distribution of the first word
                initial[t] = initial.get(t, 0.0) + 1
            else:
                # previous token in position i-1
                t_1 = tokens[i - 1]
                if i == T - 1:
                    # measure probability of ending the line
                    # fake token
                    add2dict(second_order, (t_1, t), "END")
                if i == 1:
                    # measure distribution of second word
                    # given only first word
                    add2dict(first_order, t_1, t)
                else:
                    # previous token to t-1 in position i-2
                    t_2 = tokens[i - 2]
                    add2dict(second_order, (t_2, t_1), t)
    # normalize the distributions
    initial_total = sum(initial.values())
    for t, c in initial.items():
        initial[t] = c / initial_total
    for t_1, ts in first_order.items():
        # replace list with dictionary of probabilities
        first_order[t_1] = list2pdict(ts)
    for k, ts in second_order.items():
        second_order[k] = list2pdict(ts)

    data = [initial, first_order, second_order]
    with open('ady_attila.pickle', 'wb') as handle:
        pickle.dump(data, handle)

    with open('ady_attila.pickle', 'rb') as handle:
        b = pickle.load(handle)

    # print(data == b)
    ### INNEN JÖN A GENERÁLÁS RÉSZ
    # generate(8)
    generate_with_rhyme(8)
