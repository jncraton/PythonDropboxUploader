from dbupload import upload_file
from getpass import getpass

email = raw_input("Enter Dropbox email address:")
password = getpass("Enter Dropbox password:")

# create test file
fh = open("small_test_file.txt","w")
fh.write("Small test file")
fh.close()
    
try:
    upload_file("small_test_file.txt","/","small_test_file.txt",email,password)
except:
    print("Upload failed")
else:
    print("Uploaded small_test_file.txt to the root of your Dropbox")