import socket
import time

START_FLAG = 0x38
END_FLAG = 0x83

TOGGLE = 0xAA
SET_COLOR = 0x22
SET_BRIGHTNESS = 0x2A
SET_SPEED = 0x03
SET_PRESET = 0x2C
SET_CUSTOM = 0x02
SET_LIGHTS_PER_SEGMENT = 0x2D
SET_SEGMENT_COUNT = 0x2E

SYNC = 0x10

MONO_EFFECTS = {
  'Solid (custom color)': 211,
  'Breathing (custom color)': 206,
  'Meteor (custom color)': 205,
  'Flow (custom color)': 208,
  'Wave (custom color)': 209,
  'Flash (custom color)': 210,
  'Stack (custom color)': 207,
  'Catchup (custom color)': 212,
}

PRESET_EFFECTS = {
  'Rainbow': 0,
  'Colors changing meteors': 1,
  'Flowing Colors': 2,
  'Overlaying Flowing': 3,
  'Red stacking': 4,
  'Green stacking': 5,
  'Blue stacking': 6,
  'Colors changing stacking': 7,
  'Fading flowing': 8,
  'Color changing cross flowing': 9,
  'Cross flowing': 10,
  'Chasing color dots': 11,
  'Colorful wave': 12,
  'Burning fire': 13,
  'Red meteor': 14,
  'Green meteor': 15,
  'Blue meteor': 16,
  'Yellow meteor': 17,
  'Cyan meteor': 18,
  'Purple meteor': 19,
  'White meteor': 20,
  'Red wave': 21,
  'Green wave': 22,
  'Blue wave': 23,
  'Yellow wave': 24,
  'Cyan wave': 25,
  'Purple wave': 26,
  'White wave': 27,
  'Red chasing dots': 28,
  'Green chasing dots': 29,
  'Blue chasing dots': 30,
  'Yellow chasing dots': 31,
  'Cyan chasing dots': 32,
  'White chasing dots': 33,
  'Purple chasing dots': 34,
  'Cyan dots blink on silver': 35,
  'Purple dots blink on silver': 36,
  'Yellow dots blink on silver': 37,
  'Blue dots blink on silver': 38,
  'Green dots blink on silver': 39,
  'Red dots blink on silver': 40,
  'Red and Green flowing': 41,
  'Red and blue flowing': 42,
  'Red and yellow flowing': 43,
  'Red and cyan flowing': 44,
  'Red and purple flowing': 45,
  'Red and white flowing': 46,
  'Green and blue flowing': 47,
  'Green and yellow flowing': 48,
  'Green and cyan flowing': 49,
  'Green and purple flowing': 50,
  'Green and white flowing': 51,
  'Blue and yellow flowing': 52,
  'Blue and cyan flowing': 53,
  'Blue and purple flowing': 54,
  'Blue and white flowing': 55,
  'Yellow and cyan flowing': 56,
  'Yellow and purple flowing': 57,
  'Yellow and white flowing': 58,
  'Cyan and purple flowing': 59,
  'Cyan and white flowing': 60,
  'Red crossing flowing': 61,
  'Green crossing flowing': 62,
  'Blue crossing flowing': 63,
  'Yellow crossing flowing': 64,
  'Cyan crossing flowing': 65,
  'Purple crossing flowing': 66,
  'White crossing flowing': 67,
  'Red arrows': 68,
  'Green arrows': 69,
  'Blue arrows': 70,
  'Yellow arrows': 71,
  'Cyan arrows': 72,
  'Purple arrows': 73,
  'Red cudgel': 74,
  'Green cudgel': 75,
  'Blue cudgel': 76,
  'Yellow cudgel': 77,
  'Cyan cudgel': 78,
  'Purple cudgel': 79,
  'Gaps in cyan': 80,
  'Gaps in purple': 81,
  'Gaps in yellow': 82,
  'Gaps in blue': 83,
  'Gaps in green': 84,
  'Gaps in red': 85,
  'Red breathe': 86,
  'Green breathe': 87,
  'Blue breathe': 88,
  'Yellow breathe': 89,
  'Cyan breathe': 90,
  'Purple breathe': 91,
  'White breathe': 92,
  'Red arrows reverse': 93,
  'Green arrows reverse': 94,
  'Blue arrows reverse': 95,
  'Yellow arrows reverse': 96,
  'Cyan arrows reverse': 97,
  'Purple arrows reverse': 98,
  'Red dots running in cyan': 99,
  'Green dots running in purple': 100,
  'Blue dots running in yellow': 101,
  'Yellow dots running in blue': 102,
  'Cyan dots running in green': 103,
  'Purple dots running in red': 104,
  'White dots running in cyan': 105,
  'Red fading in and out': 106,
  'Green fading in and out': 107,
  'Blue fading in and out': 108,
  'Yellow fading in and out': 109,
  'Cyan fading in and out': 110,
  'Purple fading in and out': 111,
  'White fading in and out': 112,
  'Red meteor reverse': 113,
  'Green meteor reverse': 114,
  'Blue meteor reverse': 115,
  'Yellow meteor reverse': 116,
  'Cyan meteor reverse': 117,
  'Purple meteor reverse': 118,
  'White meteor reverse': 119,
  'Red wave 2': 120,
  'Green wave 2': 121,
  'Blue wave 2': 122,
  'Yellow wave 2': 123,
  'Cyan wave 2': 124,
  'Purple wave 2': 125,
  'White wave 2': 126,
  'Red wing dots': 127,
  'Green swing dots': 128,
  'Blue swing dots': 129,
  'Yellow swing dots': 130,
  'Cyan swing dots': 131,
  'Purple swing dots': 132,
  'White swing dots': 133,
  'Red and green cudgel': 134,
  'Green and blue cudgel': 135,
  'Blue and yellow cudgel': 136,
  'Yellow and cyan cudgel': 137,
  'Cyan and purple cudgel': 138,
  'Purple and white cudgel': 139,
  'White and red cudgel': 140,
  'Red overlaps green': 141,
  'Green overlaps red': 142,
  'Blue overlaps green': 143,
  'Yellow overlaps green': 144,
  'Cyan overlaps green': 145,
  'Purple overlaps green': 146,
  'White overlaps green': 147,
  'Red overlaps blue': 148,
  'Green overlaps blue': 149,
  'Blue overlaps green 2': 150,
  'Yellow overlaps blue': 151,
  'Cyan overlaps blue': 152,
  'Purple overlaps blue': 153,
  'White overlaps blue': 154,
  'Pink mix blue': 155,
  'Green mix yellow': 156,
  'Blue mix pink': 157,
  'Blue mix white': 158,
  'Green mix orange': 159,
  'Blue mix purple': 160,
  'Cyan mix white': 161,
  'Red blinking': 162,
  'Green blinking': 163,
  'Blue blinking': 164,
  'Yellow blinking': 165,
  'Cyan blinking': 166,
  'Purple blinking': 167,
  'White blinking': 168,
  'Red stacking into green': 169,
  'Green stacking into blue': 170,
  'Blue stacking into yellow': 171,
  'Yellow stacking into cyan': 172,
  'Cyan stacking into purple': 173,
  'Purple stacking into white': 174,
  'White stacking into red': 175,
  'Color changing breathing': 176,
  'Multicolored gradients': 177,
  'Color Flashing': 178,
  'Rainbow reverse': 179
}

CUSTOM_EFFECTS = {
  'Custom Effect 1': 1,
  'Custom Effect 2': 2,
  'Custom Effect 3': 3,
  'Custom Effect 4': 4,
  'Custom Effect 5': 5,
  'Custom Effect 6': 6,
  'Custom Effect 7': 7,
  'Custom Effect 8': 8,
  'Custom Effect 9': 9,
  'Custom Effect 10': 10,
  'Custom Effect 11': 11,
  'Custom Effect 12': 12,
}

def clamp(value, min=0, max=255):
  """
  Clamps a value to be within the specified range

  Since led shop uses bytes for most data, the defaults are 0-255
  """
  if value > max:
    return max
  elif value < min:
    return min
  else:
    return value

class WifiLedShopLightState:
  def __init__(self):
    self.is_on = False
    self.color = (255, 255, 255)
    self.brightness = 255
    self.mode = 0
    self.speed = 255

  def __repr__(self):
      return f"""
        is_on: {self.is_on}
        color: {self.color}
        brightness: {self.brightness}
        mode: {self.mode}
        speed: {self.speed}
      """

  def update_from_sync(self, sync_data):
    self.is_on = sync_data[1] == 1
    self.color = (sync_data[10], sync_data[11], sync_data[12])
    self.mode = sync_data[2]
    self.speed = sync_data[3]
    self.brightness = sync_data[4]

class WifiLedShopLight:
  """
  A Wifi LED Shop Light
  """

  def __init__(self, ip, port = 8189, timeout = 5, retries = 5):
    self.ip = ip
    self.port = port
    self.timeout = timeout
    self.retries = retries
    self.state = WifiLedShopLightState()

    # Connect and sync the inital state
    self.sock = None
    self.reconnect()
    #self.sync_state()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()

  def reconnect(self):
    if self.sock:
      self.close()
    
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.settimeout(self.timeout)
    self.sock.connect((self.ip, self.port))
    print('Reconnected')

  def close(self):
    """
    Closes the socket connection to the light
    """
    self.sock.close()
    self.sock = None

  def set_color(self, r=0, g=0, b=0):
    """
    Sets the color of the light (rgb each 0-255)
    """
    r = clamp(r)
    g = clamp(g)
    b = clamp(b)
    self.state.color = (r, g, b)
    self.send_command(SET_COLOR, [int(r), int(g), int(b)])

  def set_brightness(self, brightness=0):
    """
    S
    """
    brightness = clamp(brightness)
    self.state.brightness = brightness
    self.send_command(SET_BRIGHTNESS, [int(brightness)])

  def set_speed(self, speed=0):
    """
    Sets the speed of the effect (0-255). Not all effects use the speed, but it can be safely set regardless
    """
    speed = clamp(speed)
    self.state.speed = speed
    self.send_command(SET_SPEED, [int(speed)])

  def set_preset(self, preset=0):
    """
    Sets the light effect tot he provided built-in effect number
    """
    preset = clamp(preset)
    self.state.mode = preset
    self.send_command(SET_PRESET, [int(preset)])

  def set_custom(self, custom):
    """
    Sets the light effect to the provided custom effect number
    """
    custom = clamp(custom, 1, 12)
    self.state.mode = custom
    self.send_command(SET_CUSTOM, [int(custom)])

  def toggle_light(self):
    """
    Toggles the state of the light without checking the current state
    """
    self.state.is_on = not self.state.is_on
    self.send_command(TOGGLE)

  def turn_on(self):
    """
    Toggles the light on only if it is not already on
    """
    if not self.state.is_on:
      self.toggle_light()

  def turn_off(self):
    """
    Toggles the light off only if it is not already off
    """
    if self.state.is_on:
      self.toggle_light()

  def send_command(self, command, data=[]):
    """
    Helper method to send a command to the controller
    
    Formats the low level message details like Start/End flag, binary data, and command
    """
    min_data_len = 3
    padded_data = data + [0] * (min_data_len - len(data))
    raw_data = [START_FLAG, *padded_data, command, END_FLAG]
    self.send_bytes(raw_data)

  def send_bytes(self, data):
    """
    Helper method to send raw bytes directly to the controller
    """
    raw_data = bytes(data)

    attempts = 0
    while True:
      try:
        self.sock.sendall(raw_data)
        return
      except (socket.timeout, BrokenPipeError):
        if (attempts < self.retries):
          self.reconnect()
          attempts += 1
        else:
          raise

  def sync_state(self):
    """
    Syncs the state of the controller with the state of this object
    """
    attempts = 0
    while True:
      try:
        # Send the request for sync data
        self.send_command(SYNC)

        response = self.sock.recv(1024)

        # Extract the state data
        state = bytearray(response)
        self.state.update_from_sync(state)
        return
      except (socket.timeout, BrokenPipeError):
        # When there is an error with the socket, close the connection and connect again
        if attempts < self.retries:
          self.reconnect()
          attempts += 1
        else:
          raise

  def __repr__(self):
    return f"""WikiLedShopLight @ {self.ip}:{self.port}
      state: {self.state}
    """

  # This one needs work still... it seems to partially work but I think I'm misunderstanding how this works
  # def set_size(self, lights_per_segment, segment_count):
  #   self.send_command(SET_SEGMENT_COUNT, [segment_count])
  #   self.send_command(SET_LIGHTS_PER_SEGMENT, [lights_per_segment])



with WifiLedShopLight("192.168.0.103") as light:
  light.sync_state()
  print(light)

  light.turn_on()
  light.sync_state()
  print(light)

  time.sleep(1)

  light.turn_off()
  light.sync_state()
  print(light)

  # light.set_preset(MONO_STATIC)
  # light.set_color(255, 255, 255)
  # time.sleep(1)
  # light.set_color(255, 0, 0)
  # time.sleep(1)
  # light.set_color(0, 255, 0)
  # time.sleep(1)
  # light.set_color(0, 0, 255)
  # time.sleep(1)


  # # Test Brightness
  # for brightness in range(0, 255):
  #   light.set_brightness(brightness)
  #   time.sleep(0.01)
  # light.set_brightness(128)
  # time.sleep(0.1)

  # light.toggle_light()
  # time.sleep(1)
  # light.toggle_light()

  # for i in range(1, 180):
  #   light.set_preset(i)
  #   time.sleep(0.5)
