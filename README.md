# This service is hosted on the url 

http://turingmachines.eastasia.cloudapp.azure.com:5000/

# Dashboard Link

https://public.tableau.com/profile/anubhav.pandey7854#!/vizhome/TestEmotionTrack/EmotionTrackPg1

# Rakuten Prediction pipeline Local 

This will deal with face emotions and gender at different timeframes

## Installation

Create a venv first

```bash
git clone https://github.com/NavjotBansal/Rakuten_Prediction_Pipeline.git
git checkout vedant/rakuten 
python3 -m venv rakutenvenv
source rakutenvenv/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=application.py
python3 application.py
```

## Output File 

Output is saved in Emotion_Data.csv, Participant_Data.csv, Meeting_Data.csv and output.mp4. 
