from file import McmcFile
from errors import DecryptionException
from sampling import Sampling
import os, json, random

class Decryption:
    """
        La
    """
    def __init__(self):
        """
        Parameters
        ----------
        __sampling : Sampling or None 
            Un object Sampling
        __accept_plausible_degradation:
            La limite de accepter en cas de degradation de la plausibilite, utile pour l'algorithme de metropolice
        __result : str 
            Le resultat de data decypter apres self.translate()
        __plausible : 
            La plausibilité de la traduction par apport au enchainement des lettres
        __iteration: int
            Indique combien d'itération ont falu pour décrypter les donner
        """
        McmcFile.__init__(self)
        self.__sampling = None
        self.__accept_plausible_degradation = None
        self.__result = None 
        self._plausible = None

        def set_sampling(sampling : Sampling) -> bool: 
            """
                Parametre self.__sampling
                Parameters
                ----------
                sampling : Sampling: 
                    Un object Sampling 
            """
            if(sampling.has_run()==False):
                sampling.run()
            self.__sampling = sampling
            return True

        def set_plausible_degration(degradation :int =2)-> bool : 
            """
                Parametre la limiteacceptable en cas de degradation de la plausibilite, utile pour l'algorithme de metropolice
                Parameters
                ----------
                degradation: int = 2
                    La valeur de degradation
            """
            self.__accept_plausible_degradation = degradation

        
