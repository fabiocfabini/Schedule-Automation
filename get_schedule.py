from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import  WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from Classes import Classroom

PATH = r".\chromedriver.exe"
UMINHO_URL = 'https://alunos.uminho.pt/pt/estudantes/paginas/infouteishorarios.aspx'


def makeClassroom(s,start,end,weekday):
    aulaData = s.text.strip().replace("\n"," ").replace("\t", " ")
    aulaData = " ".join(aulaData.split())
    aulaData = aulaData.split(" [")
    aulaData2 = aulaData[1].split("] ")

    name = aulaData[0]
    room = aulaData2[0]
    type = aulaData2[1]

    return Classroom(name,room,type,start,end,weekday)

def getClassroomName(s):
    aulaData = s.text.strip().replace("\n"," ").replace("\t", " ")
    aulaData = " ".join(aulaData.split())
    aulaData = aulaData.split(" [")
    aulaData2 = aulaData[1].split("] ")

    name = aulaData[0]
    type = aulaData2[1]

    return name, type

def getClassroomDuration(Class, col):
    if(len(Class) == 1): 
        height = int(col.find("div", {"class": "rsApt rsAptSimple"})['style'].split(";")[1].replace("height:","").replace("px",""))

        return round(height/60)
    else:
        heights = col.findAll("div", {"class": "rsApt rsAptSimple"})
        heights = list(map(lambda x: int(x['style'].split(";")[1].replace("height:","").replace("px","")), heights))
        
        return list(map(lambda x: round(x/60), heights))

def getPageHtml(course, course_year):
    # Get driver to run in the background
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    # Start Driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(UMINHO_URL)

    # Get the html
    username_btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='ctl00$ctl40$g_e84a3962_8ce0_47bf_a5c3_d5f9dd3927ef$ctl00$dataCurso']")))
    find_btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a[title='procurar']")))
    username_btn.send_keys(course)
    find_btn.click()
    find_btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a[title='procurar']")))
    _btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,f"input[value='{course_year}']"))).click()
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
    start_data = input('What day do your classes start (yyyy-mm-dd): ')
    end_data = input('What day do your classes end (yyyy-mm-dd): ')
    course = input("Course name (ex: Licenciatura em Engenharia Física): ")
    course_year = input("Course year (ex: 1): ")

    Table, start_time= getPageHtml(course, course_year)

    day_time = start_time
    half_hour = 0.5
    classes = []

    for row in Table:
        week_day = 0

        content = row.findAll("td")
        for col in content:

            Class = col.findAll("div", {"class": "rsAptContent"})
            if(len(Class) == 1):

                hour = getClassroomDuration(Class, col)
                cls = makeClassroom(Class[0], day_time, day_time+hour, week_day)
                classes.append(cls)

            elif(len(Class) > 1):
                stage = "pm"
                if 0 <= day_time <= 12: stage = "am"
                print(f"\nIt appears that your schedule has multiple classes at {int(day_time)}{stage}h on a {Classroom.workDays[week_day]}.")
                
                hours = getClassroomDuration(Class,col)
                for i,cls in enumerate(Class):
                    print(f"\t{i} ->", getClassroomName(cls))
                
                try:
                    classIndex = int(input("Specify the Class with the proper number (ENTER for None): "))
                except ValueError:
                    classIndex = -1
                finally:
                    if(classIndex >= 0):
                        hour = hours[classIndex]
                        cls = makeClassroom(Class[classIndex], day_time, day_time+hour, week_day)
                        classes.append(cls)

            week_day += 1

        day_time += half_hour
    
    return classes, start_data, end_data