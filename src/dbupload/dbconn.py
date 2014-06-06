import mechanize
import urllib2
import re
import json

class DropboxConnection:
    """ Creates a connection to Dropbox """
    
    email = ""
    password = ""
    root_ns = ""
    token = ""
    uid = ""
    request_id = ""
    browser = None
    
    def __init__(self,email,password):
        self.email = email
        self.password = password
        
        self.login()

    def login(self):
        """ Login to Dropbox and return mechanize browser instance """
        
        # Fire up a browser using mechanize
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        
        # Browse to the login page
        login_src = self.browser.open('https://www.dropbox.com/login').read()
        
        # Enter the username and password into the login form
        isLoginForm = lambda l: l.action == "https://www.dropbox.com/ajax_captcha_login" and l.method == "POST"
        
        try:
            self.browser.select_form(predicate=isLoginForm)
        except:
            self.browser = None
            raise(Exception('Unable to find login form'))
        
        self.get_constants(login_src)
        
        self.browser.form.new_control('text', 't', {'value':''})
        self.browser.form.fixup()
        
        self.browser['login_email'] = self.email
        self.browser['login_password'] = self.password
        self.browser['t'] = self.token
        
        # Send the form
        response = self.browser.submit()
        
    def get_constants(self, src):
        """ Load constants from page """
        
        try:
            self.root_ns = re.findall(r"\"root_ns\": (\d+)", src)[0]
            self.token = re.findall(r"\"TOKEN\": ['\"](.+?)['\"]", src)[0].decode('string_escape')
            
        except:
            raise(Exception("Unable to find constants for AJAX requests"))

    def refresh_constants(self):
        """ Update constants from page """
        
        src = self.browser.open('https://www.dropbox.com/home').read()
        
        try:
            self.root_ns = re.findall(r"\"root_ns\": (\d+)", src)[0]
            self.token = re.findall(r"\"TOKEN\": ['\"](.+?)['\"]", src)[0].decode('string_escape')
            self.uid = re.findall(r"\"id\": (\d+)", src)[0]
            self.request_id = re.findall(r"\"REQUEST_ID\": ['\"]([a-z0-9]+)['\"]", src)[0]
            
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
        
    def get_dir_list(self,remote_dir):
        """ Get file info for a directory """
        
        self.refresh_constants()
        
        if(not self.is_logged_in()):
            raise(Exception("Can't download when not logged in"))
            
        req_vars = "ns_id="+self.root_ns+"&referrer=&t="+self.token+"&is_xhr=true"+"&parent_request_id="+self.request_id
        
        req = urllib2.Request('https://www.dropbox.com/browse'+remote_dir+'?_subject_uid='+self.uid,data=req_vars)
        req.add_header('Referer', 'https://www.dropbox.com/home'+remote_dir)
        
        dir_info = json.loads(self.browser.open(req).read())
        
        dir_list = {}
        
        for item in dir_info['file_info']:
            if(item['is_dir'] == False):
                # get local filename
                absolute_filename = item['ns_path']
                local_filename = re.findall(r".*\/(.*)", absolute_filename)[0]
                
                # get file URL and add it to the dictionary
                file_url = item['href']
                dir_list[local_filename] = file_url
                
        return dir_list
                
    def get_download_url(self, remote_dir, remote_file):
        """ Get the URL to download a file """
        
        return self.get_dir_list(remote_dir)[remote_file]
        
    def download_file_from_url(self, url, local_file):
        """ Store file locally from download URL """
        
        fh = open(local_file, "wb")
        fh.write(self.browser.open(url).read())
        fh.close()
        
    def download_file(self, remote_dir, remote_file, local_file):
        """ Download a file and save it locally """
        
        self.download_file_from_url(self.get_download_url(remote_dir,remote_file), local_file)
    
    def is_logged_in(self):
        """ Checks if a login has been established """
        if(self.browser):
            return True
        else:
            return False
