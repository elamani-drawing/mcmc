import unittest
import sys 
sys.path.append(".")
from src.Sampling import Sampling
from src.McmcException import McmcFileException

class SamplingTest(unittest.TestCase):
    def test_run(self):
        sampling = make_sampling()
        self.assertIsInstance(sampling, Sampling)
        self.assertTrue(sampling.has_run()==False)

        sampling.run()
        self.assertEqual(sampling.get_path(), None) 
        data = sampling.get_result()["data"]
        #verification des valeurs apres un premier run
        self.assertEqual(data["a"]["i"], 3) 
        self.assertEqual(sampling.get_result()["occurence_letter"]["total"], 159) 
        self.assertTrue(sampling.has_run())

        sampling.run()
        self.assertEqual(sampling.get_path(), None) 
        data = sampling.get_result()["data"]
        #verification des valeurs apres un deuxieme run
        self.assertEqual(data["a"]["i"], 3) 
        self.assertEqual(sampling.get_result()["occurence_letter"]["total"], 159) 
        self.assertTrue(sampling.has_run())

        self.assertRaises(McmcFileException, sampling.set_path, "./test/not exist.txt") 

        sampling = None
        # sampling.display()
    
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
        
def make_sampling():
    sampling = Sampling()
    sampling.set_data(data=get_content())
    return sampling

if __name__ == '__main__':
    unittest.main()