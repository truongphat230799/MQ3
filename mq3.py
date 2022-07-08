import math
import time
from machine import ADC, Pin

class MQ(object):
    """ Class for dealing with MQ Sensors """
    # The load resistance on the board
    RLOAD = 10000 # 10.0
    # Calibration resistance at atmospheric CO2 level
    RZERO = 800 #76.63 #
    # Parameters for calculating ppm of CO2 from sensor resistance
    PARA = 116.6020682
    PARB = 2.8 #2.769034857

    # Parameters to model temperature and humidity dependence
    CORA = 0.00035
    CORB = 0.02718
    CORC = 1.39538
    CORD = 0.0018
    CORE = -0.003333333
    CORF = -0.001923077
    CORG = 1.130128205

    # Atmospheric CO2 level for calibration purposes
    ATMOCO2 = 410 #397.13


    def __init__(self, pin):
        self.pin = pin

    def get_correction_factor(self, temperature, humidity):
        """Calculates the correction factor for ambient air temperature and relative humidity
        Based on the linearization of the temperature dependency curve
        under and above 20 degrees Celsius, asuming a linear dependency on humidity,
        provided by Balk77 https://github.com/GeorgK/MQ135/pull/6/files
        """

        if temperature < 20:
            return self.CORA * temperature * temperature - self.CORB * temperature + self.CORC - (humidity - 33.) * self.CORD

        return self.CORE * temperature + self.CORF * humidity + self.CORG

    def get_resistance(self):
        """Returns the resistance of the sensor in kOhms // -1 if not value got in pin"""
        adc = ADC(self.pin)
        adc.atten(ADC.ATTN_11DB)
        adc.width(ADC.WIDTH_12BIT)
        value = adc.read()
        print('ADC value: ', value)
        # if value == 0:
        #     return -1
        if value < 1:
            return 1
        elif value >= 4000:
            return 4000

        return (4095./value - 1.) * self.RLOAD

    def get_corrected_resistance(self, temperature, humidity):
        """Gets the resistance of the sensor corrected for temperature/humidity"""
        return self.get_resistance()/ self.get_correction_factor(temperature, humidity)

    def get_ppm(self):
        """Returns the ppm of CO2 sensed (assuming only CO2 in the air)"""
        #print(self.get_resistance(), self.RZERO, -self.PARB)
        return round(self.PARA * math.pow((self.get_resistance()/ self.RZERO), -self.PARB))

    def get_corrected_ppm(self, temperature, humidity):
        """Returns the ppm of CO2 sensed (assuming only CO2 in the air)
        corrected for temperature/humidity"""
        return self.PARA * math.pow((self.get_corrected_resistance(temperature, humidity)/ self.RZERO), -self.PARB)

    def get_rzero(self):
        """Returns the resistance RZero of the sensor (in kOhms) for calibratioin purposes"""
        return self.get_resistance() * math.pow((self.ATMOCO2/self.PARA), (1./self.PARB))

    def get_corrected_rzero(self, temperature, humidity):
        """Returns the resistance RZero of the sensor (in kOhms) for calibration purposes
        corrected for temperature/humidity"""
        return self.get_corrected_resistance(temperature, humidity) * math.pow((self.ATMOCO2/self.PARA), (1./self.PARB))
    def get_resistance_acohol(self):
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

    def get_acohol(self):
        """Returns the resistance RZero of the sensor (in kOhms) for calibration purposes
        corrected for temperature/humidity"""
        ratio = self.get_resistance_acohol() / 800
        x = 0.3934 * ratio
        return math.pow(x,-1.504)
