if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from dbupload import upload_file, DropboxConnection
from getpass import getpass
import unittest
import mechanize

email = ""
password = ""

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        fh = open("small_test_file.txt","w")
        fh.write("Small test file")
        fh.close()
        
    def test1_login(self):
        conn = DropboxConnection(email, password)
        
        self.assertTrue(conn.is_logged_in())
    
    def test2_bad_login(self):
        try:
            conn = DropboxConnection("bad email", "bad password")
        except:
            self.assertRaises(Exception)
    
    def test3_upload_small(self):
        conn = DropboxConnection(email, password)
        conn.upload_file("small_test_file.txt","/","small_test_file.txt")
        
    def test4_dir_list(self):
        conn = DropboxConnection(email, password)
        conn.get_dir_list("/")
    
    def test5_download(self):
        conn = DropboxConnection(email, password)
        conn.download_file("/","small_test_file.txt","small_test_file.txt")
        
    def test6_get_public_url(self):
        conn = DropboxConnection(email, password)
        conn.get_public_url("/","small_test_file.txt")

    def test7_delete_file(self):
        conn = DropboxConnection(email, password)
        conn.delete_file("/","small_test_file.txt")
        
if __name__ == '__main__':
    if email == '':
        email = raw_input('Dropbox account email:')

    if password == '':
        password = getpass('Dropbox password:')

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)