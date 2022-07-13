import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from config import loadloc
from config import saveloc

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
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
        return (f"{self.name} ({self.date})")
          
           
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
        if type(holidayObj) == Holiday:
            checkholiday = self.findHoliday(holidayObj.name, holidayObj.date)
            if checkholiday == False:
        # Use innerHolidays.append(holidayObj) to add holiday
                self.innerHolidays.append(holidayObj)
        # print to the user that you added a holiday
                print('Success:')
                print(f'{holidayObj} has been added.')
            else:
                print(f"{holidayObj.name}  is already in the system.")
        else:
            print('That is not a holiday object.')



    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        for holiday in self.innerHolidays:
        # Return Holiday
            if holiday.name == HolidayName and holiday.date == Date:
                return holiday
            else:
                checkholiday = False
                return checkholiday

    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        checkholiday = self.findHoliday(HolidayName, Date)
        #holiday not present
        if checkholiday == False:
            print("That holiday cannot be found.")
        #holiday is present
        else:
            self.innerHolidays.remove(checkholiday)
            print(f'{HolidayName} has been removed')
    
    def read_json(self, filelocation):
        # Read in things from json file location
        with open(filelocation, 'r') as jfile:
            data = json.load(jfile)['holidays']
            for i in range(len(data)):
                name = data[i]['name']
                date = data[i]['date']
                fixeddate = datetime.datetime.strptime(date, '%Y-%m-%d')
        # Use addHoliday function to add holidays to inner list.
                jsonholiday = Holiday(name, fixeddate)
                self.innerHolidays.append(jsonholiday)

            


    def save_to_json(self, filelocation):
        hdict = {}
        listdict = []
        for h in self.innerHolidays:
            stringdate = datetime.datetime.strftime(h.date, '%Y-%m-%d')
            hdict = {'name': h.name, 'date': stringdate}
            listdict.append(hdict)
        # Write out json file to selected file.
        with open(saveloc,'w') as file:
            json.dump(listdict, file, indent = 3)

    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.

        for y in range(2020, 2025):
            url = ("https://www.timeanddate.com/holidays/us/{}?hol=33554809")
            url = url.format(y)

            def getHTML(url):
                response = requests.get(url)
                return response.text
                
            html = getHTML(url)
                        
            soup = BeautifulSoup(html,'html.parser')

            table = soup.find('table', attrs = {'id': 'holidays-table'})
            for row in table.find_all('tr', class_ = 'showrow'):
                name = row.find_all('td')[1].text
                date =  row.find('th', attrs = {'class':'nw'}).text
                longDate = f'{y} {date}'
                correctDate = datetime.datetime.strptime(longDate, '%Y %b %d')
                dateObject = Holiday(name, correctDate)
                self.addHoliday(dateObject)


    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        holnum = len(self.innerHolidays)
        return holnum
    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        holidays = []
        holidays = list(filter(lambda holiday: holiday.date.isocalendar()[0] == year and holiday.date.isocalendar()[1] == week_number, self.innerHolidays))
        return holidays
        

    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        if len(holidayList) == 0:
            print("No holidays were fpunmd for that week.")
        else:
            for holiday in holidayList:
                print(holiday)


    
    #def getWeather(weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        week = datetime.now().isocalendar()[1]
        year = datetime.now().isocalendar()[0]
        self.displayHolidaysInWeek(self.filter_holidays_by_week(year, week))

def AddHolidayMenu():

        print('Add a Holiday')
        print('================')
        name = input('Holiday: ')
        date = input('Date YYYY-MM-DD format: ')
        isdatevalid = True
        try:
            validdate = datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            isdatevalid = False
        if isdatevalid == True:
            addedholiday = Holiday(name, validdate)
            return addedholiday
        else:
            print('Error - Date Invalid')
            main()

def RemoveHolidayMenu():
    print('Remove a Holiday')
    print('=================')
    name = input('Holiday: ')
    date = input('Date YYYY-MM-DD format: ')
    isdatevalid = True
    try:
        validdate = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        isdatevalid = False
    if isdatevalid == True:
        return name, validdate
    else:
        print('Error - Date not valid')
        main()

        


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

    running = True

    print("Holiday Management")
    print("====================")
    print(f"There are currently {listofholidays.numHolidays()} stored in the system.")

    while running:
        print('Holiday Menu')
        print('===================')
        print('1. Add a Holiday')
        print('2. Remove a Holiday (currently not functional)')
        print('3. Save Holiday List')
        print('4. View Holidays')
        print('5. Exit')
        menuchoice = int(input('Choose your action 1 - 5: '))
        
        #Add Holiday
        if menuchoice == 1:
            addedholiday = AddHolidayMenu()
            listofholidays.addHoliday(addedholiday)

        #Remove Holiday
        elif menuchoice == 2:
            name, date = RemoveHolidayMenu()
            listofholidays.removeHoliday(name, date)
        
        #Save to json
        elif menuchoice ==3:
                print('Save Holiday List')
                print('==================')
                savechoice = input("Are you sure you want to save your changes? [y/n]: ").lower()
                if savechoice == "y":
                        print("Success:")
                        print("Your changes have been saved.")
                        listofholidays.save_to_json(loadloc)
                elif savechoice == "n":
                        print("Cancelled:")
                        print("Holiday list file save canceled.")
                else:
                        print('That is not a valid response.')
        
        elif menuchoice ==4:
            print('View Holidays')
            print('===============')
            wrong_input = True
            while(wrong_input):
                try:
                    year = int(input("Which year?: "))
                    week = (input("Which week? #[1-53] Leave blank for the current week: "))
                    
                    if week != "":
                        if(int(week) <= 53 and int(week) >= 1):
                            wrong_input = False
                            week = int(week)
                            filtered_holidays = (listofholidays.filter_holidays_by_week(year, week))
                            if(len(filtered_holidays) == 0):
                                print("There are no holidays in this week")
                            else: 
                                listofholidays.displayHolidaysInWeek(filtered_holidays)
                        else:
                            print("Input is outside of the expected range. Please try again: ")
                    else:
                        listofholidays.viewCurrentWeek()
                        wrong_input = False
                except:    
                    print("Please input a valid input")
            

        elif menuchoice ==5:
            print('Exit')
            print('=====')
            print('Are you sure you want to exit?')
            print('Your changes will be lost.')
            exitchoice = input('[y/n] ').lower()

            if exitchoice == 'y':
                print('Goodbye!')
                running = False
            elif exitchoice == 'n':
                print('Going to the menu.')
                running = True
            else:
                print('Invalid Entry. Going to the main menu.')
                running = True
        


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





