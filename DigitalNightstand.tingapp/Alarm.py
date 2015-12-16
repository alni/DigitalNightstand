import pygame
import schedule # install with "pip install schedule"
import sched, time, datetime
import os
import json

class Alarm(object):
    """description of class"""
    def __init__(self, sound, config="data/alarms.json", settings=None):
        self.current_alarm = None
        self.sound = sound
        if settings == None:
            self.settings = self.load_settings(config)
        else:
            self.settings = settings
        self.s = sched.scheduler(time.time, time.sleep)

    def load_settings(self, config):
        with open(config) as data_file:
            data = json.load(data_file)
        return data

    def _format_time(self, hour, minute):
        return "%02d:%02d" % (hour,minute)

    def create_alarms(self):
        alarms = self.settings["alarms"]
        for alarm in alarms:
            time = alarm["time"]
            days = None
            title = "ALARM"
            if "days" in alarm:
                days = alarm["days"]
            if "title" in alarm:
                title = alarm["title"]
            self.create_alarm(time[0], time[1], days, title)
        for job in schedule.jobs:
            print job

    def create_alarm(self, hour, minute, days=None, title="ALARM"):
        if days == None:
            schedule.every().day.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
        else:
            if "mon" in days:
                schedule.every().monday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "tue" in days:
                schedule.every().tuesday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "wed" in days:
                schedule.every().wednesday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "thu" in days:
                schedule.every().thursday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "fri" in days:
                schedule.every().friday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "sat" in days:
                schedule.every().saturday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "sun" in days:
                schedule.every().sunday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
        # self.s.enterabs(secs, 1, self.play_alarm, ())

    def run_alarm(self):
        schedule.run_pending()
        # self.s.run()

    def play_alarm(self, title):
        self.current_alarm = title
        print self.current_alarm
        pygame.mixer.init()
        pygame.mixer.music.load(self.sound)
        pygame.mixer.music.play(-1)
    
    def stop_alarm(self):
        self.current_alarm = None
        pygame.mixer.music.stop()

    def next_alarm(self):
        return schedule.next_run()

    @staticmethod
    def save_settings(settings_form, file_path=""):
        num_alarms = 5

        settings = {
            "alarms": []
        }

        for i in range(1, num_alarms+1):
            hour = settings_form.getvalue("alarm_" + str(i) + "_hour")



curr_dir = os.path.dirname(os.path.realpath(__file__))
# alarm = Alarm(curr_dir + "/res/sounds/Argon_48k.wav")
alarm_time = time.localtime()
print alarm_time.tm_isdst
alarm_time = time.struct_time((alarm_time.tm_year,
                               alarm_time.tm_mon,
                               alarm_time.tm_mday,
                               12, # hours
                               20, # minutes
                               0, # seconds
                               alarm_time.tm_wday,
                               alarm_time.tm_yday,
                               alarm_time.tm_isdst
                              ))
print time.strftime("%X", alarm_time)
# alarm.create_alarms()
print schedule.next_run()
# alarm.create_alarm(time.mktime(alarm_time))
# alarm.run_alarm()
#alarm.play_alarm()
while 0:
    time.sleep(1.0/30)
    schedule.run_pending()

