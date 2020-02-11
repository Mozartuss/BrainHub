import csv
import glob
import os
import pickle
import re
from os.path import sep, basename, exists

import pandas as pd


def natural_sort(in_list):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(in_list, key=alphanum_key)


def yield_data(folder, data_type='trial', deap=False, epoc=False):
    filenames = None
    folders = None
    if exists(folder):
        folders, filenames = next(os.walk(folder))[1:]
    else:
        print("Folder dosn't exist")
        exit(0)
    filenames = natural_sort(filenames)
    folders = natural_sort(folders)

    if deap:
        if len(filenames) >= 1:
            for file in filenames:
                if file.endswith('.dat'):
                    with open((folder + sep + file), 'rb') as f:
                        print('Load ' + str(file))
                        yield file, pickle.load(f, encoding="latin1")
                elif file.endswith('.csv'):
                    print('Load ' + str(file))
                    yield file, pd.read_csv(file)

    elif epoc:
        for participant in folders:
            for path in glob.glob(folder + sep + participant + sep + "T*.csv"):
                if data_type.lower() == "bp":
                    if "".join(basename(path).split(".")[:-1]).endswith(data_type.lower()):
                        print("Load:", basename(path))
                        yield path, pd.read_csv(path).iloc[:, 1:-14]
                elif data_type.lower() == "raw":
                    if not "".join(basename(path).split(".")[:-1]).endswith("bp") and not "".join(
                            basename(path).split(".")[:-1]).endswith("md") and not "".join(
                        basename(path).split(".")[:-1]).endswith("pm"):
                        print("Load:", basename(path))
                        yield path, pd.read_csv(path, skiprows=1)

    else:
        for participant in folders:
            trials = natural_sort(
                [path for path in glob.glob(folder + sep + participant + sep + 'trial_*.csv')
                 if basename(path).startswith('trial_{}'.format(data_type.lower()))])
            for trial in trials:
                print("Load " + basename(trial))
                yield trial, pd.read_csv(trial)
            print("Finish loading data from {} participant".format(participant))
    print("Load all Data")


def save(trial_counter, trial_data, dest_path, participant_folder='', data_type=''):
    """
    :param trial_counter: the number of the trial to save
    :param trial_data: The data to be saved as a list, where the first line contains the labels and then the other lines
     contain the data of the individual labels sorted by time
    :param dest_path: The complete destination folder path
    :param participant_folder: the individual participant folder names
    :param data_type: type of data
    :return: saved as [dest_folder//participant_folder//trial_"data_type"_trial_counter.csv]
    and print path to verification
    """
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    if len(data_type) > 1:
        data_type += '_'

    if len(participant_folder) > 1:
        p_path = dest_path + os.path.sep + participant_folder
        if not os.path.exists(p_path):
            os.mkdir(p_path)
        trial_folder = p_path
    else:
        trial_folder = dest_path
    if not os.path.exists(trial_folder):
        os.mkdir(trial_folder)

    path = (trial_folder + os.path.sep + 'trial_' + data_type + str(trial_counter) + '.csv')
    if not os.path.exists(path):
        with open(path, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(trial_data)
        print('Save', path)
    else:
        print('check', path)
