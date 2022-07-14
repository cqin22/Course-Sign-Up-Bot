import smtplib
import ssl
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
open = False
count = 0

# Checks every hour for class avaliablity until class is found or X number of times
while open == False or count < 5:
    driver = webdriver.Chrome('/usr/local/bin/chromedriver 3')
    driver.get("https://sa.ucla.edu/ro/ClassSearch/Results?SubjectAreaName=Computer+Science+(COM+SCI)&CrsCatlgName=31+-+Introduction+to+Computer+Science+I&t=22F&sBy=subject&subj=COM+SCI&catlg=0031&cls_no=%25&undefined=Go&btnIsInIndex=btn_inIndex")
    page_source = driver.page_source
    time.sleep(2)

# Logs into your UCLA portal
    search = driver.find_element_by_id("logon")
    search.send_keys("ID")
    search.send_keys(Keys.RETURN)

    search = driver.find_element_by_id("pass")
    search.send_keys("PASSWORD")
    search.send_keys(Keys.RETURN)
    time.sleep(2)

# Locates class status
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    for p in soup.find_all('div', {'id':'187093200_COMSCI0031-status_data'}): # Find course's HTML ID through "Inspect Element"
        text = p.text

# Checks if class is full. If not, a email is sent to user
    if " 0 " in text:
        print("Your desired class is still full")
    else:  
        email_sender = 'EMAIL'
        email_password = 'SPECIAL PASSWORD'
        email_receiver = 'RECIPIENT EMAIL'

        subject = 'Check MyUCLA'
        body = """
        Hurry! https://my.ucla.edu
        """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        open = True

        time.sleep(2)
        search = driver.find_element_by_id("187093200_COMSCI0031-checkbox")
        search.click()
        time.sleep(2)

        search = driver.find_element_by_id("187093202_187093200_COMSCI0031-checkbox")
        search.click()
        time.sleep(2)

        search = driver.find_element_by_id("btn_addToPlanner_normal_flyout")
        search.click()
        time.sleep(6)

        driver.quit()
        quit()

    time.sleep(5)
    driver.quit()
    count += 1
    time.sleep(3600)
