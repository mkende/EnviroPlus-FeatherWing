"""
plotter-gas.py

Logs the levels of different gases over 24hrs (by default)
"""

interval = 540 # full screen of reading spans 24hrs
#interval = 1 # uncomment for 1 reading per second
#interval = 60 # uncomment for 1 reading per minute
#interval = 3600 # uncomment for 1 reading per hour

import time

from pimoroni_envirowing import gas
from pimoroni_envirowing.screen import plotter

import terminalio
from adafruit_display_text import label

# colours for the plotter are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# the max value is set to 3.3 as its the max voltage the feather can read
splotter = plotter.ScreenPlotter([red, green, blue], max_value=3.3, min_value=0.5)

# add a colour coded text label for each reading
splotter.group.append(label.Label(terminalio.FONT, text="OX: {:.0f}", color=red, x=0, y=5, max_glyphs=15))
splotter.group.append(label.Label(terminalio.FONT, text="RED: {:.0f}", color=green, x=80, y=5, max_glyphs=15))
splotter.group.append(label.Label(terminalio.FONT, text="NH3: {:.0f}", color=blue, x=0, y=20, max_glyphs=15))


while True:
    #take readings
    reading = gas.read_all()

    # update the line graph
    # the value plotted on the graph is the voltage drop over each sensor, not the resistance, as it graphs nicer
    splotter.update(
        reading._OX.value * (reading._OX.reference_voltage/65535),
        reading._RED.value * (reading._RED.reference_voltage/65535),
        reading._NH3.value * (reading._NH3.reference_voltage/65535)
    )

    # update the labels
    splotter.group[1].text = "OX: {:.0f}K".format(reading.oxidising/1000)
    splotter.group[2].text = "RED: {:.0f}K".format(reading.reducing/1000)
    splotter.group[3].text = "NH3: {:.0f}K".format(reading.nh3/1000)
    
    time.sleep(interval)