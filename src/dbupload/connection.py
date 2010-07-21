#!/usr/bin/python

import mechanize

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
    """ Upload a local file to Dropbox """
    
    # Fire up a browser using mechanize
    br = mechanize.Browser()
    
    # Browse to the login page
    br.open('https://www.dropbox.com/login')
    
    # Enter the username and password into the login form
    br.select_form(predicate=isLoginForm)
    
    br["login_email"] = email
    br["login_password"] = password
    
    # Send the form 
    response = br.submit()
    
    # Add our file upload to the upload form once logged in
    br.select_form(predicate=isUploadForm)
    br.form.find_control("dest").readonly = False
    br.form.set_value(remote_dir,"dest")
    br.form.add_file(open(local_file),"",remote_file)
    
    # Submit the form with the file
    br.submit()
