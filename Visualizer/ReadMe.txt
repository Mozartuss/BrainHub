With this tool you can visualize your EEG Data if you export this as CSV.

1. Please edit 'Constants.py' and change all the wrong variables.

---[ Variables Discription ]---

    +++ Recording Units +++
    The script accepts only volts as unit, so choose in which unit the data was recorded

    +++ Shape Type ++++++++
    Select in which table form the data is available
    
    ChannelTime:

            Time 1  |   Time 2  |   Time 3
    Ch 1    --      |   --      |   --  
    Ch 2    --      |   --      |   --
    Ch 3    --      |   --      |   --

    TimeChannel:
    
            Ch 1    |   Ch 2    |   Ch 3
    Time 1  --      |   --      |   --
    Time 2  --      |   --      |   --
    Time 3  --      |   --      |   --

    +++ Sample Rate ++++++++
    Sample rate in Hz

    +++ Channels +++++++++++
    List all the CSV Channel

    +++ Channel Types ++++++
    List all the different types of the channel as List (same order as Channels) 
    or if it is only a single type than only this type as String

    Types:
        ecg, bio, stim, eog, misc, seeg, ecog, mag, eeg, ref_meg, grad, emg, hbr, hbo

2. Open IPython and write "%run ./VisualizeEEGData.py"

 Voilà ;)   
