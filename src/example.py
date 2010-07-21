from dbupload import upload_file
from getpass import getpass

email = raw_input("Enter Dropbox email address:")
password = getpass("Enter Dropbox password:")

upload_file("example.py","/","dbupload_test.txt",email,password)