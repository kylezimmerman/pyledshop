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
