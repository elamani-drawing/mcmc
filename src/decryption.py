from hmac import new
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
        __accept_degradation:
            La limite de accepter en cas de degradation de la plausibilite, utile pour l'algorithme de metropolice
            1>= __accept_degradation >= 0
        __result : dict or None 
            Le resultat de data decrypter apres self.run()
        __plausible : 
            La plausibilité de la traduction par apport au enchainement des lettres
        __max_iteration: int
            Le maximum d'iteration que le programme peut faire
        """
        McmcFile.__init__(self)
        self.__sampling = None
        self.__accept_degradation = 0
        self.__result = None 
        # self.__plausible = None
        self.__max_iteration = 100000
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

    def set_acceptable_degration(self, degradation :float =0)-> bool : 
        """
            Parametre la limite acceptable en cas de degradation de la plausibilite, utile pour l'algorithme de metropolice
            Parameters
            ----------
            degradation: int = 2
                La valeur de degradation
        """
        print("deg", degradation)
        if(degradation>1 or degradation<0):
            message = f"Degradation must be between 1 and 0."
            raise DecryptionException(message)
        self.__accept_degradation = degradation
        return True

    def set_max_iteration(self, iteration :int)-> bool : 
        """
            Parametre la limiteacceptable en cas de degradation de la plausibilite, utile pour l'algorithme de metropolice
            Parameters
            ----------
            iteration: int
                La valeur de degradation
        """
        print("deg", iteration)
        if(iteration<=9999):
            message = f"iteration must be bigger than 9999."
            raise DecryptionException(message)
        self.__max_iteration = iteration
        return True

    def get_sampling(self) -> Sampling or None:
        """
            Retourne self._sampling.
        """
        return self.__sampling

    def get_max_iteration(self) -> int :
        """
            Retourne self.__max_iteration.
        """
        return self.__max_iteration

    def get_accept_degradation(self) -> float or None:
        """
            Retourne self.__accept_degradation.
        """
        return self.__accept_degradation

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
        affichage+= f"sampling: {self.get_sampling()},\n"
        if(result):
            affichage+= f"result: {self.get_resultat()},\n"
        affichage+= f"max_iteration: {self.get_max_iteration()},\n"
        affichage+= f"limite de degradation acceptable: {self.get_accept_degradation()},\n"

        if result : 
            affichage+= f"result : {self.__result},\n"
        
        print(affichage)

    def __init_proposition(self, sampling:Sampling, sampling_crypted : Sampling) : #-> tuple(dict, list)
        """
            Renvoie la premiere proposition
        """
        sampling_list =  [key for key, value in sampling.get_result()["occurence_letter"].items()]
        sampling_crypted_list =  [key for key, value in sampling_crypted.get_result()["occurence_letter"].items()]
        proposition = {}
        for i in range(len(sampling_crypted_list)):
            if ((sampling_list[i] != "total") and (sampling_crypted_list[i] != "total")):
                if(i <len(sampling_crypted_list)):
                    proposition[sampling_crypted_list[i]] = sampling_list[i]
                else:
                    proposition[sampling_crypted_list[i]] = "" #si il y a des lettres presentes dans sampling_crypted_list mais pas dans  sampling_list
        
        return proposition, sampling_list

    def __get_next_proposition(self, proposition : dict, liste: list)-> dict:
        """
            Retourne une proposition
            Parameters
            ----------
            proposition: 
                Un dictionnaire expliquant les correspondances des lettres, ex: {a : e, b : c, d: f ...}
            liste: list
                Une liste des clés presente dans dictionnaire
        """
        letter = random.choice(liste)
        letter_2 = random.choice(liste)
        while(letter_2 == letter):
            letter_2 =random.choice(liste)
        letter_value = proposition.pop(letter)
        letter_2_value = proposition.pop(letter_2)
        proposition[letter] = letter_2_value
        proposition[letter_2] = letter_value
        print("--",letter, letter_2_value, letter_2, letter_value)
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

    def __re_write(self, phrase :str, proposition : dict, letters : list) -> str:
        """
            Réecris phrase avec la correspondance des lettres présente dans dict
            Parameters
            ----------
            phrase: str 
                La phrase qu'il faut réecrire 
            proposition: dict
                Un dictionnaire expliquant les correspondances des lettres, ex: {a : e, b : c, d: f ...}
            letters: list
                une liste de lettre, si un charractere n'est pas present dans la liste de letters ses occurences ne seront pas réecrite 
        """
        new_phrase=""
        for letter in phrase:
            if(letter in letters):
                new_phrase += proposition[letter]
            else:
                new_phrase+=letter
        return new_phrase

    def __search(self,sampling_crypted: Sampling):
        """
            S'occupe de réaliser toutes les operations sur phrase jusqu'a avoir un taux de plausibilite acceptable
            Parameters
            ----------
            sampling_crypted: Sampling
                L'object sampling du texte crypter
        """
        proposition, list_letter = self.__init_proposition(self.get_sampling(), sampling_crypted)
        list_letter.remove("total")
        traduction = sampling_crypted.get_data()
        plausibilite_acceptable = 1.7
        plausibilite = self.__plausibiliter(traduction)
        result = {
            "init" : {
                "proposition" : proposition,
                "traduction"  : traduction,
                "plausibilite": plausibilite
            },
            "others" : {
                "nbr_iterration" : 0
            }
        }
        result["last"] = result["init"].copy()
        result["max_plausible"] = result["init"].copy()
        
        while((plausibilite <plausibilite_acceptable) and (result["others"]["nbr_iterration"] < self.get_max_iteration())):
            #créer une nouvelle proposition, réecris le texte avec et calcul sa plausibiliter
            proposition = self.__get_next_proposition(proposition=proposition.copy(), liste=list_letter)
            traduction = self.__re_write(traduction, proposition, list_letter)
            plausibilite = self.__plausibiliter(traduction)
            #la plausibilite est acceptable 
            if((plausibilite+ self.get_accept_degradation()) >=result["last"]["plausibilite"]):
                print("----------------------------garde", plausibilite + self.get_accept_degradation(), result["last"]["plausibilite"] )
                #on met à jour la derniere proposition 
                result["last"]["proposition"] = proposition
                result["last"]["traduction"] = traduction 
                result["last"]["plausibilite"] = plausibilite 

                #on verifie si la plausibilite est plus grande que la meilleur qu'on est eu 
                if(plausibilite> result["max_plausible"]["plausibilite"]):  
                    result["max_plausible"]["proposition"] = proposition
                    result["max_plausible"]["traduction"] = traduction 
                    result["max_plausible"]["plausibilite"] = plausibilite 
            #la plausibilite est inutilisable > 1.6
            else:
                print("---garde pas", plausibilite, "--", result["last"]["plausibilite"], traduction)
                #on revient on arriere et on essaye une autre proposition 
                proposition = result["last"]["proposition"]
                traduction = result["last"]["traduction"]
                plausibilite = result["last"]["plausibilite"]

            result["others"]["nbr_iterration"] += 1
        
        return result 

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
        # sampling_data_crypted.display(True)
        # print(sampling_data_crypted.get_data())
        sampling_data_crypted.sorted()
        print(self.__search(sampling_data_crypted))
        
        #verifier le chargement des datas, les majuscules doivent etre des minuscule, garder les espaces etc.

        # print(self.__plausibiliter(phrase="aujourd'hui je suis allez me promener aux bord de la riviere, j'y est croiser mon frere qui y pechait des poissons-chat."))
        # print(self.__plausibiliter(phrase="sfdjk refd rfdzfsd qeqqsqdfsedz jlmfdv dfuhijodsf sdbuh i dsq vsqy caca qbdhds bds deshjk dsujkd zdesijref rsodsh gybhdsub dvsbhsdb dsbchisd dshbcxxx"))
        
        # print(self.__plausibiliter(phrase="marine"))
        # print(self.__plausibiliter(phrase="zemour"))
        # print(self.__plausibiliter(phrase="Le héros de la chanson de geste tient ses traits du héros épique. Il est vaillant, brave, il sait manier les armes, il allie la franchise à la loyauté et à la générosité. Par-dessus tout, il sait préserver son honneur. Parmi les nombreux motifs hérités de la chanson de geste, notons celui de la description des armes du chevalier, de ses acolytes ou de ses ennemis, celui des combats et des batailles qui s'ensuivent ou bien encore ceux des embuscades, poursuites et autres pièges qui jalonnent le chemin du héros. On trouve également les scènes d'ambassade chères à la chanson de geste, les scènes de conseil entre un seigneur et ses barons ou encore le regret funèbre (lamentations sur un héros, un compagnon perdu) et la prière du plus grand péril. Cependant, le roman s'éloigne sur plusieurs points de la chanson de geste"))
        # print(self.__plausibiliter(phrase="La rupture littéraire amorcée par l'apparition du nouveau genre de la poésie lyrique ne doit pas pour autant masquer une large continuité dans les thèmes et les motifs évoqués par le roman. Il hérite en premier lieu des personnages stylisés de la poésie lyrique : la dame y est une femme mariée de condition supérieure à celle de son prétendant ; l'homme vassal est obéissant à la dame, il est timide et emprunté devant elle et le losengiers est un personnage fourbe, un traître en puissance. Il reprend également le thème de la fine amor, cet amour secret, sacré dans lequel la femme est divinisée, sacralisée. Il hérite aussi de la Reverdie. La Reverdie est un retour cyclique au printemps qui entraîne la contemplation de la dame par l'amant ainsi que son portrait élogieux fait d'association entre la beauté de la nature et celle de la femme. La sonorité est également une partie intégrante de la poésie lyrique, car la poésie ne peut se faire sans rimes et le lyrisme ne peut se séparer des sonorités, du rythme."))
        
        # print(self.__plausibiliter(phrase="Lg pg lqwg rcu eqpvtg wpg gswkrg gp rctvkewnkgt. Lg lqwg rqwt og dcvvtg eqpvtg n'kfgg fg rgtftg. Lg pg lqwg rcu eqpvtg wpg gswkrg gp rctvkewnkgt. Lg lqwg rqwt og dcvvtg eqpvtg n'kfgg fg rgtftg."))

        # x >= 1.8 parfait
        # x >= 1.6 && x < 1 discutable
        # x > 1 beaucoup trop null

        #verifier la proposition initiale