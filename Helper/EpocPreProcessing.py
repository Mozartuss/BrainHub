import re
from os import makedirs
from os.path import sep, basename, exists

import pandas as pd

from Helper import Constants
from Helper.Filter import butter_highpass_filter, butter_lowpass_filter
from Helper.LoadSave import yield_data


def main(path):
    for current_path, file in yield_data(path, "raw", epoc=True):
        s, e = get_first_last_index(file)
        file = file.iloc[s:e, :]
        filtered_file = filter_epoc_file(file)
        '''cut first and last 10 sec '''
        filtered_file = filtered_file.iloc[1280:-1280, :].reset_index(drop=True)
        '''trim file to 60 sec length avoid peaks in file'''
        s, e = trim_file(filtered_file, path)
        minute_file = filtered_file.iloc[s:e].reset_index(drop=True)
        minute_file.columns = Constants.EPOC_CHANNELS
        participant = current_path.split(sep)[-2]
        f = "trial_data_" + re.search(r'\d+', basename(current_path).split("_")[0]).group()
        dp = Constants.SAVE_PATH_RW_EPOC + sep + participant
        if not exists(dp):
            makedirs(dp)
        fp = dp + sep + f + ".csv"
        if not exists(fp):
            minute_file.to_csv(fp, index=False, header=True)
            print("Save", fp)
        else:
            print("Check", fp)


def filter_epoc_file(file):
    file = file.iloc[:, 2:16].sub(4200)  # <- EPOC data is converted from the unsigned 14-bit ADC
    ff = []
    for column in file:
        co_data = file[column].to_numpy()
        nco = butter_highpass_filter(co_data, 4.0, 128, 1)
        nnco = butter_lowpass_filter(nco, 45, 128)
        ff.append(nnco)
    return pd.DataFrame(list(map(list, zip(*ff))))


def get_first_last_index(file):
    li = file.iloc[:, 0].tolist()
    first_0_sample = li.index(0.0)
    last_128_sample = next(i for i in reversed(range(len(li))) if li[i] == 127.0)
    return first_0_sample, last_128_sample + 1


def trim_file(file, path):
    peak = []
    for col in file:
        cod = file[col].to_numpy()
        peaks = [i for i in range(len(cod)) if abs(cod[i]) >= 1000]
        peak.extend(peaks)
    cp = {x: peak.count(x) for x in peak}
    ci = list({k: v for k, v in sorted(cp.items(), key=lambda item: item[1], reverse=True) if v > 10}.keys())
    ci.sort()
    fl = [(ci[i], ci[i + 1]) for i in range(len(ci) - 1) if ci[i + 1] - ci[i] >= 128 * 60]
    if ci:
        if ci[0] >= 128 * 60:
            fl.append((0, ci[0]))
        if len(file) - ci[-1] >= 128 * 60:
            fl.append((ci[-1], len(file)))
    if fl:
        a, b = fl[0]
        hl = int(b / 2)
        a = hl - 128 * 30
        b = hl + 128 * 30
        print(basename(path) + ":", "Find peak free minute!")
    else:
        hl = int(len(file) / 2)
        a = hl - 128 * 30
        b = hl + 128 * 30
        print(basename(path) + ":", "Take the middle minute!")
    return a, b + 1
