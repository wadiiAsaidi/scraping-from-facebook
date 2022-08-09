import requests
import random
from time import sleep 
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import re
from secrets import username, password

#connection facebook
class ConnectionFacebook():

    def __init__(self):
        self.driver = webdriver.Chrome('C:/chromedriver')

    #The first time we login
    def login_facebook(self,username, password):
        self.driver.get("https://www.facebook.com/login")

        sleep(1)

        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(username)

        password_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        password_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')
        login_btn.click()

        sleep(1)


#create class facebookbot and let's find all the data
class FaceBookBot(ConnectionFacebook):

    def __init__(self):
        super().__init__()
    
    def find_url(self,n,page_name):

        self.login_facebook(username, password)

        REQUEST_URL = f'https://m.facebook.com/{page_name}'
        r=self.driver.get(REQUEST_URL)
        sleep(1)

        for i in range(1,n):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        
        comment_share=self.CommentShare(soup)
        
        all_date=self.published(soup)
        sent=[]

        sentiments=self.sentiment(soup)
        for i in range(len(sentiments)):
            sent.append(all_date[i])
        
        #extract all the id of status like: fbid=4315836428475514
        links = self.driver.find_elements_by_tag_name('a')
        posts = []
        for link in links:
            post = link.get_attribute('data-uri')
            if post is not None:
                posts.append(post)

        #dict of lists
        dict = {'ft ent identifier': self.get_id(posts),'published': sent,'reactions':sentiments,'comments_shares':comment_share}
        self.driver.close()
        return dict

    def CommentShare(self,soup):
        tuple=()
        comment_share=[]
        div=soup.find_all('div',class_="_1fnt")
        for item in div:
            if len(item)==0:
                tuple=(0,0)
            elif len(item)==1:
                if re.findall('[0-9]+ commentaires',item.get_text()) !=[] :
                    tuple=(re.findall('[0-9]+ commentaires',item.get_text()),0)
                else:
                    tuple=(0,re.findall('[0-9]+ partages',item.get_text()))
            
            elif len(item)==2:

                tuple=(re.findall('[0-9]+ commentaires',item.get_text()),re.findall('[0-9]+ partages',item.get_text()))
            #save comments and shares in list comment_share
            comment_share.append(tuple)
            

        return comment_share

    def sentiment(self,soup):
        sentiment=soup.find_all('div',class_="_1g06")
        #extract reacttion
        sentiments=[]
        for item in sentiment:
            if item.text is not None:
                sentiments.append(item.text)
            else:
                sentiments.append('')

        return sentiments

    def published(self,soup):
        published=soup.find_all('abbr')
        #extract date 
        all_date=[]
        for item in published:
            if item.text is not None:
                all_date.append(item.text)
            else:
                all_date.append('')

        return all_date


    def get_id(self,list):
        list_id=[]
        for item in list:
            id=re.findall('/?ft_ent_identifier=[0-9]+',item)
            list_id.extend(id)
        return list_id




#bot=FaceBookBot()
#dict=bot.find_url(5,'delicetunisie')
#print(dict)
        