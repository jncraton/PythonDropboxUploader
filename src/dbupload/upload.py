import mechanize

def upload_file(local_file,remote_dir,remote_file,email,password):
    """ Upload a local file to Dropbox """
    
    # Fire up a browser using mechanize
    br = mechanize.Browser()
    
    # Browse to the login page
    br.open('https://www.dropbox.com/login')
    
    # Enter the username and password into the login form
    isLoginForm = lambda l: l.action == "https://www.dropbox.com/login" and l.method == "POST"
    
    try:
        br.select_form(predicate=isLoginForm)
    except:
        print("Unable to find login form.");
        exit(1);
    
    br['login_email'] = email
    br['login_password'] = password
    
    # Send the form
    response = br.submit()
    
    # Add our file upload to the upload form once logged in
    isUploadForm = lambda u: u.action == "https://dl-web.dropbox.com/upload" and u.method == "POST"

    try:
        br.select_form(predicate=isUploadForm)
    except:
        print("Unable to find upload form.");
        print("Make sure that your login information is correct.");
        exit(1);
        
    br.form.find_control("dest").readonly = False
    br.form.set_value(remote_dir,"dest")
    br.form.add_file(open(local_file,"rb"),"",remote_file)
    
    # Submit the form with the file
    br.submit()
