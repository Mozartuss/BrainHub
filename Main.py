import os
from os.path import sep, exists

import pandas as pd

from Helper import Constants, Converter
from Helper.Converter import convert_deap_to_csv
from Helper.LoadSave import yield_data


def relevant_channels():
    for filename, file in yield_data(Constants.SAVE_PATH_CUT_3, "data", deap=True):
        new_trial = file.loc[:, Constants.EPOC_CHANNELS]
        participant_folder = filename.split(os.path.sep)[-2]
        dp = Constants.SAVE_PATH_RELEVANT_CHANNELS + os.path.sep + participant_folder
        if not os.path.exists(dp):
            os.makedirs(dp)
        fp = dp + os.path.sep + os.path.basename(
            filename)
        if not os.path.exists(fp):
            new_trial.to_csv(fp, index=False)
            print("Save " + fp)
        else:
            print('Check', fp)


def deap_to_csv(path):
    for filename, file in yield_data(path, deap=True):
        data = file['data']
        labels = file['labels']
        convert_deap_to_csv(filename, data, Constants.DEAP_CHANNELS, 'data', Constants.SAVE_PATH_CUT_3)
        convert_deap_to_csv(filename, labels, Constants.LABEL_CHANNELS, 'label', Constants.SAVE_PATH_CUT_3)


def freq_ext():
    theta_freq = [4, 8]
    alpha_freq = [8, 12]
    beta_freq = [12, 31]
    gamma_freq = [31, 50]
    sampling_rate = 128
    order = 7
    for filename, file in yield_data(Constants.SAVE_PATH_RELEVANT_CHANNELS, "data", deap=True):
        new_trial = Converter.separate_freqs(file, theta_freq, alpha_freq, beta_freq, gamma_freq, sampling_rate, order)
        pf = filename.split(os.path.sep)[-2]
        dp = Constants.SAVE_PATH_FREQ_EXT + os.path.sep + pf
        if not exists(dp):
            os.makedirs(dp)
        fp = dp + sep + os.path.basename(filename)
        if not exists(fp):
            new_trial.to_csv(fp, index=False)
            print("Save " + fp)
        else:
            print('Check', fp)


if __name__ == '__main__':
    '''
    1. Transform deap matlab data into useful trial separated csv data (Each participant has 40 trials and each trial 
    record data for 63 seconds with 128 Hz. -> the first 3 seconds were removed.) 
    '''
    # deap_to_csv("/home/mo7art/PycharmProjects/belfast_projekt_2019/data")

    '''
    2. Only select the relevant channels (Epoc <==> Deap)
    '''
    # relevant_channels()

    '''
    3. Extract the frequencies for each trial () 
    '''
    # freq_ext()

    # new_epoc()

    f = pd.read_csv("/home/mo7art/PycharmProjects/belfast_projekt_2019/epoc_data/P01/T1_2018.12.04_11.17.16.bp.csv",
                    skiprows=1)
    f = f.iloc[:, 1:-14]

    f.to_csv("/home/mo7art/BrainHub/Converted/Epoc/T1_bp.csv", index=False, header=False)
