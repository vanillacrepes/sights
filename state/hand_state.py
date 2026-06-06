class HandState:
  def __init__(self):
    self.save_armed = True
    self.saved_position = None
    self.open_frames = 0
    
hand_states = {
  "Left": HandState(),
  "Right": HandState()
}