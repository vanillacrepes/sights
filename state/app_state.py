import keyboard

class AppState:
  def __init__(self):
    self.mode = 1
    
  def setupInput(self):
    keyboard.add_hotkey('1', lambda: setattr(self, 'mode', 1))
    keyboard.add_hotkey('2', lambda: setattr(self, 'mode', 2))
    keyboard.add_hotkey('3', lambda: setattr(self, 'mode', 3))