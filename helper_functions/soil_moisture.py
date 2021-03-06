# Functions needed to access the data from the capacitive soils moisture sensor

from machine import ADC
from PlantMonitor.helper_functions import c_like_map


def get_soil_moisture(air, water):
    adc = ADC(0)
    adc_raw = adc.read_u16()
    hum = c_like_map(adc_raw, air, water, 0, 100)
    return adc_raw, hum
