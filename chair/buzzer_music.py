import RPi.GPIO as GPIO   #import the GPIO library
import time               #import the time library


# NOTES TO FREQUENCIES DICTIONARY
fN =  {
            "cL": 129,
            "cLS": 139,
            "dL": 146,
            "dLS": 156,
            "eL": 163,
            "fL": 173,
            "fLS": 185,
            "gL": 194,
            "gLS": 207,
            "aL": 219,
            "aLS": 228,
            "bL": 232,
            "c": 261,
            "cS": 277,
            "d": 294,
            "dS": 311,
            "e": 329,
            "f": 349,
            "fS": 370,
            "g": 391,
            "gS": 415,
            "a": 440,
            "aS": 455,
            "b": 466,
            "cH": 523,
            "cHS": 554,
            "dH": 587,
            "dHS": 622,
            "eH": 659,
            "fH": 698,
            "fHS": 740,
            "gH": 784,
            "gHS": 830,
            "aH": 880,
            "aHS": 910,
            "bH": 933
            }

class Buzzer(object):
 def __init__(self):
  GPIO.setmode(GPIO.BCM)  
  self.buzzer_pin = 26 #set to GPIO pin 5
  GPIO.setup(self.buzzer_pin, GPIO.IN)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  print("buzzer ready")

 def __del__(self):
  class_name = self.__class__.__name__
  print (class_name, "finished")

 def buzz(self,pitch, duration):   #create the function "buzz" and feed it the pitch and duration) 
  if(pitch==0):
   time.sleep(duration)
   return
  period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
  delay = period / 2     #calcuate the time for half of the wave  
  cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency

  for i in range(cycles):    #start a loop from 0 to the variable "cycles" calculated above
   GPIO.output(self.buzzer_pin, True)   #set pin 18 to high
   time.sleep(delay)    #wait with pin 18 high
   GPIO.output(self.buzzer_pin, False)    #set pin 18 to low
   time.sleep(delay)    #wait with pin 18 low

 def play(self, tune):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  x=0

  print("Playing tune ",tune)
  if(tune=="sitting"):
    pitches=[392,294,0,392,294,0,392,0,392,392,392,0,1047,262]
    duration=[0.2,0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.8,0.4]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1
  elif(tune=="posture"):
    pitches=[1047, 988,523]
    duration=[0.1,0.1,0.2]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1


  GPIO.setup(self.buzzer_pin, GPIO.IN)

if __name__ == "__main__":
  a = input("Enter \"posture\" or \"sitting\":")
  buzzer = Buzzer()
  buzzer.play(str(a))
