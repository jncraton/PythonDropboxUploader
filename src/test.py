from dbupload import upload_file, DropboxConnection
from getpass import getpass
import unittest
import mechanize

# This won't function until these variables are set to valid credentials
email = ""
password = ""

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        fh = open("small_test_file.txt","w")
        fh.write("Small test file")
        fh.close()
        
    def test_login(self):
        conn = DropboxConnection(email, password)
        
        self.assertTrue(conn.is_logged_in())
    
    def test_bad_login(self):
        try:
            conn = DropboxConnection("bad email", "bad password")
        except:
            self.assertRaises(Exception)
    
    def test_upload_small(self):
        conn = DropboxConnection(email, password)
        conn.upload_file("small_test_file.txt","/","small_test_file.txt")
        
    def test_dir_list(self):
        conn = DropboxConnection(email, password)
        conn.get_dir_list("/Archives")
    
    def test_download(self):
        conn = DropboxConnection(email, password)
        conn.download_file("/","small_test_file.txt","small_test_file.txt")
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)