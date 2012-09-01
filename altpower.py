#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from firmata import Arduino, OUTPUT, INPUT
from cosmSender import CosmSender


class AlternatePowerReporter(object):
    """Read a load of things, send to cosm."""

    def __init__(self, api_key, feed, serial_port, delay=1):
        """Setup hardware and remote feeds.

        @param api_key This is the key from Cosm.com
        @param feed This is the feed ID from Cosm.com
        @param serial_port Where to read data from
        @param delay Number of seconds to wait between reads.

        """
        self.api_key = api_key
        self.feed = feed
        self.serial_port = serial_port
        self.delay = delay

        self.arduino = Arduino(self.serial_port)
        self.cosm = CosmSender(self.api_key, self.feed, {}, cacheSize=0)

        self.streams = {}

    def add_sensor(self, pin_number, feed_id):
        """Add a sensor (on the arduino) to our read list."""
        self.streams[feed_id] = pin_number
        self.arduino.pin_mode(pin_number, INPUT)

    def read_sensors(self):
        """Read all of the pins we know about, return them."""
        result = {}
        self.arduino.parse()
        for stream, pin_no in self.streams.items():
            result[stream] = self.arduino.analog_read(pin_no)
        return result

    def send_data(self, data):
        """Send stuff to cosm."""
        for stream, value in data.items():
            self.cosm.sendData(stream, str(value))

    def run(self):
        while True:
            data = self.read_sensors()
            self.send_data(data)
            time.sleep(self.delay)

    def test_setup(self):
        """Check that the streams defined are available etc."""
        for stream in self.streams:
            if not stream in self.cosm.cache:
                logging.warn(
                    "Stream '%s' not set up on Cosm, will be created" % (
                        stream)) 
