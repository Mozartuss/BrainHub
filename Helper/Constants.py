from os.path import sep

EPOC_CHANNELS = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

DEAP_CHANNELS = ['Fp1', 'AF3', 'F3', 'F7', 'FC5', 'FC1', 'C3', 'T7', 'CP5', 'CP1', 'P3', 'P7', 'PO3', 'O1', 'Oz',
                 'Pz', 'Fp2', 'AF4', 'Fz', 'F4', 'F8', 'FC6', 'FC2', 'Cz', 'C4', 'T8', 'CP6', 'CP2', 'P4', 'P8',
                 'PO4', 'O2']

LABEL_CHANNELS = ['valence', 'arousal', 'dominance', 'liking']

SAVE_PATH_CUT_3 = "Converted" + sep + "Deap" + sep + "1.Deap_data_cut_first_3_seconds_csv"
SAVE_PATH_RELEVANT_CHANNELS = "Converted" + sep + "Deap" + sep + "2.Deap_data_relevant_channels"
SAVE_PATH_FREQ_EXT = "Converted" + sep + "Deap" + sep + "3.Deap_data_channel_extraction"

SAVE_PATH_RW_EPOC = "Converted" + sep + "Epoc" + sep + "4.Epoc_post_processing"
