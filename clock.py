from apscheduler.schedulers.blocking import BlockingScheduler
import tasks
from rq import Queue
from worker import conn



sched = BlockingScheduler()



@sched.scheduled_job('interval', seconds=20)
def close_sessions():
    print('This job closes any old, open sessions.')
    q = Queue(connection=conn)
    result = q.enqueue(tasks.close_stale_sessions)
    print('Posted Worker Message to Redis for closing sessions: ' + str(result))




# @sched.scheduled_job('interval', minutes=1)
# def timed_job():
#     print('This job is run every 1 minute.')


# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')


sched.start()
