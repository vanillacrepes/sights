import cv2 
import keyboard
import time

# a lil kick at "proper" oop

class CameraSwitcher():
  def __init__(self):    
    self.cameras = self.findCameras()
    
    self.request_switch = False
    
    self.current_i = 0
    self.cap = cv2.VideoCapture(self.cameras[self.current_i])
    
  def findCameras(self):
    cameras = []
    
    for i in range(10):
      cap = cv2.VideoCapture(i)
      
      if cap.isOpened():
        ret, _ = cap.read()
        
        if ret:
          cameras.append(i)
          print(i)
          
      cap.release()
      
    return cameras
  
  @property
  def current_camera(self):
    return self.cameras[self.current_i]
  
  def switch_camera(self):
    self.cap.release()
    
    self.current_i = (self.current_i + 1) % len(self.cameras)
    
    self.cap = cv2.VideoCapture(self.cameras[self.current_i])
    
    time.sleep(0.2)
    
  def setup_camera_hotkey(self):
    keyboard.add_hotkey('4', lambda: 
      setattr(self, 'request_switch', True)
    )
    
  def read(self):
    return self.cap.read()
  
  def release(self):
    self.cap.release()


    
    