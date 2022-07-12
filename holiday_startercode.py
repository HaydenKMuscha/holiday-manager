import datetime
import json
import csv
from tkinter import Menu
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass, field
import time
import calendar
from config import loadloc
from config import saveloc

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
      
    name: str
    date: datetime
    def __str__ (self):
        # String output
        # Holiday output when printed.
        return (f'{self.name}({self.date:%Y-%m-%d})')
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
@dataclass
class HolidayList:
   
    innerHolidays: list
   
    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        if type(holidayObj) is not Holiday:
            print("That is not a holiday.")
            return False
        # Use innerHolidays.append(holidayObj) to add holiday
        else:
            self.innerHolidays.append(holidayObj)
            # print to the user that you added a holiday
            print(f'{holidayObj.name} has been added')
            return True

    def findHoliday(self, HolidayName, date):
        # Find Holiday in innerHolidays
        for h in self.innerHolidays:
            # Return Holiday
            if HolidayName == h.name and date == h.date:
                return h
            return False

    def removeHoliday(self, HolidayName, date):

        for h in self.innerHolidays:
            # Find Holiday in innerHolidays by searching the name and date combination.
            if h.name == HolidayName and h.date == date:
                # remove the Holiday from innerHolidays
                self.innerHolidays.remove(h)
                # inform user you deleted the holiday
                print(f'{HolidayName} has been removed')
            
            else:
                print(f'{HolidayName} not found')

    def read_json(self, filelocation):
        # Read in things from json file location
        with open (filelocation, 'r') as file:
            data = json.load(file)['holidays']
            # Use addHoliday function to add holidays to inner list.
            for h in range (len(data)):
                newholidayname = data[h]['name']
                newholidaydate = data[h]['date']
                newholiday = Holiday(newholidayname, newholidaydate)
                self.addHoliday(newholiday)

    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        with open(filelocation, "w") as file:
            holiday_dictionary = []

            for h in self.innerHolidays:
                newholdiay = {'name':h.name, 'date':h.date}
                holiday_dictionary.append(newholdiay)
            
            json.dump(holiday_dictionary, file)
        
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022

        for y in range(2020, 2025):
            url = (f"https://www.timeanddate.com/holidays/us/{y}?hol=33554809")
            response = requests.get(url).text
            soup = BeautifulSoup(response, 'html.parser')
            table = soup.find('table', attrs={'id':'holidays-table'})
            tablebody = table.find('tbody')

            for row in tablebody.find_all('tr', attrs={'class':'showrow'}):
                    holidayname = row.find_all('td')[1].text
                    holidaydatestring = row.find('th').text
                    holidayyear = (f"{y} {holidaydatestring}")
                    formatteddate = datetime.datetime.strptime(holidayyear, "%Y %b %d")

                    # Check to see if name and date of holiday is in innerHolidays array
                    # Add non-duplicates to innerHolidays
                    repeathyoliday = self.findHoliday(holidayname, formatteddate)

                    if repeathyoliday == False:
                        addholiday = Holiday(holidayname, formatteddate)
                        self.innerHolidays.append(addholiday)

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)
        
    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the datetime object
        # Cast filter results as list
        holidaysweek = list(filter(lambda h: h.date.isocalendar()[0] == year and h.date.isocalendar()[1] == week_number, self.innerHolidays))
        # return your holidays
        self.displayHolidaysInWeek(holidaysweek)

    def displayHolidaysInWeek(self, HolidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        for h in HolidayList:
            print(h)

        #def getWeather(weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        # Use the datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        now = datetime.date.today()
        thisyear = now.year
        thisweek = now.isocalendar()[1]
        thisweekholidays = self.filter_holidays_by_week(thisyear, thisweek)
        self.displayHolidaysInWeek(thisweekholidays)

#ensuring entered date is valid
def isdatevalid(date):
    global dateisvalid

    try:
        dateisvalid = bool(datetime.datetime.strptime(date, '%Y-%m-%d'))

    except:
        dateisvalid = False
        print('Please enter the date in YYYY-MM-DD format.')

#initial text
def initialtext():
    print('Holiday Management')
    print('====================')
    print(f'There are {listofholidays.numHolidays()} holidays in the system')

#user start menu
def startmenu(self):
    print('Holiday Menu')
    print('===================')
    print('1. Add a Holiday')
    print('2. Remove a Holiday')
    print('3. Save Holiday List')
    print('4. View Holidays')
    print('5. Exit')



def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
    global loadloc
    global saveloc
    global listofholidays
    listofholidays = HolidayList([])
    listofholidays.read_json(loadloc)
    listofholidays.scrapeHolidays()

    initialtext()
    running = True

    while running == True:

        try:
            print('Holiday Menu')
            print('===================')
            print('1. Add a Holiday')
            print('2. Remove a Holiday')
            print('3. Save Holiday List')
            print('4. View Holidays')
            print('5. Exit')
            menuchoice = int(input('Choose your action 1 - 5: '))

            if menuchoice == 1:
                print('Add a Holiday')
                print('================')
                newholiday = str(input("Holiday: "))
                newdate = str(input("Date YYYY-MM-DD format: "))

                correctlystructureddate = isdatevalid(newdate)

                while correctlystructureddate == False:
                    print('The date entered was not in the YYYY-MM-DD format')
                    newdate = str(input('Date: '))
                    correctlystructureddate = isdatevalid(newdate)
                
                print("Date added successfully.")
                listofholidays.addHoliday(Holiday(newholiday, newdate))

            elif menuchoice == 2:
                print('Remove a Holiday')
                print('=================')
                newholiday = str(input("Holiday: "))
                newdate = str(input("Date YYYY-MM-DD format: "))

                correctlystructureddate = isdatevalid(newdate)

                while correctlystructureddate == False:
                    print('The date entered was not in the YYYY-MM-DD format')
                    newdate = str(input('Date: '))
                    correctlystructureddate = isdatevalid(newdate)
                
                print("Date removed successfully.")
                listofholidays.removeHoliday(Holiday(newholiday, newdate))

            elif menuchoice ==3:
                print('Save Holiday List')
                print('==================')
                saving = True
                while saving == True:
                    savechoice = input("Are you sure you want to save your changes? [y/n]: ")
                    
                    if savechoice == "y":
                        print("Success:")
                        print("Your changes have been saved.")
                        listofholidays.save_to_json(saveloc)
                        saving = False
                    elif savechoice == "n":
                        print("Cancelled:")
                        print("Holiday list file save canceled.")
                        saving = False
                    else:
                        print('That is not a valid response.')

            elif menuchoice == 4:
                print('View Holidays')
                print('===============')

                viewyear = input('Year: ')
                viewweek = input('Week #[1-52, Leave blank for the current week]: ')
                #blank week
                if viewweek == '':
                    print('These are the holidays for this week:')
                    listofholidays.viewCurrentWeek()
                
                else:
                    print(f'These are the holidays for {viewyear} week #{viewweek}')
                    listofholidays.displayHolidaysInWeek(viewyear, viewweek)
            
            elif menuchoice == 5:
                print('Exit')
                print('=====')
                print('Are you sure you want to exit?')
                print('Your changes will be lost.')
                exitchoice = input('[y/n] ').lower()

                if exitchoice == 'y':
                    print('Goodbye!')
                    running = False
                if exitchoice == 'n':
                    print('Going to the menu.')
                    running = True
                else:
                    print('Invalid Entry. Going to the main menu.')
                    running = True
        except:
            print('Please enter numbers in the range of 1-5.')










if __name__ == "__main__":
    main()


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





