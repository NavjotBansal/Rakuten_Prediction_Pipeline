# Rakuten Prediction pipeline

This will deal with face emotions and gender at different timeframes

## Installation

Create a venv first

```bash

python3 -m venv rakutenvenv
source rakutenvenv/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=application.py
python3 application.py
```

## Output File 

Output is saved in output.csv , which is just one meeting inference we need to append all outputs to a new csv
