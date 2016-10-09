#!/bin/python

import json
import RPi.GPIO as GPIO
import datetime
import requests
from buzzer_music import Buzzer

BACKEND_ENDPOINT="https://smart-chair.herokuapp.com"
USERNAME="admin"
POLLING_INTERVAL_SECS = 3



def post(uri, data):
  response = requests.post(uri, json=data)
  json_obj = response.json()
  return json_obj


def get(uri):
  response = requests.get(uri)
  json_obj = response.json()
  return json_obj


def get_pretty_json_obj(json_obj):
  return json.dumps(json_obj, indent=4, sort_keys=True)


def register_user_event(username, event_type):
  print "Registering event_type: '%s' for user: '%s'" % (event_type, username)
  uri = BACKEND_ENDPOINT+'/event/register'
  json = {"username": username,"event_type":event_type}
  response = post(uri, json)
  print "Register Event Response: %s" % get_pretty_json_obj(response)


def get_user_reminders(username):
  print "Fetching User Reminders for user: '%s'" % username
  uri = BACKEND_ENDPOINT+'/reminders/'+username
  response = get(uri)
  print "Get User Reminders Response: %s" % get_pretty_json_obj(response)
  return response


def buzz(buzz_type):
  print "Paying buzz type: %s" % buzz_type
  buzzer = Buzzer()
  buzzer.play(buzz_type)


def send_user_reminder(username, reminder_type):
  print "Sending reminder_type: '%s' to user: '%s'" % (reminder_type, username)
  uri = BACKEND_ENDPOINT+'/reminders/send'
  data = {"username": username,"reminder_type":reminder_type}
  response = post(uri, data)
  print "Send Reminder Response: %s" % get_pretty_json_obj(response)


def get_current_time_utc():
  return datetime.datetime.utcnow()


def should_update_database(last_updated, posture, sitting):
  seconds_since_last_update = (get_current_time_utc() - last_updated).total_seconds()
  #print "Seconds since last update: %s" % seconds_since_last_update
  if seconds_since_last_update > POLLING_INTERVAL_SECS:
    #print "Polling Interval Threshold Reached. Posture: %s, Sitting: %s" % (posture, sitting)
    return posture or sitting
  return False


def check_for_and_send_user_reminders(username):
  reminders = get_user_reminders(USERNAME)
  if reminders is not None:
    reminders = reminders["reminders"]

  send_posture_reminder = reminders["send_posture_reminder"]
  send_sitting_reminder = reminders["send_sitting_reminder"]
  print "User Reminders: Posture:%s, Sitting:%s" % (send_posture_reminder, send_sitting_reminder)

  if send_posture_reminder:
    print "Sending User Posture Reminder"
    buzz("posture")
    send_user_reminder(USERNAME, "posture")
    
  if send_sitting_reminder:
    print "Sending User Sitting Reminder"
    buzz("sitting")
    send_user_reminder(USERNAME, "sitting")


def buzz(buzz_type):
  print "Paying buzz type: %s" % buzz_type
  buzzer = Buzzer()
  buzzer.play(buzz_type)


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
      user_reminders = get_user_reminders(USERNAME)
      check_for_and_send_user_reminders(USERNAME)
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
  #get_user_reminders(USERNAME)
  #send_user_reminder(USERNAME, "sitting")
  #check_for_and_send_user_reminders(USERNAME)
  run()
