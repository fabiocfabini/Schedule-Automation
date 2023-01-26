from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as soup
from datefinder import find_dates
from Classes import Event
from datetime import datetime

PATH = r"./chromedriver" # Path to the WebDriver executable
UMINHO_URL = 'https://alunos.uminho.pt/pt/estudantes/paginas/infouteishorarios.aspx'
HALF_HOUR = 0.5


def makeEvent(s,start,end,weekday):
    aulaData = s.text.strip().replace("\n"," ").replace("\t", " ")
    aulaData = " ".join(aulaData.split())
    aulaData = aulaData.split(" [")
    aulaData2 = aulaData[1].split("] ")

    name = aulaData[0]
    room = aulaData2[0]
    type = aulaData2[1]

    return Event(name,room,type,start,end,weekday)

def getEventName(s):
    aulaData = s.text.strip().replace("\n"," ").replace("\t", " ")
    aulaData = " ".join(aulaData.split())
    aulaData = aulaData.split(" [")
    aulaData2 = aulaData[1].split("] ")

    name = aulaData[0]
    type = aulaData2[1]

    return name, type

def getEventDuration(Class, col):
    if(len(Class) == 1): 
        height = int(col.find("div", {"class": "rsApt rsAptSimple"})['style'].split(";")[1].replace("height:","").replace("px",""))

        return round(height/60)
    else:
        heights = col.findAll("div", {"class": "rsApt rsAptSimple"})
        heights = list(map(lambda x: int(x['style'].split(";")[1].replace("height:","").replace("px","")), heights))
        
        return list(map(lambda x: round(x/60), heights))

def getPageHtml(course, course_year, date: datetime, debug=False):
    """gets the html table corresponding to the schedule and the start of the  earliest class.

    Args:
        course (string): name of course
        course_year (string): year of course

    Returns:
        soup object: contains said html table
        int:  start of the earliest class (hour)
    """

    # Start Driver
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("window-size=1400,2100")
    if debug is False:
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("disable-gpu")

    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) -> if Chrome webDriver is not installed
    driver = webdriver.Chrome(ChromeDriverManager().install()) # -> if you have Chrome webdriver (Path must contain the path to the driver executable)
    driver.minimize_window()
    driver.get(UMINHO_URL)

    # Get the html
    username_btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='ctl00$ctl40$g_e84a3962_8ce0_47bf_a5c3_d5f9dd3927ef$ctl00$dataCurso']")))
    find_btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a[title='procurar']")))
    username_btn.send_keys(course)
    find_btn.click()
    find_btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a[title='procurar']")))
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,f"input[value='{course_year}']"))).click()
    find_btn.click()
    date_btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[id='ctl00_ctl40_g_e84a3962_8ce0_47bf_a5c3_d5f9dd3927ef_ctl00_dataWeekSelect_dateInput']")))
    find_btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a[title='procurar']")))
    #clear date
    date_btn.clear()
    date_btn.send_keys(f"{date.day}-{date.month}-{date.year}")
    find_btn.click()

    page_html = driver.page_source
    driver.close()

    # Get Schedule Table
    soup_page = soup(page_html, 'html.parser')
    time_body = soup_page.findAll("table", {"class": "rsVerticalHeaderTable"})
    start_time = int(time_body[0].th.div.text.strip().split(':')[0])
    Table = soup_page.find("table", {"class": "rsContentTable"}).findAll("tr") 

    return Table, start_time

def getScheduleData():
    """
    returns a list of all the classes in the schedule.
    Each class is a Event object.
    """
    
    # get all user input
    start_data = input('What day do your classes start (yyyy-mm-dd): ')
    end_data = input('What day do your classes end (yyyy-mm-dd): ')
    try:
        start_data = next(find_dates(start_data))
        end_data = next(find_dates(end_data))
    except StopIteration: 
        print("Please input a valid date.")
        return [], "", ""
    else:
        if(end_data < start_data):
            print("Your classes appear to finish before they even begin. Please check your date inputs.")
            return [], "", ""

    course = input("Course name (ex: Licenciatura em Engenharia Física): ")
    course_year = input("Course year (ex: 1): ")

    # fetch html and start time
    Table, start_time= getPageHtml(course, course_year, start_data)

    day_time = start_time
    classes = []

    for row in Table:
        week_day = 0

        content = row.findAll("td")
        for col in content:

            Class = col.findAll("div", {"class": "rsAptContent"})
            if(len(Class) == 1):

                hour = getEventDuration(Class, col)
                cls = makeEvent(Class[0], day_time, day_time+hour, week_day)
                classes.append(cls)

            elif(len(Class) > 1):
                stage = "pm"
                if 0 <= day_time <= 12: stage = "am"
                print(f"\nIt appears that your schedule has multiple classes at {int(day_time)}{stage} on a {Event.workDays[week_day]}.")
                
                hours = getEventDuration(Class,col)
                for i,cls in enumerate(Class):
                    print(f"\t{i} ->", getEventName(cls))
                
                try:
                    classIndex = int(input("Specify the Class with the proper number (ENTER for None): "))
                except ValueError:
                    classIndex = -1
                finally:
                    if(classIndex >= 0):
                        hour = hours[classIndex]
                        cls = makeEvent(Class[classIndex], day_time, day_time+hour, week_day)
                        classes.append(cls)

            week_day += 1

        day_time += HALF_HOUR

    return classes, start_data, end_data