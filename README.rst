Alternative power monitoring
============================

This module is intended for use with e.g. a Solar panel wired up to a car battery.
The python code sits on a device (e.g. Mac Mini) that has an Arduino board attached by USB.
The Arduino board can be connected to various sensors (e.g. current sensor) and this code
will report the values to Cosm.

Basic usage is to make a board and add a sensor to it, which needs a pin spec (e.g. 'a:0:i', see pyfirmata docs), a stream id (from Cosm), and value modifier function (e.g., take the read value, multiply it by something).

The values are read constantly over the delay period and averaged, before sending.

Quickstart
----------

    mvirtualenv altpower && pip install https://github.com/stringfellow/alt-power-cosm/tarball/master

then, e.g.:

    from altpower import AlternatePowerReporter

    from altpower.utils import current_sensor_ACS712_5A
    
    apr = AlternatePowerReporter("MYKEY", FEED_ID, "/dev/tty.WHATEVS")

    apr.add_sensor('a:0:i', 'STREAM_NAME', current_sensor_ACS712_5A)

    apr.run()

