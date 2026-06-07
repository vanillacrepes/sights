import keyboard

class AppState:
  def __init__(self):
    self.mode = 1
    
def setupInput(app_state):
  keyboard.add_hotkey('1', lambda: setattr(app_state, 'mode', 1))
  keyboard.add_hotkey('2', lambda: setattr(app_state, 'mode', 2))
  keyboard.add_hotkey('3', lambda: setattr(app_state, 'mode', 3))