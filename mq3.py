import math
import time
from machine import ADC, Pin

class MQ3(object):
    """ Class for dealing with MQ3 Gas Sensors """
    # The load resistance on the board
    RLOAD = 10000 # 10.0
    # Calibration resistance at atmospheric CO2 level
    RZERO = 800 #76.63 #
    # Parameters for calculating ppm of CO2 from sensor resistance
    PARA = 0.3934
    PARB = -1.504 #2.769034857

    # Atmospheric CO2 level for calibration purposes
    ATMOACOHOL = 60 #397.13


    def __init__(self, pin):
        self.pin = pin

    
    def get_resistance(self):
        """Returns the resistance of the sensor in kOhms // -1 if not value got in pin"""
        adc = ADC(self.pin)
        adc.atten(ADC.ATTN_11DB)
        adc.width(ADC.WIDTH_12BIT)
        value = adc.read()
        #print('ADC value: ', value)
        # if value == 0:
        #     return -1
        if value < 1:
            return 1
        elif value >= 4000:
            return 4000
        
        volt_sensor = (value / 4095) * 3.3
        return (3.3 * self.RLOAD / volt_sensor) - self.RLOAD

    
    def get_ppm(self):
        """Returns the ppm of CO2 sensed (assuming only CO2 in the air)"""
        #print(self.get_resistance(), self.RZERO, -self.PARB)
        ratio = self.get_resistance() / 800
        x = 0.3934 * ratio
        return ratio * PARA + PARB
  

    def get_acohol(self):
        """Returns the resistance RZero of the sensor (in kOhms) for calibration purposes
        corrected for temperature/humidity"""
        ratio = self.get_resistance() / 800
        x = 0.3934 * ratio
        return math.pow(x,-1.504)


