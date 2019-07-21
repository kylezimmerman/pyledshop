import socket

from .constants import (END_FLAG, SET_BRIGHTNESS, SET_COLOR, SET_CUSTOM,
                        SET_PRESET, SET_SPEED, START_FLAG, SYNC, TOGGLE)
from .utils import clamp
from .WifiLedShopLightState import WifiLedShopLightState


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
    try:
      self.reconnect()
    except:
      print('Failed to connect to light')
      pass

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
    Sets the brightness of the light (0 to 255)
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
    Sets the light effect to the provided built-in effect number
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
