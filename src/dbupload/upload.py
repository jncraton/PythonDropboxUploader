import mechanize
from dbconn import DropboxConnection

def upload_file(local_file,remote_dir,remote_file,email,password):
    """ Upload a local file to Dropbox """
    
    conn = DropboxConnection(email, password)
    conn.upload_file(local_file,remote_dir,remote_file)
