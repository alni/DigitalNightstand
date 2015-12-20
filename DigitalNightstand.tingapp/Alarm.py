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
        if settings is None:
            self.settings = self.load_settings(config)
        else:
            self.settings = settings
        self.s = sched.scheduler(time.time, time.sleep)

    def load_settings(self, config):
        if config is not None:
            # Only load settings if config is actually set
            with open(config) as data_file:
                data = json.load(data_file)
            return data
        else:
            # Otherwise, return None
            return None

    def _format_time(self, hour, minute):
        return "%02d:%02d" % (hour,minute)

    def create_alarms(self):
        if self.settings is not None:
            # Only create alarms if settings actually set
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
            # If days is not defined we assume that the alarm should
            # be run every day
            schedule.every().day.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
        else:
            # Check if each weekday exists in days.
            # And schedule the alarm for each weekday found.
            if "mon" in days: # Monday found... Schedule it!
                schedule.every().monday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "tue" in days: # Tuesday found... Schedule it!
                schedule.every().tuesday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "wed" in days: # Wednesday found... Schedule it!
                schedule.every().wednesday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "thu" in days: # Thursday found... Schedule it!
                schedule.every().thursday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "fri" in days: # Friday found... Schedule it!
                schedule.every().friday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "sat" in days: # Saturday found... Schedule it!
                schedule.every().saturday.at(self._format_time(hour, minute)).do(self.play_alarm, (title))
            if "sun" in days: # Sunday found... Schedule it!
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
        # Return the datetime object of next scheduled alarm
        return schedule.next_run()

    @staticmethod
    def save_settings(settings_form, file_path=""):
        num_alarms = 5

        settings = {
            "alarms": []
        }

        for i in range(1, num_alarms+1):
            hour = settings_form.getvalue("alarm_" + str(i) + "_hour")

