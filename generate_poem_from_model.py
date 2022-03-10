# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 01:23:33 2022

@author: MIKLOS
"""

import pickle
import numpy as np
from textblob import TextBlob


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


def generate_with_rhyme(poem_line_num, num_of_syllables=8):
    for i in range(poem_line_num):  # generate poem_line_num lines
        if i % 2 == 0:
            print("")
        is_num_syllables = False
        is_ryme = False
        condition = is_num_syllables and is_ryme
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
                poem.append(line)
            elif vowel_counter(sentence) == num_of_syllables and len(poem) % 2 == 1:
                if line[-2:] == poem[len(poem) - 1][-2:]:
                    poem.append(line)
                    is_num_syllables = True
                    is_ryme = True
            condition = is_num_syllables and is_ryme
        for line in poem:
            print(line)


if __name__ == "__main__":
    with open("ady_attila.pickle", "rb") as handle:
        data = pickle.load(handle)
    initial = {}  # start of a phrase
    first_order = {}  # second word only, like the A matrix
    second_order = {}

    initial, first_order, second_order = data
    ### INNEN JÖN A GENERÁLÁS RÉSZ
    # generate(8)
    generate_with_rhyme(8)
