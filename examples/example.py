from dbupload import DropboxConnection
from getpass import getpass

email = raw_input("Enter Dropbox email address:")
password = getpass("Enter Dropbox password:")

# Create a little test file
fh = open("small_test_file.txt","w")
fh.write("Small test file")
fh.close()

try:
    # Create the connection
    conn = DropboxConnection(email, password)
    
    # Upload the file
    conn.upload_file("small_test_file.txt","/","small_test_file.txt")
except:
    print("Upload failed")
else:
    print("Uploaded small_test_file.txt to the root of your Dropbox")