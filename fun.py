import numpy as np
import pandas as pd

def compare(comparing, comparing_to):
    if isinstance(comparing[0], str) == 1:
        x = "nan"

    else:
        storage = []
        for i in range(0, len(comparing)):
            if comparing[i] == comparing_to[i]:
                storage.append(1)
            else:
                storage.append(0)
        if sum(storage) > 0:
            x = (sum(storage) / len(storage))
        else:
            x = 0

    return x


def condorcet_compare(comparing, comparing_to):
    storage = []
    storage_condorcet = []

    if isinstance(comparing[0], str) == 1:
        x = "nan"

    else:
        for i in range(0, len(comparing)):
            if comparing[i] == [0]:
                storage.append(0)

            elif comparing[i] == comparing_to[i]:
                storage.append(1)
            else:
                storage.append(0)

        for ii in range(0, len(comparing_to)):
            if comparing_to[ii][0] > 0:
                storage_condorcet.append(1)
            else:
                storage_condorcet.append(0)

        if sum(storage) > 0:
            x = (sum(storage)/sum(storage_condorcet))
        else:
            x = 0

    return x


def condorcet_compare_proportion(comparing, comparing_to):
    storage = []
    storage_condorcet = []

    if isinstance(comparing[0], str) == 1:
        x = "nan"

    else:
        for i in range(0, len(comparing)):
            for ii in range(0, len(comparing[i])):
                if comparing[i][ii] == 0:
                    storage.append(0)
                elif comparing[i][ii] == comparing_to[i][0]:
                    storage.append(1/len(comparing[i]))
                else:
                    storage.append(0)

        for ii in range(0, len(comparing_to)):
            if comparing_to[ii][0] > 0:
                storage_condorcet.append(1)
            else:
                storage_condorcet.append(0)

        if sum(storage) > 0:
            x = (sum(storage)/sum(storage_condorcet))
        else:
            x = 0

    return x


def condorcet_compare_within_list(comparing, comparing_to):
    storage = []
    storage_condorcet = []

    if isinstance(comparing[0], str) == 1:
        x = "nan"

    else:
        for i in range(0, len(comparing)):
            for ii in range(0, len(comparing[i])):
                if comparing[i][ii] == 0:
                    storage.append(0)
                elif comparing[i][ii] == comparing_to[i][0]:
                    storage.append(1)
                else:
                    storage.append(0)

        for ii in range(0, len(comparing_to)):
            if comparing_to[ii][0] > 0:
                storage_condorcet.append(1)
            else:
                storage_condorcet.append(0)

        if sum(storage)>0:
            x = (sum(storage)/sum(storage_condorcet))
        else:
            x = 0

    return x


def multiple_winners(input_list):
    x = 0

    if isinstance(input_list[0], str) == 1:
        x = "nan"

    else:
        for i in range(0, len(input_list)):
            if len(input_list[i]) > 1:
                x += 1
            else:
                pass

        if len(input_list) > 0:
            x = x / len(input_list)
        else:
            pass

    return x


def how_often_chosen(input_list, unique_value):
    new_list = []

    if isinstance(input_list[0], str) == 1:
        x = "nan"

    else:
        for i in input_list:
            for ii in range(0, len(i)):
                new_list.append(i[ii])

        x = 0
        for i in new_list:
            if i == unique_value:
                x += 1
            else:
                pass

        try:
            x = x / len(new_list)
        except:
            x = 0

    return x


def average_of_lists(input_lists):
    ar = np.array(input_lists).astype(float)
    x = np.mean(ar, axis=0)
    return list(x)





