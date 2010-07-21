#!/usr/bin/python

import mechanize
import os
from datetime import date

email = 'email'
password = 'pass'

def isLoginForm(form):
    if(form.action == "https://www.dropbox.com/login"):
        return True
    else:
        return False
        
def isUploadForm(form):
    if(form.action == "https://dl-web.dropbox.com/upload"):
        return True
    else:
        return False

def uploadFile(local_file,remote_dir,remote_file,email,password):
    print("Connecting to Dropbox server...")
    
    br = mechanize.Browser()
    br.open('https://www.dropbox.com/login')
    br.select_form(predicate=isLoginForm)
    
    print("Found login form...")
    print("Sending username and password...")
    
    br["login_email"] = email
    br["login_password"] = password
    
    response = br.submit()
    
    print("Looking for upload form...")
    
    br.select_form(predicate=isUploadForm)
    
    print("Uploading the file...")
    
    br.form.find_control("dest").readonly = False
    br.form.set_value(remote_dir,"dest")
    br.form.add_file(open(local_file),"",remote_file)
    
    print(br.form)
    
    br.submit()
    
    print("File uploaded successfully!")
