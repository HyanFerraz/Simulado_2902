from typing import Dict
import numpy as np 

def create_hsv_filter(lower_filter, upper_filter): 
    lower_hsv = np.array(lower_filter)
    upper_hsv = np.array(upper_filter)

    return {
        "lower": lower_hsv, 
        "upper": upper_hsv
    }