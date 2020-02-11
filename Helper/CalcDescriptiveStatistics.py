import os

import numpy
import pandas as pd
from scipy.stats import zscore

from Helper.LoadSave import yield_data


def mean(data):
    return numpy.mean(data)


def standard_deviation(data):
    return numpy.std(data)


def afd(data):
    return numpy.mean(numpy.absolute(numpy.diff(data)))


def norma_afd(data):
    return numpy.mean(zscore(numpy.absolute(numpy.diff(data))))


def asd(data):
    a = numpy.diff(data)
    return numpy.mean(numpy.absolute(numpy.diff(a)))


def norma_asd(data):
    a = numpy.diff(data)
    return numpy.mean(zscore(numpy.absolute(numpy.diff(a))))


def calculation(file):
    """
    Get the DataFrame and calculate for ever column the different statistical mean
    :param file: DataFrame 56x7681
    :return: 6 different 56x1 lists for (mean, std, afd, norm_afd, asd, norm_asd)
    """
    m, sd, afd_l, nafd, asd_l, nasd = ([] for _ in range(6))
    for column in file:
        data = file[column].to_numpy()
        m.append(mean(data))
        sd.append(standard_deviation(data))
        afd_l.append(afd(data))
        nafd.append(norma_afd(data))
        asd_l.append(asd(data))
        nasd.append(norma_asd(data))
    return m, sd, afd_l, nafd, asd_l, nasd


def run(load_path, save_path):
    """
    Get (yield) all the different DataFrame from a folder
    and calculate for each file the statistical mean and save it in a csv file

    :param load_path: the folder path to load all the different files
    :param save_path: the folder save path
    :return: none
    """
    m, sd, afd_l, nafd, asd_l, nasd = ([] for _ in range(6))
    for current_path, file in yield_data(load_path, data_type="data"):
        a, b, c, d, e, f = calculation(file)
        m.append(a)
        sd.append(b)
        afd_l.append(c)
        nafd.append(d)
        asd_l.append(e)
        nasd.append(f)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    pd.DataFrame(m).to_csv(save_path + os.path.sep + "mean.csv", index=False, header=False)
    pd.DataFrame(sd).to_csv(save_path + os.path.sep + "std.csv", index=False, header=False)
    pd.DataFrame(afd_l).to_csv(save_path + os.path.sep + "afd.csv", index=False, header=False)
    pd.DataFrame(nafd).to_csv(save_path + os.path.sep + "norm_afd.csv", index=False, header=False)
    pd.DataFrame(asd_l).to_csv(save_path + os.path.sep + "asd.csv", index=False, header=False)
    pd.DataFrame(nasd).to_csv(save_path + os.path.sep + "norm_asd.csv", index=False, header=False)
