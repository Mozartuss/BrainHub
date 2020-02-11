from scipy.signal import butter, lfilter


def butter_bandpass_filter(data, lowcut, highcut, freq, order=5, bt='bandpass'):
    nyq = freq * 0.5
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype=bt)
    return lfilter(b, a, data)

def butter_lowpass_filter(data, lowcut, freq, order=5):
    nyq = freq * 0.5
    low = lowcut / nyq
    b, a = butter(order, low, btype='lowpass')
    return lfilter(b, a, data)

def butter_highpass_filter(data, lowcut, freq, order=5):
    nyq = freq * 0.5
    low = lowcut / nyq
    b, a = butter(order, low, btype='highpass')
    return lfilter(b, a, data)