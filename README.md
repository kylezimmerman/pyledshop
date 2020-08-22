# pyledshop
Python module for interacting with LED Shop Compatible Wifi Controllers (e.g. SP108E)

## Usage

```py
from pyledshop import WifiLedShopLight, MonoEffect, CustomEffect

# The IP assigned to the device on your network
# I recommend setting a static IP to avoid the IP changing over time with DHCP
light_ip = "192.168.0.100" 

light = WifiLedShopLight(light_ip)

# Power controls
light.turn_off()
light.turn_on()
light.toggle()

# Color
light.set_color(255, 0, 0) # Red

# Effects
light.set_preset(MonoEffect.STATIC) # Enum for single color customizable effects
light.set_preset(0) # Rainbow - See <pyledshop>/effects.py for full list of values
light.set_custom(CustomEffect.CUSTOM_1) # Custom Effects upload via app

# Brightness
light.set_brightness(0) # Dimmest
light.set_brightness(255) # Brightest

# Speed
light.set_speed(0) # Slowest
light.set_speed(255) # Fastest

# Sync state
light.sync_state() # Updates light.state with the latest state on the controller
```

## Features

This project is mostly a reverse engineering of the LED Shop protocol by capturing packets sent to the controller using the app.
Most of the features in the app are supported, but not everything.

### Supported
- [x] Turn On / Off
- [x] Set Color (rgb)
- [x] Set Brightness
- [x] Set Speed
- [x] Select Preset
- [x] Select Custom
- [x] Sync State

### Not Yet Supported
- [ ] Upload new custom patterns
- [ ] Change number of segments
- [ ] Change length of segments

### Won't Be Supported
- Connecting to Device.

  This is done via a complex (and often un-reliable) process involving the LED Shop App and the WiFi on your phone. It's not something that can be supported through software alone.

  If you are having difficulty connecting to the device, the only way I have found to work is to **DISABLE your routers 5 GHz network completely** during pairing. I had both 2.4 and 5 GHz networks running simultaneously, even with different names I could not get it to connect. The only thing that worked was to temporarily disable 5 GHz to connect, and then re-enabling both.
