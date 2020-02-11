import os

from Helper import Constants, LoadSave


def get_index_of_deap_labels_contains_epoc():
    index_list = []
    for e in Constants.EPOC_CHANNELS:
        for d in Constants.DEAP_CHANNELS:
            if e is d:
                index_list.append(Constants.DEAP_CHANNELS.index(d))
    return index_list
