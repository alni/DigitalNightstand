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
        """Load settings from config"""
        if config is not None and os.path.exists(config):
            # Only load settings if config is actually set and the file exists
            with open(config) as data_file:
                data = json.load(data_file)
            return data
        else:
            # Otherwise, return None
            return None

    def set_settings(self, settings):
        """Set the current settings"""
        if settings is not None and "alarms" in settings:
            # Only set settings if settings is actually set and "alarms" exists
            # within settings
            self.settings = settings
            schedule.clear() # Delete all scheduled alarms
            self.create_alarms()

    def _format_time(self, hour, minute):
        """Format hour and time as 'HH:MM'"""
        return "%02d:%02d" % (hour,minute)

    def create_alarms(self):
        """Create alarms schedule from settings"""
        if self.settings is not None:
            # Only create alarms if settings actually set
            alarms = self.settings["alarms"]
            for alarm in alarms:
                time = alarm["time"]
                days = None
                title = "ALARM"
                repeat = False
                if "days" in alarm:
                    days = alarm["days"]
                if "title" in alarm:
                    title = alarm["title"]
                if "repeat" in alarm:
                    repeat = alarm["repeat"]
                self.create_alarm(time[0], time[1], repeat, days, title)
        for job in schedule.jobs:
            print job

    def create_alarm(self, hour, minute, repeat, days=None, title="ALARM"):
        """Create schedule for a single alarm
        
        Parameters:
        - hour : the hour to schedule the alarm for
        - minute : the minute to schedule the alarm for
        - repeat : should the alarm repeat?
        - days : (optional) the list of days to schedule this alarm for
        - title : (optional) the title of the alarm (defaults to 'ALARM')
        """
        _time = self._format_time(hour, minute)
        _args = None
        if repeat:
            _args = (title)
        else:
            # If repeat is false, then the alarm should only be run once
            _args = (title, True)
        if days == None or len(days) == 7:
            # If days is not defined, or it contains 7 entries, we assume that
            # the alarm should be run every day
            schedule.every().day.at(_time).do(self.play_alarm, _args)
        else:
            # Check if each weekday exists in days.
            # And schedule the alarm for each weekday found.
            if "mon" in days: # Monday found... Schedule it!
                schedule.every().monday.at(_time).do(self.play_alarm, _args)
            if "tue" in days: # Tuesday found... Schedule it!
                schedule.every().tuesday.at(_time).do(self.play_alarm, _args)
            if "wed" in days: # Wednesday found... Schedule it!
                schedule.every().wednesday.at(_time).do(self.play_alarm, _args)
            if "thu" in days: # Thursday found... Schedule it!
                schedule.every().thursday.at(_time).do(self.play_alarm, _args)
            if "fri" in days: # Friday found... Schedule it!
                schedule.every().friday.at(_time).do(self.play_alarm, _args)
            if "sat" in days: # Saturday found... Schedule it!
                schedule.every().saturday.at(_time).do(self.play_alarm, _args)
            if "sun" in days: # Sunday found... Schedule it!
                schedule.every().sunday.at(_time).do(self.play_alarm, _args)
        # self.s.enterabs(secs, 1, self.play_alarm, ())

    def run_alarm(self):
        """Run pending, scheduled alarms"""
        schedule.run_pending()
        # self.s.run()

    def play_alarm(self, title, only_once=False):
        """Play alarm
        
        Parameters:
        - title : the title of the alarm
        - only_once : (optional) should the schedule of this alarm be cleared 
          after playing? (defaults to False)
        """
        self.current_alarm = title
        print self.current_alarm
        pygame.mixer.init()
        pygame.mixer.music.load(self.sound)
        pygame.mixer.music.play(-1)
        if only_once:
            return schedule.CancelJob
    
    def stop_alarm(self):
        """Stop the playback of the alarm"""
        self.current_alarm = None
        pygame.mixer.music.stop()

    def next_alarm(self):
        """Returns the datetime object of next scheduled alarm"""
        return schedule.next_run()
