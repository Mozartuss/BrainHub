from os import makedirs
from os.path import sep, basename, exists

import numpy
import pandas as pd

from Helper import Constants
from Helper.Filter import butter_highpass_filter, butter_lowpass_filter
from Helper.LoadSave import yield_data


def main(path):
    for current_path, file in yield_data(path, "raw", epoc=True):
        s, e = get_first_last_index(file)
        file = file.iloc[s:e, :]
        filtered_file = filter_epoc_file(file)
        '''cut first an last 10 sec '''
        filtered_file = filtered_file.iloc[1280:-1280, :].reset_index(drop=True)
        s, e = trim_file(file)
        minute_file = filtered_file.iloc[s:e]
        participant = current_path.split(sep)[-2]
        f = basename(current_path).split("_")[0] + "_new"
        dp = Constants.SAVE_PATH_RW_EPOC + sep + participant
        if not exists(dp):
            makedirs(dp)
        fp = dp + sep + f + ".csv"
        if not exists(fp):
            filtered_file.to_csv(fp, index=False, header=False)
            print("Save", fp)
        else:
            print("Check", fp)

def filter_epoc_file(file):
    file = file.iloc[:, 2:16].sub(4200)  # <- EPOC data is converted from the unsigned 14-bit ADC
    ff = []
    for column in file:
        co = file[column]
        co_data = co.to_numpy()
        nco = butter_highpass_filter(co_data, 4.0, 128, 1)
        nnco = butter_lowpass_filter(nco, 45, 128)
        ff.append(nnco)
    return pd.DataFrame(list(map(list, zip(*ff))))


def get_first_last_index(file):
    li = file.iloc[:, 0].tolist()
    first_0_sample = li.index(0.0)
    last_128_sample = next(i for i in reversed(range(len(li))) if li[i] == 127.0)
    return first_0_sample, last_128_sample + 1


def trim_file(file):
    fl = []
    peak = []
    for col in file:
        co = file[col]
        cod = co.to_numpy()
        peaks = [i for i in range(len(cod)) if cod[i] >= 650]
        peak.extend(peaks)
    di = {x: peak.count(x) for x in peak}
    ch = list({k: v for k, v in sorted(di.items(), key=lambda item: item[1], reverse=True) if v > 7}.keys())
    ch.sort()
    for i in range(len(ch) - 1):
        if ch[i + 1] - ch[i] >= 128 * 60:
            fl.append((ch[i], ch[i + 1]))
    if ch:
        if ch[0] >= 128 * 60:
            fl.append((0, ch[0]))
        if len(file) - ch[-1] >= 128 * 60:
            fl.append((ch[-1], len(file)))
    if fl:
        a, b = fl[0]
    else:
        hl = int(len(file) / 2)
        a = hl - 182 * 30
        b = hl + 182 * 30
        
    return a, b


if __name__ == '__main__':
    main("/home/mo7art/PycharmProjects/belfast_projekt_2019/epoc_data")
