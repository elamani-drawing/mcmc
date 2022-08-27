import  sys, os, shutil
sys.path.append(".")
from src.MCMC_AU import Sampling
from src.MCMC_AU import McmcException
#si vous avez installer MCMC_AU vous pouvez utiliser ses imports
# from MCMC_AU import Sampling
# from MCMC_AU import McmcException
import unittest

class SamplingTest(unittest.TestCase):
    def test_run_with_data(self):
        sampling = make_sampling()
        sampling.set_data(data=get_content())
        
        self.assertIsInstance(sampling, Sampling.Sampling)
        self.assertTrue(sampling.has_run()==False)

        sampling.run()
        self.assertEqual(sampling.get_path(), None) 
        data = sampling.get_result()["data"]
        #verification des valeurs apres un premier run
        self.assertEqual(data["a"]["i"], 3) 
        self.assertEqual(sampling.get_result()["occurence_letter"]["total"], 160) 
        self.assertTrue(sampling.has_run())

        sampling.run()
        self.assertEqual(sampling.get_path(), None) 
        data = sampling.get_result()["data"]
        #verification des valeurs apres un deuxieme run
        self.assertEqual(data["a"]["i"], 3) 
        self.assertEqual(sampling.get_result()["occurence_letter"]["total"], 160) 
        self.assertTrue(sampling.has_run())

        self.assertRaises(McmcException.McmcFileException, sampling.set_path, "./test/not exist.txt") 

        sampling = None

    def test_run_with_path(self):
        sampling = make_sampling()
        self.assertIsInstance(sampling, Sampling.Sampling)
        self.assertTrue(sampling.has_run()==False)
        
        #erreur du run parcequ'il n'y a pas de data, pas de path
        self.assertEqual(sampling.get_path(), None) 
        self.assertEqual(sampling.get_data(), None) 
        self.assertRaises(McmcException.McmcFileException, sampling.run ) 

        sampling.set_path("test/words/francais_30000.txt")
        self.assertTrue(sampling.has_run() == False)
        sampling.run()
        data = sampling.get_result()["data"]

        #verification des valeurs apres un premier run
        self.assertEqual(data["a"]["i"], 1604) 
        self.assertEqual(data["b"]["a"], 507) 
        self.assertEqual(sampling.get_result()["occurence_letter"]["total"], 158910) 
        self.assertTrue(sampling.has_run())

        sampling = None

    def test_to_percentage(self):
        sampling = make_sampling()
        sampling.set_path("test/words/francais_30000.txt")
        sampling.run()
        data_percentage = sampling.to_percentage()
        #verification data
        for letter in data_percentage["data"]:
            for letter_two in data_percentage["data"][letter]:
                if(letter_two !="total"):
                    if((0>data_percentage["data"][letter][letter_two]) or (data_percentage["data"][letter][letter_two]>100)):
                        print(data_percentage["data"][letter], data_percentage["data"][letter][letter_two])
                        self.assertTrue(False)
        #verification occurence_letter
        for letter in data_percentage["occurence_letter"]:
            if(letter_two !="total"):
                if((0>data_percentage["occurence_letter"][letter]) or (data_percentage["occurence_letter"][letter]>100)):
                    print(data_percentage["occurence_letter"][letter])
                    self.assertTrue(False)

    def test_make_words(self):
        sampling = make_sampling()
        sampling.set_path("test/words/francais_30000.txt")
        self.assertRaises(McmcException.SamplingException, sampling.make_word) 
        sampling.run()
        words = sampling.make_word()
        self.assertEqual(len(words), 5)
        default_value = 8
        words = sampling.make_word(iteration = default_value, length=default_value)
        self.assertEqual(len(words), default_value)
        for word in words:
            self.assertEqual(len(word), default_value)

    def test_generate_file(self):
        
        # return #le test est desactiver 
        sampling = make_sampling()
        sampling.set_path("test/words/swann.txt")
        sampling.run()
        output_directory_path ="test/output/"
        #clear output directory
        try:
            shutil.rmtree(output_directory_path)
        except:
            pass
        #make directory
        os.makedirs(output_directory_path)
        #make file
        samping_files = ["sampling_tojson.json","sampling_percentage_tojson.json","sampling_to_txt.txt","sampling_export_to_percentage.txt"]
        data_percentage = sampling.to_percentage()
        sampling.to_json(export=True, name=output_directory_path+samping_files[0])
        sampling.to_json(data=data_percentage,export=True, name=output_directory_path+samping_files[1])
        sampling.to_txt(output_directory_path+samping_files[2])
        sampling.to_percentage(export=True,name=output_directory_path+samping_files[3])

        #verification file
        output_directory = os.listdir(output_directory_path)
        for file in samping_files:
            self.assertIn(file, output_directory)


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
    sampling = Sampling.Sampling()
    return sampling


if __name__ == '__main__':
    unittest.main()