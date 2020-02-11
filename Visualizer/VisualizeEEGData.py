import Constants
import mne
import numpy as np
import pandas as pd

n_channels = len(Constants.CHANNELS)
info = mne.create_info(ch_names=Constants.CHANNELS, sfreq=Constants.SAMPLE_RATE, ch_types=Constants.CHANNEL_TYPES)
ru = Constants.RECORDING_UNITS
a = pd.read_csv(Constants.CSV_PATH).to_numpy()
if Constants.ShapeType:
    b = np.swapaxes(a, 0, 1)
    data = np.divide(b, ru)
else:
    data = np.divide(a, ru)

f = mne.io.RawArray(data, info)
f.plot()
