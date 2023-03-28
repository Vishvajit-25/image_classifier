import tensorflow as tf
from tensorflow.keras.models import load_model
import warnings
warnings.simplefilter("ignore")
import numpy as np
import cv2
from bs4 import BeautifulSoup
import requests
Model=load_model('E:\Project1\ISO_NON_ISO_Classifier_Model_13_94_acc.h5')
import re
from flask import Flask, request
import time


def check(web,timeout):
  #timeout is specified by the user how long does he has to wait for a website to load. 
  start_time=time.time()
  #Scrapping the website.
  res=requests.get(web,headers={"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"},verify=False);
  soup = BeautifulSoup(res.text, "lxml")
  link=[]
  #Getting URL for all the links to all other associated pages.
  for i in soup.findAll('a'):
      m=i.get('href')
      if m!=None:
        try:
          if m[0]=='/' and web[-1]=='/':
              link.append(m.strip('/'))
          else:
              link.append(m)
        except:
          continue
  #Removing Duplicates 
  link=set(link)
  #Check URL for special conditions.
  if web.find('about')!=-1:
    web=web.split('about')
    web=web[0]
  if web.find('index')!=-1:
    web=web.split('index')
    web=web[0]
  ans=[]
  #Getting only specific pages to scrap as mentioned below such as overview page , about us page , etc . 
  for i in link:
    if i!=None:
      m=i.lower()
      if m.find('overview')!=-1 or m.find('about')!=-1 or m.find('certificat')!=-1 or m.find('quality')!=-1 or m.find('iso')!=-1:
        if i.find('https')!=-1:
          ans.append(i)
        else:
          ans.append(web+i)
      else:
          ans.append(web)
  #Removing Duplicates.
  ans=set(ans)
  images=[]
  #Getting all the Image URL from the links . 
  for i in ans:
    try:
        res=requests.get(i,headers={"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"},verify=False);
        soup = BeautifulSoup(res.text, "lxml")
        links = []
        for link in soup.findAll('img'):
            links.append(link.get('src'))
            links.append(link.get('nitro-lazy-src'))
            links.append(link.get('data-src'))
            for i in links:
              if i!=None:
                i=i.strip('/')
                if i.find('.jpg')!=-1 or i.find('.png')!=-1 or i.find('.jpeg')!=-1:
                  if i.find('http')!=-1:
                    images.append(i)
                  elif i.find('www')!=-1:
                    images.append('https://'+i)
                  else:
                    images.append(web+i)
    except:
      continue
  #Removing Duplicates.
  images=set(images)
  for i in images:
      i=i.strip('/')
      #print(i)
      #if the function has taken more time than timeout break the loop and return -1 .
      if (time.time()-start_time)>timeout:
        return -1
        break
      #We consider only png , jpeg , jpg format images and not taking into considering SVC or Gif type of images. 
      try:
        # We are downloading the images and store them in their respective format below . 
       if i!=None:
          if i.find('.png')!=-1 and i.find('http')!=-1:
            #print(i)
            try:
             res=requests.get(i,headers={"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"},verify=False,timeout=3);
            except:
             continue
            if res.status_code:
              fp = open('check.png', 'wb')
              fp.write(res.content)
              fp.close()
            im=cv2.imread(r"E:\iso_v2\check.png")
          elif i.find('.jpg')!=-1 and i.find('http')!=-1:
            #print(i)
            try:
             res=requests.get(i,headers={"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"},verify=False,timeout=3);
            except:
             continue
            if res.status_code:
              fp = open('check.jpg', 'wb')
              fp.write(res.content)
              fp.close()
            im=cv2.imread(r"E:\iso_v2\check.jpg")
          elif i.find('jpeg')!=-1 and i.find('http')!=-1:
            #print(i)
            try:
             res=requests.get(i,headers={"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"},verify=False,timeout=3);
            except:
             continue
            if res.status_code:
              fp = open('check.jpeg', 'wb')
              fp.write(res.content)
              fp.close()
            im=cv2.imread(r"E:\iso_v2\check.jpeg")
          else:
            continue
          #resizing the image to fit to the model .
          im=cv2.resize(im,(256,256))
          #cv2.imshow('',im)
          #cv.waitkey(0)
          #Predicting the outcome..
          yhat=Model.predict(np.expand_dims(im/255,0))
          print(yhat)
          #if the predicted value is greater than 0.75 than return 1 and break loop .
          if np.argmax(yhat)==0:
            if yhat[0][0]>=0.75:
              print("ISO certified")
              return 1
              break
      except:
        continue 
  return 0
            
