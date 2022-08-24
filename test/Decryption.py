import unittest
import sys 
sys.path.append(".")
from src.Decryption import Decryption

class SamplingTest(unittest.TestCase):
    def test_run(self):
        """
        """
    
def get_content():
    return """Aaron
        abaisse
        abaissement
        abaisser
        abandon
        abandonnant
        abandonne
        abandonne
        abandonnee
        abandonnees
        abandonnent
        abandonner
        abandonnes
        abasie
        abasourdi
        abasourdir
        abasourdissement
        abat-jour
        abats
        abattage"""
        
def make_decryption():
    decryption = Decryption()
    # decryption.set_data(data=get_content())
    return decryption

if __name__ == '__main__':
    unittest.main()