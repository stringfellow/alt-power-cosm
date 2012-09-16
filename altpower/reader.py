#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
from pyfirmata import Arduino, util
from cosmSender import CosmSender


log = logging.getLogger(__file__)


class AlternatePowerReporter(object):
    """Read a load of things, send to cosm."""

    def __init__(self, api_key, feed, serial_port, delay=5000):
        """Setup hardware and remote feeds.

        @param api_key This is the key from Cosm.com
        @param feed This is the feed ID from Cosm.com
        @param serial_port Where to read data from
        @param delay Number of miliseconds to wait between reads.

        """
        self.api_key = api_key
        self.feed = feed
        self.serial_port = serial_port
        self.delay = delay

        self.arduino = Arduino(self.serial_port)
        self.iterator = util.Iterator(self.arduino)
        self.iterator.start()
        self.cosm = CosmSender(self.api_key, self.feed, {}, cacheSize=0)

        self.streams = {}

    def add_sensor(self, pin_string, feed_id, fn):
        """Add a sensor (on the arduino) to our read list.

        :param pin_string: e.g. a:0:i (see pyFirmata docs)
        :param feed_id: e.g. solar_current (datastream on cosm)
        :param fn: the function to run on the pin readout before sending

        """
        self.streams[feed_id] = {
            'pin': self.arduino.get_pin(pin_string),
            'fn': fn,
        }

    def read_sensors(self):
        """Read all of the pins we know about, return them."""
        results = {}
        for i in range(self.delay):
            for stream, params in self.streams.items():
                val = params['pin'].read()
                if val:
                    results.setdefault(stream, {'sum': 0, 'reads': 0})
                    results[stream]['sum'] += params['fn'](val)
                    results[stream]['reads'] += 1
            time.sleep(self.delay / 1000.0)

        for stream, params in results.items():
            results['value'] = (
                results[stream]['sum'] / float(results[stream]['reads']))

        return results

    def send_data(self, data):
        """Send stuff to cosm."""
        for stream, params in data.items():
            self.cosm.sendData(stream, str(params['value']))

    def run(self):
        while True:
            data = self.read_sensors()
            self.send_data(data)

    def test_setup(self):
        """Check that the streams defined are available etc."""
        for stream in self.streams:
            if not stream in self.cosm.cache:
                log.warn(
                    "Stream '%s' not set up on Cosm, will be created" % (
                        stream))
