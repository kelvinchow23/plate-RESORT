#!/usr/bin/env python3

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class ADCManager:
    def __init__(self):
        # Setup I2C for ADS1115
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.adc_channel = AnalogIn(self.ads, ADS.P0)

    def get_voltage(self):
        """Get current voltage reading from ADC"""
        return self.adc_channel.voltage

    def voltage_to_angle(self, voltage):
        """Convert feedback voltage to angle based on datasheet calibration:
        2.60V = 0° (high voltage = 0°), 0.72V = 270° (low voltage = 270°)
        """
        # Clamp voltage to valid range
        voltage = min(2.60, max(0.72, voltage))
        normalized_voltage = (2.60 - voltage) / (2.60 - 0.72)
        angle = normalized_voltage * 270.0
        print(f"[ADC DEBUG] Voltage: {voltage:.3f} V -> Angle: {angle:.1f}°")
        return angle