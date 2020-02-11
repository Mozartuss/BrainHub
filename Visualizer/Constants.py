"""
Ignore
"""


def enum(**enums):
    return type('Enum', (), enums)


RecordingUnits = enum(NanoVolt=1000000000, MicroVolt=1000000, MilliVolt=1000, Volt=1)

ShapeType = enum(ChannelTime=False, TimeChannel=True)

"""
Edit here
"""
SAMPLE_RATE = 128
SHAPE_TYPE = ShapeType.TimeChannel
RECORDING_UNITS = RecordingUnits.MicroVolt
# CSV_PATH = "/home/mo7art/BrainHub/Converted/Deap/3.Deap_data_channel_extraction/s05/trial_data_18.csv"
# CSV_PATH = "/home/mo7art/BrainHub/Converted/Deap/2.Deap_data_relevant_channels/s05/trial_data_18.csv"
CSV_PATH = "/home/mo7art/BrainHub/Converted/Epoc/4.Epoc_post_processing/P02/T3_new.csv"
# CSV_PATH = "/home/mo7art/BrainHub/Converted/Epoc/T1_bp.csv"
# CHANNELS = ["AF3_Theta", "AF3_Alpha", "AF3_Beta", "AF3_Gamma", "F7_Theta", "F7_Alpha", "F7_Beta", "F7_Gamma","F3_Theta", "F3_Alpha", "F3_Beta", "F3_Gamma", "FC5_Theta", "FC5_Alpha", "FC5_Beta", "FC5_Gamma","T7_Theta", "T7_Alpha", "T7_Beta", "T7_Gamma", "P7_Theta", "P7_Alpha", "P7_Beta", "P7_Gamma", "O1_Theta","O1_Alpha", "O1_Beta", "O1_Gamma", "O2_Theta", "O2_Alpha", "O2_Beta", "O2_Gamma", "P8_Theta", "P8_Alpha","P8_Beta", "P8_Gamma", "T8_Theta", "T8_Alpha", "T8_Beta", "T8_Gamma", "FC6_Theta", "FC6_Alpha", "FC6_Beta","FC6_Gamma", "F4_Theta", "F4_Alpha", "F4_Beta", "F4_Gamma", "F8_Theta", "F8_Alpha", "F8_Beta", "F8_Gamma","AF4_Theta", "AF4_Alpha", "AF4_Beta", "AF4_Gamma"]
CHANNELS = ["AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2", "P8", "T8", "FC6", "F4", "F8", "AF4"]
# CHANNELS = ["COUNTER", "INTERPOLATED", "AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2", "P8", "T8", "FC6", "F4", "F8", "AF4", "RAW_CQ", "GYROX", "GYROY", "MARKER", "MARKER_HARDWARE", "SYNC", "TIME_STAMP_s", "TIME_STAMP_ms", "TimeStamp", "CQ_AF3", "CQ_F7", "CQ_F3", "CQ_FC5", "CQ_T7", "CQ_P7", "CQ_O1", "CQ_O2", "CQ_P8", "CQ_T8", "CQ_FC6", "CQ_F4", "CQ_F8", "CQ_AF4", "CQ_CMS", "CQ_DRL"]
# CHANNELS = ["AF3_THETA","AF3_ALPHA","AF3_LOW_BETA","AF3_HIGH_BETA","AF3_GAMMA","F7_THETA","F7_ALPHA","F7_LOW_BETA","F7_HIGH_BETA","F7_GAMMA","F3_THETA","F3_ALPHA","F3_LOW_BETA","F3_HIGH_BETA","F3_GAMMA","FC5_THETA","FC5_ALPHA","FC5_LOW_BETA","FC5_HIGH_BETA","FC5_GAMMA","T7_THETA","T7_ALPHA","T7_LOW_BETA","T7_HIGH_BETA","T7_GAMMA","P7_THETA","P7_ALPHA","P7_LOW_BETA","P7_HIGH_BETA","P7_GAMMA","O1_THETA","O1_ALPHA","O1_LOW_BETA","O1_HIGH_BETA","O1_GAMMA","O2_THETA","O2_ALPHA","O2_LOW_BETA","O2_HIGH_BETA","O2_GAMMA","P8_THETA","P8_ALPHA","P8_LOW_BETA","P8_HIGH_BETA","P8_GAMMA","T8_THETA","T8_ALPHA","T8_LOW_BETA","T8_HIGH_BETA","T8_GAMMA","FC6_THETA","FC6_ALPHA","FC6_LOW_BETA","FC6_HIGH_BETA","FC6_GAMMA","F4_THETA","F4_ALPHA","F4_LOW_BETA","F4_HIGH_BETA","F4_GAMMA","F8_THETA","F8_ALPHA","F8_LOW_BETA","F8_HIGH_BETA","F8_GAMMA","AF4_THETA","AF4_ALPHA","AF4_LOW_BETA","AF4_HIGH_BETA","AF4_GAMMA"]
CHANNEL_TYPES = "eeg"
