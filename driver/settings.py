#!/usr/bin/env python
SETTINGS = {
	'data_pin'  : 17,						# data GPIO pin			
	'clock_pin' : 21,						# clock GPIO pin
	'latch_pin' : 22,						# latch GPIO pin

	'max_inflation_time': 12000,			# in seconds
	'min_deflation_time': 800,				# in seconds
}

def get_setting(key):
	return SETTINGS[key] if key in SETTINGS else None
