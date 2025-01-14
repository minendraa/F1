from tabulate import tabulate
import sys

# Initializing an empty dictionary to store data of lap times and driver information
dictionary = {}

# Function to add data to dictionary from the files
def addtodict():
    global dictionary, r, r1, r2, r3
    try:
        # Opening files for reading lap times and driver information
        r = open("f1_drivers.txt", 'r')
        r1 = open("lap_times_1.txt", 'r')
        r2 = open("lap_times_2.txt", 'r')
        r3 = open("lap_times_3.txt", 'r')
        #Taking out the information from the txt files.
        for x in r.readlines():
            x = x.strip('\n')
            driverinfo = x.split(',')
            dictionary[driverinfo[1]] = {
                'Detail': {
                    'Number': driverinfo[0],
                    'Name': driverinfo[2],
                    'Team': driverinfo[3]
                }
            }
            #Error handling. 
    except FileNotFoundError:
        print("File not found! Please ensure all files are available.")
        sys.exit(1)

#Function call to initialize the dictionary.
addtodict()

# Function to add lap values for each race to the dictionary
def lap_values(rn, n):
    nlaps = {} 
    next(rn)
    for x in rn.readlines():
        x=x.strip('\n')
        if x[0:3] in nlaps.keys():
            nlaps[x[:3]].append(float(x[3:]))
        else:
            nlaps[x[:3]]=[]
            nlaps[x[:3]].append(float(x[3:]))
    for key,value in nlaps.items():
        dictionary[key]=dictionary[key] | {f'lap{n}':value}
  
    for key, value in nlaps.items():
        dictionary[key][f'lap{n}'] = value

#Add lap times for all races.
lap_values(r1, 1)
lap_values(r2, 2)
lap_values(r3, 3)

def race_name(grandprix):
    #This function gives the name of the grandprix.
    grandprix.seek(0)
    print(f"The name of the grand prix is {grandprix.readlines(1)[0].strip()}")

def fastest(lap):
    #This function gives the fastest lap time for each grandprix.
    driver=[]
    top=1000
    for data,time in dictionary.items():
        if min(time[lap])<top:
            driver.clear()
            top=min(time[lap])
            driver.append(data)
    print(f"The fastest in {lap} is {driver[0]}[{dictionary[driver[0]]['Detail']['Name']}] with speed {top}.")

def fastesttimeforeach():
    #This function gives the fastest lap time for each driver from all grandprix.
    driver = []
    for x, y in dictionary.items():
            time = min([min(y['lap1']), min(y['lap2']), min(y['lap3'])])
            driver.append([x, y['Detail']['Number'], y['Detail']['Name'], y['Detail']['Team'], time])
    def position(Fastesttime):
        return Fastesttime[4]
    driver.sort(key=position)
    print("The fastest time for each driver is: ")
    print(tabulate(driver, headers=["Driver", "Number", "Name", "Team", "Fastest Time"], tablefmt="grid"))

def averagetimeoverall():
    #This funstion gives the overall average laptime from all grandprix and all drivers.
    driver=[]
    for x,y in dictionary.items():
        driver+=(y['lap1'])
        driver+=(y['lap2'])
        driver+=(y['lap2'])
        averagetimeoverallis=sum(driver)/len(driver)
    print(f"The overall average time of all th drivers is : {averagetimeoverallis:.3f} ")

def personalaverage():
    #This function gives the average laptime for each driver.
    driver=[]
    def position(fastesttime):
        return fastesttime[4]
    for x,y in dictionary.items():
        laptime=[]
        laptime+=(y['lap1'])
        laptime+=(y['lap2'])
        laptime+=(y['lap3'])
        personalavg=sum(laptime)/len(laptime)
        driver.append([x,y['Detail']['Number'],y['Detail']['Name'],y['Detail']['Team'],personalavg])
        driver.sort(key=position)
    print("The average time of each drive is: ")
    print(tabulate(driver,headers=["Driver","Number","Name","Team","Average Time"],tablefmt='grid'))

def desfastestforeach():
    #This function gives the fastest lap time for each driver from all grandprix.
    driver = []
    for x, y in dictionary.items():
            time = min([min(y['lap1']), min(y['lap2']), min(y['lap3'])])
            driver.append([x, y['Detail']['Number'], y['Detail']['Name'], y['Detail']['Team'], time])
    def position(Fastesttime):
        return Fastesttime[4]
    driver.sort(key=position,reverse="True")
    print("The fastest time for each driver in descending order is: ")
    print(tabulate(driver, headers=["Driver", "Number", "Name", "Team", "Fastest Time"], tablefmt="grid"))
   
def main():
#This function handles the user input.
    try:
        i = sys.argv[1]
        if i == '1':
            race_name(r1)
            race_name(r2)
            race_name(r3)
        elif i == '2':
            fastest('lap1')
            fastest('lap2')
            fastest('lap3')
        elif i == '3':
            fastesttimeforeach()
        elif i == '4':
            averagetimeoverall()
        elif i == '5':
            personalaverage()
        elif i == '6':
            desfastestforeach()
        elif i == '7':
            print("Goodbye User!")
            sys.exit(1)
        else:
            print("Invalid input! Please provide a valid option.")
    #Handles missing command-line argument.
    except IndexError:
        print("No argument provided. Please provide a valid input.")
#Calling the main function. 
main()
