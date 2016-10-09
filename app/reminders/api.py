from app import application
from flask import jsonify, request
from app.reminders import reminder_manager


@application.route('/reminders/<username>', methods=['GET'])
def get_user_reminders(username):
    print "Get User Reminder Request Received: %s" % username
    reminders = reminder_manager.get_user_reminders(username)
    print "Reminders: " + str(reminders)
    return jsonify(
    	reminders=reminders
    )


@application.route('/reminders/send', methods=['POST'])
def send_user_reminder():
	json = request.get_json()
	print "Send Reminder Request Received: " + str(json)
	username = json["username"]
	reminder_type = json["reminder_type"]
	status_msg = reminder_manager.send_reminder(username, reminder_type)
	return jsonify(
		status_msg=status_msg
	)
