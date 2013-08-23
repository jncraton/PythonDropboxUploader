# PythonDropboxUploader (dbupload)

A very small Python package which provides a function to easily maniupulate files stored on Dropbox. This does not use the official API and should probably not be used on any kind of production system.

# Usage

## Basic uploading

```python
from dbupload import DropboxConnection

conn = DropboxConnection("email@example.com", "password")
conn.upload_file("local_file.txt","/remote/path/","remote_file.txt")
```