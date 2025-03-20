# creating a scraper to scrape from https://www.flightradar24.com/data/airlines/sq-sia/fleet 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
import time
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
from selenium.common.exceptions import TimeoutException , StaleElementReferenceException 
import os
from tqdm import tqdm 

class Scraper:
    def __init__(self):
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        self.driver = webdriver.Chrome(options=chrome_options)  
        self.wait = WebDriverWait(self.driver, 10) 
        self.linkstoAircrafts = {}
        self.flights = []
        self.planeID = ''
        self.aircraftTypeCode = ''
        self.operator = ''
        self.code = '' 
        self.modeS = ''
        self.serialNumber = '' 
        self.age = '' 
        self.remainingAircrafts = []

        self.airline = ''  # use this to form the link to the airline 
    def login(self,username,password):
        #!https://www.flightradar24.com/data/airlines/jl-jal/fleet
        #!https://www.flightradar24.com/data/airlines/sq-sia/fleet
        #!https://www.flightradar24.com/data/airlines/mm-apj/fleet
        #!https://www.flightradar24.com/data/airlines/nq-ajx/fleet
        #!https://www.flightradar24.com/data/airlines/nx-amu/fleet
        
        link = f"https://www.flightradar24.com/data/airlines/{self.airline}/fleet"
        self.driver.get(link) 
        #self.driver.maximize_window() 
        print("Page loaded")
        try:
            # click the cookie button 
            element = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            element.click()
            print ("clicked the cookie button") 
        except Exception as e: 
            print (e) 
            pass      
        # check if user is alreay logged in
        # if so skip the login process 
        # check if //span[@class='whitespace-nowrap text-xs uppercase'] . text is gold or log in 
        checkLoginElement = self.driver.find_element(By.XPATH, "//span[@class='whitespace-nowrap text-xs uppercase']")
        print (checkLoginElement.text) 
        #time.sleep(20)
        if checkLoginElement.text == "LOG IN": 
            print ("user is not logged in")  
            loginElement = self.driver.find_element(By.XPATH, "//div[@class='flex h-9 flex-col items-center justify-center text-white']")

            loginElement.click() 

            emailElement = self.driver.find_element(By.XPATH, "//input[@name='email']")  
            emailElement.send_keys(username) 

            passwordElement = self.driver.find_element(By.XPATH, "//input[@type='password']")
            passwordElement.send_keys(password) 

            submitButton = self.driver.find_element(By.XPATH, "//button[@type='submit']") 

            submitButton.click() 
        time.sleep(10)

    def extractOverviewInformation(self):
        # dictionary to store number of aircraft per type 
        numberofAircraftPerType = {} 
        listElement = self.driver.find_element(By.ID,"list-aircraft")
        aircrafts = listElement.find_elements(By.TAG_NAME, "dt")
        craftLinksElement = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"regLinks")))
        print (f"total number of aircrafts: {len(craftLinksElement)}")

        for item in craftLinksElement: 
            print ("item")
            #print(self.driver.execute_script("return arguments[0].textContent", item))
            aircraft = self.driver.execute_script("return arguments[0].textContent", item)
            # print (item)
            # print (item.get_attribute("href"))
            linkToAircraft = item.get_attribute("href") 
            print ("--------------------------------")
            self.linkstoAircrafts[aircraft] = linkToAircraft 
            self.remainingAircrafts.append(aircraft) 
    
    def scrapeAircraft(self,link):
        

        self.driver.get(link)

 
        try:
            clickCount = 0
            iteration = 0 
            print (f"iteration: {iteration}") 
            while True:
                
                try:
                    
                    # Wait until the "Load Earlier Flights" button is clickable
                    loadEarlierFlightsButton = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "btn-load-earlier-flights"))
                    )
                    # Click the button if found
                    loadEarlierFlightsButton.click()
                    clickCount += 1
                    print(f"Clicked the 'Load Earlier Flights' button {clickCount} times")
                    time.sleep(1.5)  # Wait for more data to load

                    # Reset retry counter after a successful click
                    #!retry_count = 0

                except TimeoutException:
                    print("Timeout waiting for the 'Load Earlier Flights' button.")

                    try:
                        # Check if the button is present in the DOM but not clickable
                        loadEarlierFlightsButton = self.driver.find_element(By.ID, "btn-load-earlier-flights")
                        if "loading" in loadEarlierFlightsButton.get_attribute("class"):  # Adjust class name if needed
                            print("Button is still loading. Refreshing the site...")
                            time.sleep(3)
                            self.driver.refresh() 
                            clickCount = 0 
                            iteration += 1 
                            
                            if iteration > 100: 
                                #log it in a csv file 
                                # log the planeID 
                                with open("data/UnScrapable.csv","a") as f: 
                                    f.write(f"{self.planeID}\n") 
                                return 
                            # if iterations less than or equates to 100 then continue  
                            print (f"iteration: {iteration}") 
                            continue

                        else: # loading not even in the class so i just gonna exit the loop with the data i have 
                            print("Button is not clickable. Exiting loop.")
                            break 
                    except Exception:
                        # Button not found in the DOM, indicating end of data
                        print("The 'Load Earlier Flights' button is no longer in the DOM. Reached the end of data.")
                        break

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        try: 
            # go and find typecode 
            typeCodeElement = self.driver.find_element(By.XPATH, "//label[text()='TYPE CODE']/following-sibling::span")
            self.aircraftTypeCode = typeCodeElement.text 

            # get operator
            operatorElement = self.driver.find_element(By.XPATH, "//label[text()='OPERATOR']/following-sibling::span") 
            self.operator = operatorElement.text 

            #get Code 
            codeElement = self.driver.find_element(By.XPATH, "//label[text()='Code']/following-sibling::span") 
            self.code = codeElement.text 

            #get mode S 
            modeSElement = self.driver.find_element(By.XPATH, "//label[text()='MODE S']/following-sibling::span") 
            self.modeS = modeSElement.text 

            #get serial number 
            serialNumberElement = self.driver.find_element(By.XPATH, "//label[text()='SERIAL NUMBER (MSN)']/following-sibling::span") 
            self.serialNumber = serialNumberElement.text

            #get age 
            ageElement = self.driver.find_element(By.XPATH, "//label[contains(text(), 'AGE')]/following-sibling::span")
            self.age = ageElement.text 
        except Exception as e: 

            return 


        datarowElements = self.driver.find_elements(By.CLASS_NAME, "data-row") 
        print (f"total number of data rows: {len(datarowElements)}") 
        #for flightDetails in datarowElements: 
        for flightDetails in tqdm(datarowElements): 
            # CREATE a new flight dictionary 
            flight = {'planeID':self.planeID,'aircraftTypeCode':self.aircraftTypeCode,'operator':self.operator,'code':self.code,'modeS':self.modeS,'serialNumber':self.serialNumber,'age':self.age} 
            # Headings for the flight details
            headings = ["DATE", "FROM", "TO", "FLIGHT", "FLIGHT TIME", "STD", "ATD", "STA", "ONTIME","STATUS"] # very hardcodish ignore for now
            # print every nested element 
            allTdElements = flightDetails.find_elements(By.TAG_NAME, "td")  
            details = [td.text for td in allTdElements[2:12]]  # Extract text from the relevant <td> elements
            color = allTdElements[10].find_element(By.TAG_NAME, "div").get_attribute("class").split()[-1] # [-1] so i can remove 'state-block' from state-block green

            details[-2] = color 
            flight.update(dict(zip(headings, details)))

            self.flights.append(flight) 
            #print ("----------------------") 


    def workflow(self,airline): 
        self.airline = airline 
        self.login("jinbetheshark@gmail.com","jinbe22400149google") 
        self.extractOverviewInformation()
        
        for planeID,link in self.linkstoAircrafts.items():
            print (f"number of remaining aircrafts: {len(self.remainingAircrafts)}") 
            print (f"remaining aircrafts: {self.remainingAircrafts}") 
            print ("--------------------------------") 
            self.planeID = planeID
            # check if the planeID already exist in flights.csv if it does skip it 
            try:
                df = pd.read_csv("flights.csv") 
                if planeID in df['planeID'].values:
                    print ("found planeID in flights.csv skipping") 
                    self.remainingAircrafts.remove(planeID) 
                    continue
            except FileNotFoundError: 
                pass

            # x.scrapeAircraft('https://www.flightradar24.com/data/aircraft/9v-shb') 
            print (link)
            time.sleep(5)   
            self.scrapeAircraft(link) 

            df = pd.DataFrame(self.flights) 
            print (df) 
            if len(df) == 0: 
                self.remainingAircrafts.remove(planeID) 
                continue 
            #check if flights.csv exists if not create it with index
            try:
                pd.read_csv("flights.csv")
                df.to_csv("flights.csv",mode='a',index=False,header=False) 
            except FileNotFoundError:
                df.to_csv("flights.csv",index=False)
            

            #reset the flight details for the next plane
            self.flights = [] 
            self.remainingAircrafts.remove(planeID) 

        # rename flights.csv to respective airline.csv
        airlineName = self.operator.replace(" ","-").lower()
        os.rename("flights.csv",f"data/{airlineName}_{self.airline}.csv") 


#? THE WORKFLOW OF THE SCRIPT 
#TODO newzealand zk-mva is removed from the list of aircrafts to scrape 
#TODO SOME HOW SQ MISSED 9v-sfo
airlineToScrape = ['jl-jal']
for airline in airlineToScrape: 
    x = Scraper() 
    x.workflow(airline)

