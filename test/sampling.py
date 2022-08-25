import  sys
sys.path.append(".")
from src.Sampling import Sampling
from src.McmcException import McmcFileException
import unittest

class SamplingTest(unittest.TestCase):
    def test_run_with_data(self):
        sampling = make_sampling()
        sampling.set_data(data=get_content())
        
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

    def test_run_with_path(self):
        sampling = make_sampling()
        self.assertIsInstance(sampling, Sampling)
        self.assertTrue(sampling.has_run()==False)
        
        #erreur du run parcequ'il n'y a pas de data, pas de path
        self.assertEqual(sampling.get_path(), None) 
        self.assertEqual(sampling.get_data(), None) 
        self.assertRaises(McmcFileException, sampling.run ) 

        sampling.set_path("test/words/francais_30000.txt")
        self.assertTrue(sampling.has_run() == False)
        sampling.run()
        data = sampling.get_result()["data"]

        #verification des valeurs apres un premier run
        self.assertEqual(data["a"]["i"], 1601) 
        self.assertEqual(data["b"]["a"], 472) 
        self.assertEqual(sampling.get_result()["occurence_letter"]["total"], 157410) 
        self.assertTrue(sampling.has_run())

        sampling = None


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
    return sampling


if __name__ == '__main__':
    unittest.main()