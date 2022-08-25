import unittest
import sys 
sys.path.append(".")
from src.Decryption import Decryption

class DecryptionTest(unittest.TestCase):
    def test_run(self):
        """
        """
    
def make_decryption():
    decryption = Decryption()
    # decryption.set_data(data=get_content())
    return decryption

if __name__ == '__main__':
    unittest.main()