# PythonDropboxUploader (dbupload)

A very small Python package which provides a function to easily maniupulate files stored on Dropbox. This does not use the official API and should probably not be used on any kind of production system.

# Usage

## Basic uploading

```python
from dbupload import DropboxConnection

conn = DropboxConnection("email@example.com", "password")
conn.upload_file("local_file.txt","/remote/path/","remote_file.txt")
```

## Directory Listing

```python
from dbupload import DropboxConnection

conn = DropboxConnection("email@example.com", "password")
print(conn.get_dir_list('/remote/path'))
```

## Downloading a file

```python
from dbupload import DropboxConnection

conn = DropboxConnection("email@example.com", "password")
conn.download_file("/remote/path","remote_file.txt","local_file.txt")
```

## Download all files in a directory

```python
from dbupload import DropboxConnection

conn = DropboxConnection("email@example.com", "password")

urls = conn.get_dir_list('/remote/path')

for filename in urls:
    conn.download_file_from_url(urls[filename], filename)
```