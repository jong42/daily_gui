#import requests
from backend import extract_vals_from_dict
from frontend import init_gui, add_fig_to_gui

### handle api_call ###
#api_address = "api.openweathermap.org/data/2.5/forecast?q=Jena,ger&appid=ca3c615c20062c4fed7b25374cb16a77"
#api_result = requests.get(api_address)

#temporary workaround
import json
f = open("/home/jonas/Desktop/forecast.json")
api_result = json.load(f)

# Extract values
timestamps, temps, weather, prec_probs = extract_vals_from_dict(api_result)

# Construct GUI
_VARS = init_gui()
add_fig_to_gui(_VARS, timestamps, temps)

### show GUI
_VARS['window'].read()
_VARS['window'].close()
