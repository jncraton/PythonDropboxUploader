import mechanize
import urllib2
import re

class DropboxConnection:
    """ Creates a connection to Dropbox """
    
    email = ""
    password = ""
    root_ns = ""
    token = ""
    browser = None
    
    def __init__(self,email,password):
        self.email = email
        self.password = password
        
        self.login()
        self.get_constants()

    def login(self):
        """ Login to Dropbox and return mechanize browser instance """
        
        # Fire up a browser using mechanize
        self.browser = mechanize.Browser()
        
        # Browse to the login page
        self.browser.open('https://www.dropbox.com/login')
        
        # Enter the username and password into the login form
        isLoginForm = lambda l: l.action == "https://www.dropbox.com/login" and l.method == "POST"
        
        try:
            self.browser.select_form(predicate=isLoginForm)
        except:
            self.browser = None
            raise(Exception('Unable to find login form'))
        
        self.browser['login_email'] = self.email
        self.browser['login_password'] = self.password
        
        # Send the form
        response = self.browser.submit()
        
    def get_constants(self):
        """ Load constants from page """
        
        home_src = self.browser.open('https://www.dropbox.com/home').read()
        
        try:
            root_ns = re.findall(r"root_ns: (\d+)", home_src)[0]
            token = re.findall(r"TOKEN: '(.+)'", home_src)[0]
        except:
            raise(Exception("Unable to find constants for AJAX requests"))

    def upload_file(self,local_file,remote_dir,remote_file):
        """ Upload a local file to Dropbox """
        
        if(not self.is_logged_in()):
            raise(Exception("Can't upload when not logged in"))
            
        self.browser.open('https://www.dropbox.com/')
    
        # Add our file upload to the upload form
        isUploadForm = lambda u: u.action == "https://dl-web.dropbox.com/upload" and u.method == "POST"
    
        try:
            self.browser.select_form(predicate=isUploadForm)
        except:
            raise(Exception('Unable to find upload form'))
            
        self.browser.form.find_control("dest").readonly = False
        self.browser.form.set_value(remote_dir,"dest")
        self.browser.form.add_file(open(local_file,"rb"),"",remote_file)
        
        # Submit the form with the file
        self.browser.submit()
        
    def is_logged_in(self):
        """ Checks if a login has been established """
        if(self.browser):
            return True
        else:
            return False