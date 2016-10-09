#!/bin/python

import json
import RPi.GPIO as GPIO
import datetime
import requests

BACKEND_ENDPOINT="https://smart-chair.herokuapp.com"
USERNAME="admin"
POLLING_INTERVAL_SECS = 3


def get_current_time_utc():
  return datetime.datetime.utcnow()


def buzzBuzzer(time):
  GPIO.output(buzzer,1)
  time.sleep(time)
  GPIO.output(buzzer,0)

  
def should_update_database(last_updated, posture, sitting):
  seconds_since_last_update = (get_current_time_utc() - last_updated).total_seconds()
  #print "Seconds since last update: %s" % seconds_since_last_update
  if seconds_since_last_update > POLLING_INTERVAL_SECS:
    #print "Polling Interval Threshold Reached. Posture: %s, Sitting: %s" % (posture, sitting)
    return posture or sitting
  return False


def register_user_event(username, event_type):
  print "Registering user event: %s" % event_type
  response = requests.post(BACKEND_ENDPOINT+"/event/register", json = {"username": username,"event_type":event_type})
  json_obj = response.json()  #json.loads(r)
  print "Response: %s" % json.dumps(json_obj, indent=4, sort_keys=True)


def run():
  seatButton=13
  backButton=19
  buzzer=26

  GPIO.setmode(GPIO.BCM)

  GPIO.setup(seatButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(backButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(buzzer, GPIO.OUT)
  try:
    while True:
      sitting_recorded = False
      posture_recorded = False
      last_update_sent = datetime.datetime.now()
      while True:
        back_state = GPIO.input(backButton)
        seat_state = GPIO.input(seatButton)
        if back_state==False:
          print('Back is touching')
          posture_recorded = True
          event_type = "posture"
        if seat_state==False:
          sitting_recorded = True
          event_type = "sitting"
          print('Sitting')
        if should_update_database(last_update_sent, posture_recorded, sitting_recorded):
          register_user_event(USERNAME, event_type)
          break
                                  
  except KeyboardInterrupt:
    GPIO.cleanup()


if __name__ == "__main__":
  #register_user_event(USERNAME,"sitting")
  run()
