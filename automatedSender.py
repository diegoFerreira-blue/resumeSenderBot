from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import datetime
import time
from dateutil.parser import parse

wait = int(7)

print('waiting')

class bcolors:
    YELLOW = '\033[93m'
    PINK = '\033[91m'


n_cvs_sent = 0
#chromedriver version must be the same with browser chromium
driver_path = 'path to the most recent chromedriver here'

#Open and read cv
cv = open('path to your cv here')
conteudo = cv.read()

#Open and read data.txt
d = open('path to your cv in txt here', encoding="utf-8-sig")
last_date = d.read()
parsed_last_date = parse(last_date)


#path to broswer.exe
browser_path = 'path to your browser here'

#choosing Brave as default broswer
option = webdriver.ChromeOptions()
#option.binary_location = brave_path
#option.add_argument("--disable-extensions") #disabling extensions
#option.add_argument("--start-maximized")
# option.add_argument("--incognito") OPTIONAL
# option.add_argument("--headless") OPTIONAL

#create new instance of Chrome
browser = webdriver.Chrome(executable_path=driver_path, options=option)

#Address
browser.get("https://www.empregasaojose.com.br/")

browser.implicitly_wait(wait)
time.sleep(wait)
print(f"{bcolors.PINK}Browser open with a delay of {wait}sec")


#-----------------------------------------------------------------------

#All elements in the page that have class as specified
wild_card_pages = browser.find_elements_by_css_selector("*[class^='page-numbers']")
current_page = browser.find_element_by_css_selector("span[class^='page-numbers current']")

#Date to be saved in the .txt file
data = browser.find_elements_by_class_name("value-title")
recent_date = data[0].text

move_on_to_next_page = False
searching = True
#Begin by a bool that is set to True

while searching is True:

    #Finds the elements that hold the date value
    data = browser.find_elements_by_class_name("value-title")
    #A variable that marks how many dates there are in the current page
    n_datas_pagina = len(data)
    contador = 0

    #Iterates as many times as there is dates
    for d in range(n_datas_pagina):

        #Finds the date again and transform the current date in the list into a datetime obj
        data = browser.find_elements_by_class_name("value-title")
        parsed_current_date = parse(data[d].text)
        
        
        #Checks if the current date is bigger than the date in the data.txt file
        if parsed_current_date > parsed_last_date and move_on_to_next_page is False:
            
            #Finds button in the page and count them
            canditar_btn = browser.find_elements_by_css_selector('a[title^="Candidatar-se"]')
            
            #A variable that marks how many canditate buttons there are in the current page
            n_vagas = len(canditar_btn)
            browser.implicitly_wait(wait)
            time.sleep(wait)

 
            #Iterates as many times as there are buttons
            
            for i in range(n_vagas):
                
                #Finds the button again since refreshing the page cause the elements to be
                #rebuild
                canditar_btn = browser.find_elements_by_css_selector('a[title^="Candidatar-se"]')
                
                print('indice: ', end='')
                print(i)
                print('Tamanho da lista de botões: ', end ='')
                print(len(canditar_btn))
                
                canditar_btn[i].click()
                browser.implicitly_wait(wait)
                time.sleep(wait)               
                
                #Finds the and fill the name field
                browser.implicitly_wait(wait)
                nome_campo = browser.find_element_by_id("your-name")
                nome_campo.clear()
                nome_campo.send_keys("your name here")


                #Finds and fill the e-mail field
                browser.implicitly_wait(wait)
                email_campo = browser.find_element_by_id("your-email")
                email_campo.clear()
                email_campo.send_keys("your e-mail here")
                
                #Finds and fill the phone field
                browser.implicitly_wait(wait)
                tel_campo = browser.find_element_by_id("your-tel")
                tel_campo.clear()
                tel_campo.send_keys('your phone here')

                #Finds and fill the content field
                browser.implicitly_wait(wait)
                msg_campo = browser.find_element_by_id('your-message')
                msg_campo.clear()
                msg_campo.send_keys(conteudo)

                #Finds the send button
                enviar_CSS_selector_btn = browser.find_element_by_css_selector("input[class^='wpcf7-']")
                browser.implicitly_wait(wait)
                time.sleep(wait) 

                try:
                    #Finds and send archive if element is present
                    arquivo_btn = browser.find_element_by_name('file-254')
                    arquivo_btn.send_keys('your cv in .word or .odt format')
                except NoSuchElementException:
                    contador += 1
                    print('Sem necessidade de envio por arquivo ' + str(contador))


                enviar_CSS_selector_btn.submit()
                print('cv sent')
                n_cvs_sent += 1
                print('Number of cvs sent: ', end="")
                print(n_cvs_sent)
                browser.implicitly_wait(wait)
                time.sleep(wait) 

                browser.execute_script("window.history.go(-1)")
                browser.implicitly_wait(wait)
                
                time.sleep(wait)
           
                #If counter is equal or greater than the number of job offers, 
                # set move_on_to_next_page to true  
                if i >= (n_vagas - 1):
                        print('Move on')
                        move_on_to_next_page = True
                        break

        #If current date less or equal than last date, finish process   
        elif parsed_current_date <= parsed_last_date:
            
            #Variable that switches off the whole loop
            searching = False
            print('ending search')

            #update data.txt to the most recent date on page
            d = open('path to data,txt in the project here', 'w')
            update_date = d.write(recent_date)
            d.close()
            
            break

        else:
            #if move_on_to_next_page is true.

            #Finds the element span that marks the current page...
            current_page = browser.find_element_by_css_selector("span[class^='page-numbers current']")
            #And parse its value to string and int and actual index number of the list
            current_index = int(current_page.text) - 1    
            next_page = current_index + 1
            current_page_str = current_page.text
            

            print('current page ' + current_page_str)
            #All(*) elements in the page that have class as specified
            wild_card_pages = browser.find_elements_by_css_selector("*[class^='page-numbers']")
           
           #Select the next page on the wild_card_pages, and set move_on_to_next_page to false
            browser.implicitly_wait(wait)
            time.sleep(wait)
            wild_card_pages[next_page].click()
            move_on_to_next_page = False
            print(f'{bcolors.YELLOW}Moved to page ' + str(next_page + 1))
            print('move to next page:')
            

            

            
            
