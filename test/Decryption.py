import unittest
import sys
sys.path.append(".")

from src.Sampling import Sampling
from src.McmcException import DecryptionException 
from src.Decryption import Decryption

class DecryptionTest(unittest.TestCase):
    def test_run(self):
        decryption = make_decryption()
        sampling = Sampling()
        sampling.set_path("test/words/swann.txt")
        #test erreur path/data and sampling renseigned
        self.assertRaises(DecryptionException, decryption.run) #error because sampling not renseigned
        # self.assertRaises(DecryptionException, decryption.set_sampling, sampling) #error because sampling not runed // now this error is catch from sampling class
        decryption.set_sampling(sampling=sampling) 
        self.assertRaises(DecryptionException, decryption.run) #error because data/path not renseigned
        decryption.set_path("test/words/chiffrer.txt")
        # decryption.set_data("a word")
        # decryption.run()

    def test_accept_plausible_degradation(self):
        decryption = make_decryption()
        self.assertRaises(DecryptionException, decryption.set_acceptable_degration, 1.1)
        self.assertRaises(DecryptionException, decryption.set_acceptable_degration, 2)
        self.assertRaises(DecryptionException, decryption.set_acceptable_degration, -0.0000001)
        decryption.set_acceptable_degration()
        decryption.set_acceptable_degration(0.00005)
        decryption.set_acceptable_degration(1.00000000)
        
    def test_take_plausibilite_plausibilite(self):
        decryption = make_decryption()
        sampling = Sampling()
        sampling.set_path("test/words/francais_30000.txt")
        decryption.set_sampling(sampling=sampling) 
        #un prenom
        self.assertEqual(decryption.take_plausibilite("marine"), 1.891323871106025)
        #aucune difference par apport au majuscule et minuscule
        self.assertEqual(decryption.take_plausibilite("mArIne"), decryption.take_plausibilite("marine"))
        #un veritable texte en francais
        self.assertEqual(decryption.take_plausibilite("Le héros de la chanson de geste tient ses traits du héros épique. Il est vaillant, brave, il sait manier les armes, il allie la franchise à la loyauté et à la générosité. Par-dessus tout, il sait préserver son honneur. Parmi les nombreux motifs hérités de la chanson de geste, notons celui de la description des armes du chevalier, de ses acolytes ou de ses ennemis, celui des combats et des batailles qui s'ensuivent ou bien encore ceux des embuscades, poursuites et autres pièges qui jalonnent le chemin du héros. On trouve également les scènes d'ambassade chères à la chanson de geste, les scènes de conseil entre un seigneur et ses barons ou encore le regret funèbre (lamentations sur un héros, un compagnon perdu) et la prière du plus grand péril. Cependant, le roman s'éloigne sur plusieurs points de la chanson de geste"), 1.959384845357306)
        #un phrase en francais qui a été crypter en cesar avec un décalage de 2
        self.assertEqual(decryption.take_plausibilite("Lg pg lqwg rcu eqpvtg wpg gswkrg gp rctvkewnkgt. Lg lqwg rqwt og dcvvtg eqpvtg n'kfgg fg rgtftg. Lg pg lqwg rcu eqpvtg wpg gswkrg gp rctvkewnkgt. Lg lqwg rqwt og dcvvtg eqpvtg n'kfgg fg rgtftg."), 0.09680116661844874)
        #une phrase en francais
        self.assertEqual(decryption.take_plausibilite("Le héros de la chanson de geste tient ses traits du héros épique"), 2.718990346033509)
        #une phrase avec des lettres mis au hasard
        self.assertEqual(decryption.take_plausibilite("zdsf rzsduhidsw hdsiu gdsiSFGygdsi dsgiuopSefdKSfe eds"), 0.25009819643702536)

        
        
def make_decryption():
    decryption = Decryption()
    # decryption.set_data(data=get_content())
    return decryption

if __name__ == '__main__':
    unittest.main()