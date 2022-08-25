from .McmcFile import McmcFile
from .McmcException import DecryptionException 
from .Sampling import Sampling 
import os, json, random

class Decryption(McmcFile):
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
        __result : dict or None 
            Le resultat de data decrypter apres self.run()
        __plausible : 
            La plausibilité de la traduction par apport au enchainement des lettres
        __iteration: int
            Indique combien d'itération ont falu pour décrypter les données
        """
        McmcFile.__init__(self)
        self.__sampling = None
        self.__accept_plausible_degradation = None
        self.__result = None 
        self.__plausible = None
        self.__iteration = None

    def set_sampling(self, sampling : Sampling) -> bool: 
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

    def set_plausible_degration(self, degradation :int =2)-> bool : 
        """
            Parametre la limiteacceptable en cas de degradation de la plausibilite, utile pour l'algorithme de metropolice
            Parameters
            ----------
            degradation: int = 2
                La valeur de degradation
        """
        self.__accept_plausible_degradation = degradation

    def get_resultat(self) -> dict or None:
        """
            Retourne le resultat du dechiffrage ou None si la fonction run n'a pas encore etait appellée.
        """
        return self.__result

    def display(self, result: bool = False):
        """
            Affiche le contenu de l'object Sampling
            Parameters
            ----------
            result : bool = False
                indique si self.__result doit etre afficher ou non
        """
        affichage = self.toStringMcmcFile() 
        affichage+= f"sampling: {self.__sampling},\n"
        affichage+= f"result: {self.__result},\n"
        affichage+= f"iteration: {self.__iteration},\n"
        affichage+= f"plausible: {self.__plausible},\n"
        affichage+= f"limite de degradation acceptable: {self.__accept_plausible_degradation},\n"

        if result : 
            affichage+= f"result : {self.__result},\n"
        
        print(affichage)


    def __plausibiliter(self, phrase:str) -> float:
        """
            Calcul le niveau de plausibiliter d'une phrase
            Parameters
            ----------
            phrase : str
                La phrase dont il faut calculer le niveau de plausibiliter
        """
        #formule = (1/N) * Produit(log(Pi)) avec N=  le nombre de charractere par mot et Pi= la probabilité
        
        return -1.5

    def run(self):
        """
            {
                "initiale ": {
                    proposition  : 
                    traduction  :
                    plausibilite:
                }, 
                "before" : {
                    ...
                }, 
                "current" : {
                    ...
                }
            }
        """
        return None

    
