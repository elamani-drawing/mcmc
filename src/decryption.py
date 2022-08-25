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
            sampling.sorted()
        else: 
            message = f"The resource: 'sampling' must be run with sampling.run()"
            raise DecryptionException(message)
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

    def __init_proposition(self, sampling:Sampling, sampling_crypted : Sampling) -> dict :
        sampling_list =  [key for key, value in sampling.get_result()["occurence_letter"].items()]
        sampling_crypted_list =  [key for key, value in sampling_crypted.get_result()["occurence_letter"].items()]
        proposition = {}
        for i in range(len(sampling_list)):
            if ((sampling_list[i] != "total") and (sampling_crypted_list[i] != "total")):
                proposition[sampling_list[i]] = sampling_crypted_list[i]
        return proposition

    def __plausibiliter(self, phrase:str) -> float:
        """
            Calcul le niveau de plausibiliter d'une phrase
            Parameters
            ----------
            phrase : str
                La phrase dont il faut calculer le niveau de plausibiliter
        """
        #formule = (1/N) * Produit(log(Pi)) avec N=  le nombre de charractere par mot et Pi= la probabilité
        data = self.__sampling.to_percentage()["data"]
        produit_final = []
        alphabet = [key for key, value in self.__sampling.get_result()["occurence_letter"].items()]
        for mot in phrase.split(" "):
            # print("--------------------------", mot)
            produit_current = []
            for i in range(len(mot)):
                if (i>0):
                    current_letter = mot[i] 
                    if (before_letter in alphabet and current_letter in alphabet):
                        # print("value", data[before_letter][current_letter])
                        # print("produit", produit_current * math.log(data[before_letter][current_letter]*1000) )
                        produit_current.append(data[before_letter][current_letter])
                before_letter = mot[i]
                
            # print(produit_current)
            produit_current = sum(produit_current)
            produit_current = produit_current * (1/len(mot))
            # print(produit_current)
            produit_final.append(produit_current)
        
        alphabet = None
        # return sum(produit_final)
        return sum(produit_final) * (1/len(phrase))


    def run(self):
        """
            Lance le processus de déchiffrement
        """
        """
            {
                "initiale ": {
                    proposition  : {a : e , b : c ..}
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
        resultat = {
            "initiale" : {},
            "before" : {},
            "current" : {}
        }
        if(self.__sampling == None):
            message = f"The resource: 'self.__sampling' must be renseigned"
            raise DecryptionException(message)
            
        sampling_data_crypted = Sampling()
        if(self.get_data() == None):
            if(self.get_path()==None):
                message = f"The resource: 'self._data' et 'self._path' are None, must be use self.set_data() or self.set_path()"
                raise DecryptionException(message)
            sampling_data_crypted.set_path(self.get_path())
        else:
            sampling_data_crypted.set_data(self.get_data())
        sampling_data_crypted.run()
        sampling_data_crypted.sorted()
        
        # print(sampling_data_crypted.get_result()["occurence_letter"])
        # print(self.__sampling.get_result()["occurence_letter"])
        # print(self.__init_proposition(self.__sampling, sampling_crypted=sampling_data_crypted))
        print(self.__plausibiliter(phrase="aujourd'hui je suis allez me promener aux bord de la riviere, j'y est croiser mon frere qui y pechait des poissons-chat."))
        print(self.__plausibiliter(phrase="sfdjk refd rfdzfsd qeqqsqdfsedz jlmfdv dfuhijodsf sdbuh i dsq vsqy caca qbdhds bds deshjk dsujkd zdesijref rsodsh gybhdsub dvsbhsdb dsbchisd dshbcxxx"))
        
        print(self.__plausibiliter(phrase="marine"))
        print(self.__plausibiliter(phrase="zemour"))
        
        