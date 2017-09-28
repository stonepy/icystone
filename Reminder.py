"""
    Reminder programme
"""


"""
    Import required packages
"""
import sys
import os
import time
import datetime
import calendar
import pandas as pd

from datetime import datetime




# e.g. 2017.09.25 & 2017.11.22
startDate = "2017.09.25"
endDate = "2017.11.22"
givenDate = "2017.10.05"

database_path = "database.db"
databaseTmp_path = "database_tmp.db"



"""
    For schedule time summary
"""
class summary:


    def __init__(self):
        self.dayObj = self.dayStartEndObj()


    """

    """
    def dayStartEndObj(self):
        dateSet = [startDate, endDate, givenDate]
        dayObjs  = []

        for date in dateSet:
            year, month, day = date.split(".")
            dayObjs.append(datetime(int(year), int(month), int(day)))

        # This day object contains objects for time(days) difference calculation
        return dayObjs


    """
        Calculator for days passed and left
    """
    def dayPassLeft(self, dayStart, dayEnd, anyday):

        daypass = (anyday - dayStart).days
        dayleft = (dayEnd - anyday).days

        return daypass, dayleft


    """
        Calculate days passed and left from today
    """
    def todayPassLeft(self):
        dayStart, dayEnd, dayNow = self.dayObj[0], self.dayObj[1], datetime.now()
        timepass, timeleft = self.dayPassLeft(dayStart, dayEnd, dayNow)

        print("To today, days passed:", timepass)
        print("From today, days left:", timeleft)

    """
        Calculate days passed and left from any selected day
    """
    def anydayPassLeft(self):
        dayStart, dayEnd, dayGiven = self.dayObj[0], self.dayObj[1], self.dayObj[2]
        timepass, timeleft = self.dayPassLeft(dayStart, dayEnd, dayGiven)

        print("To the selected day, days passed:", timepass)
        print("From the selected day, days left:", timeleft)


"""
    For database process
"""
class database:

    """
    try:
        db_df = pd.read_table(database_path)
    except Exception as e:
        print(e, "\nTried to use the default method to read the schedule database, but encounter some problems...\n")
        try:
            db = open(database_path, "w+")
        except IOError as e:
            print(e, "\nSorry, your schedule database could not be reached.\n")
            sys.exit()
    """


    def __init__(self):

        dayObj = summary().dayStartEndObj()

        # Get total days of the schedule
        self.total_days = (dayObj[1] - dayObj[0]).days
        self.first_date = dayObj[0]
        self.last_date  = dayObj[1]


    """
        Record in formed format
    """
    def write_in_format(self, db, No, weekday, date, task, memo):
        db.write("{NO}\t{Weekday}\t{Date}\t{Task}\t{Memo}\n".format(NO=No, Date=date, Weekday=weekday, Task=task, Memo=memo))


    """
        Schedule creator (default)
    """
    def sch_databaseCreator_default(self):

        title = "NO\tWeekday\tDate\tTask\tMemo\n"
        db_list = []

        # Examine the 'database.db'
        try:
            with open(database_path, "r") as db:
                for l in db:
                    db_list.append(l)

                for l in db_list:
                    if l.startswith("#") or len(l.strip()) == 0:
                        continue

                    elif l.strip() != title.strip():
                        tmp = open(databaseTmp_path, "a+")
                        for l in db_list:
                            tmp.write(l)
                        tmp.close()
                        print("\nSchedule database was empty or the data was not saved in standard format, thus the data has been move to %s.\n" % databaseTmp_path)
                        break
            db = open(database_path, "w+")

        except IOError as e:
            print(e, "\nYour schedule database did not exist. Trying to build one ...\n")
            try:
                db = open(database_path, "w+")

            except IOError as e:
                print(e, "\nSorry, your schedule database could not be built.\n")
                sys.exit()

        # Create the title part
        db.write("## Created time: %s\n\n" % str(datetime.now()))
        db.write(title)

        # Create the content part
        secs_of_aday = 24 * 60 * 60
        firstdate_timestamp = self.first_date.timestamp()
        for i in range(self.total_days):
            No = i + 1

            thedate_timestamp = firstdate_timestamp + secs_of_aday * i
            year, month, mday, hour, min, sec, wday, yday, tm_isdst = time.gmtime(thedate_timestamp)
            weekday = wday + 1
            date = "%d-%d-%d" % (year, month, mday)
            task = "-"
            memo = "-"
            self.write_in_format(db, No, weekday, date, task, memo)

        db.close()

    """
        Schedule reader (default)
    """
    def sch_databaseReader_default(self):
        self.db.close()

    """
        Schedule writter (default)
    """
    def sch_databaseWritter_default(self):
        self.db.close()



    """
        Schedule creator (pandas)
    """
    def sch_databaseCreator_pandas(self):
        pass

    """
        Schedule reader (pandas)
    """
    def sch_databaseReader_pandas(self):
        pass

    """
        Schedule writter (pandas)
    """
    def sch_databaseWritter_pandas(self):
        pass







def main():

    database().sch_databaseCreator_default()



if __name__ == "__main__":
    main()
