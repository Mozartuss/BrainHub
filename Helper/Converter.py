import os

import numpy
import pandas as pd

from Helper.Filter import butter_bandpass_filter
from Helper.LoadSave import save, yield_data


def convert_deap_to_csv(filename, data, ids, data_type, dest_path, c_mode=None):
    """
    Convert the deap-matlab-data into trial separated trial csv data and save the file into given destination
    :param filename: the filename of the different files to convert
    :param data: the list data
    :param ids: the csv list headers
    :param data_type: type of data (save as trial_"data_type"_...csv)
    :param dest_path: the store path
    :param c_mode: optional: avg as average
    :return: None
    """
    trials_counter = 1
    for trials in data:
        trial = []
        counter = 0
        for channels in trials[:32]:
            if type(channels) == numpy.float64:
                channel = [ids[counter], channels]
            else:
                if c_mode == "avg":
                    '''
                    Calculates the time average of the data per second
                    '''
                    ch = channels[384:]
                    channel = [sum(ch[sec:sec + 128]) / 128 for sec in range(0, len(ch), 128)]
                else:
                    channel = list(channels[384:])
                    channel.insert(0, ids[counter])
            counter += 1
            trial.append(channel)
        '''
        save the List vertically
        '''
        data_list = list(map(list, zip(*trial)))

        save(trials_counter, data_list, dest_path, filename.split('.')[0], data_type)

        trials_counter += 1


def separate_freqs(data, t, a, b, g, freq, order):
    sol = []
    for column in data:
        co = data[column]
        co_name = co.name
        co_data = co.to_numpy()

        theta = list(butter_bandpass_filter(co_data, t[0], t[1], freq, order))
        theta.insert(0, str(co_name) + "_Theta")
        alpha = list(butter_bandpass_filter(co_data, a[0], a[1], freq, order))
        alpha.insert(0, str(co_name) + "_Alpha")
        beta = list(butter_bandpass_filter(co_data, b[0], b[1], freq, order))
        beta.insert(0, str(co_name) + "_Beta")
        gamma = list(butter_bandpass_filter(co_data, g[0], g[1], freq, order))
        gamma.insert(0, str(co_name) + "_Gamma")
        sol.extend((theta, alpha, beta, gamma))

    f_sol = pd.DataFrame(list(map(list, zip(*sol))))
    f_sol_h = f_sol.iloc[0]
    f_sol = f_sol[1:]
    f_sol.columns = f_sol_h
    return f_sol


def label_to_NNLabel(load_path, save_path, t):
    label_list = []

    if t == "arousal":
        for filename, file in yield_data(load_path, 'label'):
            file.loc[(file.arousal >= 0) & (file.arousal < 2), 'arousal'] = 0  # Very LOW
            file.loc[(file.arousal >= 2) & (file.arousal < 5), 'arousal'] = 1  # LOW
            file.loc[(file.arousal >= 5) & (file.arousal < 8), 'arousal'] = 2  # HIGH
            file.loc[(file.arousal >= 8) & (file.arousal <= 10), 'arousal'] = 3  # Very HIGH

            label_list.append(int(file['arousal'][0]))
    else:
        for filename, file in yield_data(load_path, 'label'):
            file.loc[(file.valence >= 0) & (file.valence < 2), 'valence'] = 0  # Very LOW
            file.loc[(file.valence >= 2) & (file.valence < 5), 'valence'] = 1  # LOW
            file.loc[(file.valence >= 5) & (file.valence < 8), 'valence'] = 2  # HIGH
            file.loc[(file.valence >= 8) & (file.valence <= 10), 'valence'] = 3  # Very HIGH

            label_list.append(int(file['valence'][0]))

    if not os.path.exists(os.path.sep.join(save_path.split('/')[:-1])):
        os.makedirs(os.path.sep.join(save_path.split('/')[:-1]))
    labels = pd.DataFrame(label_list)
    labels.to_csv(save_path, index=False, header=False)
