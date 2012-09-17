#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial

# these values from
# http://www.sparkfun.com/datasheets/BreakoutBoards/0712.pdf
ACS712_5A_SENSITIVITY = 0.185
ACS712_20A_SENSITIVITY = 0.100
ACS712_30A_SENSITIVITY = 0.66


def current_sensor_ACS712(sensitivity_rating, read_value):
    """Convert read value to amps for given rating."""
    volts_per_increment = 5 / 1024.0
    return (
        (volts_per_increment * (read_value * 1024) - 2.5) /
        sensitivity_rating)


current_sensor_ACS712_5A = partial(
    current_sensor_ACS712,
    ACS712_5A_SENSITIVITY)


current_sensor_ACS712_20A = partial(
    current_sensor_ACS712,
    ACS712_20A_SENSITIVITY)


current_sensor_ACS712_30A = partial(
    current_sensor_ACS712,
    ACS712_30A_SENSITIVITY)
