# -*- coding: utf-8 -*-

import os
import logging
import json
import time
import datetime
import re
import calendar

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Raijin:

    def __init__(self):
        self.__tariffs = self.loadTariffs(logger)
        self.__holidays = self.loadHolidays(logger)

    @staticmethod
    def loadTariffs(logger):
        print(bcolors.WARNING)

        if logger.getEffectiveLevel() != logging.DEBUG:
            logger.debug("Running in Debug Mode")

        try:
            with open(os.path.dirname(os.path.realpath(__file__))+'/config/tariffs.json') as tariff_file:
                tariffs = json.load(tariff_file)
                logger.debug("Loaded: config/tariffs.json")
        except IOError:
            print("Error loading tariffs.json!")
            exit()

        print(bcolors.ENDC)
        return (tariffs)

    @staticmethod
    def loadHolidays(logger):
        print(bcolors.WARNING)

        if logger.getEffectiveLevel() != logging.DEBUG:
            logger.debug("Running in Debug Mode")

        try:
            with open(os.path.dirname(os.path.realpath(__file__))+'/config/holidays.json') as hollydays_file:
                hollidays = json.load(hollydays_file)
                logger.debug("Loaded: config/holidays.json")
        except IOError:
            print("Error loading holidays.json!")
            exit()

        print(bcolors.ENDC)
        return (hollidays)

    def getTariff(self, name, datetime=None):

        if datetime is None:
            time = self.getCurTime()
            date = self.getCurDate()
        else:
            if self.checkDateTime(datetime) != True:
                return self.checkDateTime(datetime)
            time = datetime.split(" ")[1]
            date = datetime.split(" ")[0]

        # Fix winter/summer time
        if(name == "3.1"):
            date = self.changeTime(date)

        for tariff in self.__tariffs["tariffs"]:
            if tariff["name"] == name:
                if(tariff["workable-discrimination"] == True):
                    for grid in tariff["grid"]:
                        if self.isWorkable(date) == grid["workable"]:
                            nMonth = 0
                            for month in grid["month"]:
                                nMonth += 1
                                if month and nMonth == self.getMonth(date):
                                    for period in grid["peak"]:
                                        if self.inTime(time, period):
                                            return "peak"
                                    for period in grid["flat"]:
                                        if self.inTime(time, period):
                                            return "flat"
                                    for period in grid["valley"]:
                                        if self.inTime(time, period):
                                            return "valley"

                else:
                    for grid in tariff["grid"]:
                        nMonth = 0
                        for month in grid["month"]:
                            nMonth += 1
                            if month and nMonth == self.getMonth(date):
                                for period in grid["peak"]:
                                    if self.inTime(time, period):
                                        return "peak"
                                for period in grid["flat"]:
                                    if self.inTime(time, period):
                                        return "flat"
                                for period in grid["valley"]:
                                    if self.inTime(time, period):
                                        return "valley"
        return None

    def isWorkable(self, date):
        if self.checkDate(date) != True:
            return self.checkDate(date)
        day = int(date.split("-")[0])
        month = int(date.split("-")[1])
        year = date.split("-")[2]
        for cday in self.__holidays[year][month - 1]:
            if cday == day:
                return False

        if self.getWeekDay(date) == 6 or self.getWeekDay(date) == 7:
            return False

        return True

    def checkDateTime(self, datetime):
        data = {}
        sdatetime = datetime.split(" ")
        if len(sdatetime) != 2:
            data["message"] = "Wrong datetime format. Try with: " + self.getCurDate() + " " + self.getCurTime()
            return data
        if self.checkDate(sdatetime[0]) != True:
            return self.checkDate(sdatetime[0])
        if self.checkTime(sdatetime[1]) != True:
            return self.checkTime(sdatetime[1])

        return True

    @staticmethod
    def checkDate(date):
        data = {}
        pattern_date = re.compile("^([0-9]{2}-[0-9]{2}-[0-9]{4})$")
        if not pattern_date.match(date):
            data["message"] = "Wrong date format. Expected format: [0-9]{2}-[0-9]{2}-[0-9]{4}"
            return data

        return True

    @staticmethod
    def checkTime(time):
        data = {}
        pattern_time = re.compile("^([0-9]{2}:[0-9]{2}(:[0-9]{2})*)$")
        if not pattern_time.match(time):
            data["message"] = "Wrong time format. Expected format: [0-9]{2}:[0-9]{2}:[0-9]{2} or [0-9]{2}:[0-9]{2}"
            return data

        return True

    @staticmethod
    def checkYear(year):
        data = {}
        pattern_year = re.compile("^([0-9]{4})$")
        if not pattern_year.match(year):
            data["message"] = "Wrong year format. Expected format: [0-9]{4}"
            return data

        return True

    def getHolidays(self, year=None, prettify=False):
        if year is not None:
            if self.checkYear(str(year)) != True:
                return self.checkYear(str(year))

        if prettify:
            prettified = {}
            year_holidays = []
            if year is None:
                for year in self.__holidays:
                    for month in range(1, 12):
                        for day in self.__holidays[year][month-1]:
                            year_holidays.append(str(day).zfill(2) + '-' + str(month).zfill(2) + '-' + year)
                    prettified[year] = year_holidays
                    year_holidays = []
            else:
                for month in range(1, 12):
                    for day in self.__holidays[str(year)][month-1]:
                        year_holidays.append(str(day).zfill(2) + '-' + str(month).zfill(2) + '-' + str(year))
                prettified[str(year)] = year_holidays

            return prettified

        else:
            if year is None:
                return self.__holidays
            else:
                return {str(year): self.__holidays[str(year)]}

    @staticmethod
    def getMonth(date):
        return int(date.split("-")[1])

    @staticmethod
    def getWeekDay(date):
        sdate = date.split("-")
        return datetime.date(int(sdate[2]), int(sdate[1]), int(sdate[0])).isoweekday()

    @staticmethod
    def getCurDate():
        return time.strftime("%d-%m-%Y")

    @staticmethod
    def getCurTime():
        return time.strftime("%H:%M:%S")

    @staticmethod
    def inTime(time, interval):
        a = interval.split("-")[0]
        if len(a) == 5:
            a = a+":00"
        b = interval.split("-")[1]
        if len(b) == 5:
            b = b + ":00"

        if(b == "00:00:00"):
           b = "24:00:00"

        if time >= a and time <= b:
            return True
        else:
            return False

    @staticmethod
    def lastSunday(date):
        sdate = date.split("-")
        cal = calendar.Calendar()
        month = cal.monthdatescalendar(int(sdate[2]), int(sdate[1]))
        #lastweek = month[-1]
        #sunday = lastweek[-1]
        if month[-1][-1].month > int(sdate[1]):
            sunday = month[-2][-1]
        else:
            sunday = month[-1][-1]
        return sunday

    # Manage the changes between summer time and winter time
    def changeTime(self, date):
        sdate = date.split("-")
        if sdate[1] == "03" or sdate[1] == "10":
            cdate = datetime.date(int(sdate[2]), int(sdate[1]), int(sdate[0]))
            if cdate >= self.lastSunday(date):
                cdate = cdate + datetime.timedelta(days=7)
                return cdate.strftime('%d-%m-%Y')
            else:
                return date
        else:
            return date

    def timeChange(self, date=None):
        if date is None:
            sdate = self.getCurDate().split("-")
        else:
            if self.checkDate(date) != True:
                return self.checkDate(date)
            sdate = date.split("-")

        cdate = datetime.date(int(sdate[2]), int(sdate[1]), int(sdate[0]))
        if int(sdate[1]) >= 3 and int(sdate[1]) <= 10:
            if cdate >= self.lastSunday("15-03-"+sdate[2]) and cdate < self.lastSunday("15-10-"+sdate[2]):
                days_left = self.lastSunday("15-10-" + sdate[2]) - datetime.date(int(sdate[2]), int(sdate[1]), int(sdate[0]))
                days_left = days_left.days
                return self.lastSunday("15-10-"+sdate[2]).strftime("%d-%m-%Y"), days_left
        if int(sdate[1]) <= 3 or int(sdate[1]) >= 10:
            if cdate < self.lastSunday("15-03-" + sdate[2]):
                days_left = self.lastSunday("15-03-" + sdate[2]) - datetime.date(int(sdate[2]), int(sdate[1]), int(sdate[0]))
                days_left = days_left.days
                return self.lastSunday("15-10-" + sdate[2]).strftime("%d-%m-%Y"), days_left
            if cdate >= self.lastSunday("15-10-" + sdate[2]):
                days_left = self.lastSunday("15-03-" + str(int(sdate[2])+1)) - datetime.date(int(sdate[2]), int(sdate[1]), int(sdate[0]))
                days_left = days_left.days
                return self.lastSunday("15-03-" + str(int(sdate[2])+1)).strftime("%d-%m-%Y"), days_left