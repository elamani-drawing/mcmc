from unittest import result
from .McmcFile import McmcFile
from .McmcException import SamplingException 
import json, random

class Sampling(McmcFile):
    """
        La Classe Sampling réalise un échantillonage sur self._data, elle compte pour chaque lettre entre [a, z] combien de fois elle est suivie par chaque lettre dans [a, z] d'apres le contenu de self._data.
        Apres cela elle permet d'exporter les résultats en fichier.txt ou fichier.json() en valeur brute ou convertit en pourcentage, et peut etre utiliser dans la classe Decryption()
        La classe Sampling hérite de McmcFile.
    """
    def __init__(self):
        """
        Parameters
        ----------
        __result : dict or None 
            Le resultat de donnée génerer par self.run()
        __alphabet : list or None
            L'alphabet de a à Z, il est vide sauf durant l'execution de self.run()
        __has_run: bool
            Indique si self.run() à déjà été executer au moins une fois sur self
        """
        McmcFile.__init__(self)
        self.__result = None
        self.__alphabet = None
        self.__has_run = False

    def has_run(self) -> bool:
        """
            Indique si self.run() à déjà étè executer au moin une fois
        """
        return self.__has_run

    def get_result(self) -> dict or None:
        """
            Renvoie le contenu de self.__result
        """
        return self.__result 
        
    def __take_stats(self):
        """
            Parcours le contenu de data et compte combien de fois une lettre a la position i-1 est suivis de la lettre à la position i 
        """
        dictionaire = self.__result["data"]
        dictionaire_occurence = self.__result["occurence_letter"]

        alphabet = self.__alphabet
        data = str(self._data)
        for i in range(len(data)):
            if(i >0 and (data[i] in alphabet) ):
                if(str(letter_before) in dictionaire):
                    if(str(data[i]) in dictionaire[str(letter_before)]):
                        dictionaire[str(letter_before)][str(data[i])] += 1
                        dictionaire[str(letter_before)]["total"] += 1

                        dictionaire_occurence[str(letter_before)] +=1
                        dictionaire_occurence["total"] +=1

            letter_before = data[i]
        alphabet = None
    

    def to_percentage(self, export:bool = False, name:str = "mcmc_pourcent.txt")-> dict or None:
        """
            Convertit self.__result en pourcentage 
            Parameters
            ----------
            export: bool = False
                indique si les données doivent etre retourner ou exporter sous forme de fichier txt
            name: str = mcmc_pourcent.txt
                le nom du fichier qui sera exporter
        """
        #formule = (valeur * 100 )/ total
        
        dictionnaire_percentage = self.__result["data"]
        dictionnaire_occurence_percentage = self.__result["occurence_letter"]
        dictionnaire = {} 
        dictionnaire_occurence = {} 
        #créé un dictionnaire de pourcentage
        for cle in dictionnaire_percentage:
            dictionnaire[cle] = {}
            total = dictionnaire_percentage[cle]["total"]
            if(total <1):
                total = 1
            for cle_2 in dictionnaire_percentage[cle]:
                if(cle_2 != "total") :
                    dictionnaire[cle][cle_2] = (dictionnaire_percentage[cle][cle_2] * 100) / total
            dictionnaire[cle]["total"] = dictionnaire_percentage[cle]["total"]

        for cle in dictionnaire_occurence_percentage:
            if(cle != "total"):
                total = dictionnaire_occurence_percentage["total"]
                if(total <1):
                    total = 1
                dictionnaire_occurence[cle] = (dictionnaire_occurence_percentage[cle] * 100)/total
            else:
                dictionnaire_occurence[cle] = dictionnaire_occurence_percentage["total"]

        resultat = {}
        resultat["data"] = dictionnaire
        resultat["occurence_letter"] = dictionnaire_occurence
        #on a convertit les valeurs en pourcentage
        if(export):
            self._create_file(name, resultat)
            return None
        return resultat

    def to_json(self, data: dict =None, export:bool = False, name:str = "sampling.json") -> dict or None:
        """
            Convertit self.__result en json 
            Parameters
            ----------
            data : dict or None = None
                est un dictionnaire de donner comme self.__result comme self.to_percentage(...)
            export: bool = False
                indique si les données doivent etre retourner ou exporter sous forme de fichier json
            name: str = sampling.json
                le nom du fichier qui sera exporter
        """
        if(data==None):
            data = self.__result
        json_data = json.dumps(data, indent = 4) 
        if(export):
            self._create_file(name, json_data)
            return None
        return json_data

    def to_txt(self, name:str = "mcmc_txt.txt") -> None:
        """
            Exporte self.__result en fichier.txt 
            Parameters
            ----------
            name: str = mcmc_txt.txt
                le nom du fichier qui sera exporter
        """
        self._create_file(name, self.__result)
        return None

    def display(self, result: bool = False):
        """
            Affiche le contenu de l'object Sampling
            Parameters
            ----------
            result : bool = False
                indique si self.__result doit etre afficher ou non
        """
        affichage = self.toStringMcmcFile()
        affichage+= f"has_run: {self.__has_run},\n"
        if result : 
            affichage+= f"result: {self.__result},\n"
        
        print(affichage)
    
    def run(self) -> bool:
        """
            Lance la simulation
        """

        if(self._data == None):
            self._load_file()
            
        self.__has_run= True
        dictionnaire_letter_count = {} #enregistre pour chaque lettre les occurences des autres lettre
        dictionnaire_letter_occurence = {} #enregistre loccurence de chaque lettre 
        self.__alphabet = []
        #generation des dictionnaires de lettres
        for num_lettre in range(ord('a'), ord('z')+1):
            #remplissage du tableau de lettre qui est utile pour eviter les carracteres speciaux
            self.__alphabet.append(chr(num_lettre))
            content2 = {}
            for num_lettre2 in range(ord('a'), ord('z')+1):
                content2[chr(num_lettre2)] = 0
                dictionnaire_letter_occurence[chr(num_lettre2)] = 0
            
            content2["total"] = 0
            dictionnaire_letter_occurence["total"] = 0
            dictionnaire_letter_count[chr(num_lettre)] = content2
        
        self.__result = {}
        self.__result["data"] = dictionnaire_letter_count
        self.__result["occurence_letter"] = dictionnaire_letter_occurence
        self.__take_stats()
        return True


    def __sorted_alphabet_by_value(self,dictionnaire:dict) -> dict:
        """
            Range dictionnaire["occurence_letter"] par apport au valeur
            Parameters
            ----------
            dictionnaire : dict 
                Attend une valeur de type self.__result non None
        """
        dictionnaire_sorte = {}
        while len(dictionnaire) >0:
            plus_grand_key = -1
            plus_grand_value = -1
            for element in dictionnaire:
                if (dictionnaire[element] > plus_grand_value):
                    plus_grand_key = element
                    plus_grand_value = dictionnaire[element]

            dictionnaire_sorte[plus_grand_key] = dictionnaire.pop(plus_grand_key)

        dictionnaire = dictionnaire_sorte
        return dictionnaire

    def sorted(self) -> bool:
        """
            Range le contenu de self.__result["occurence_letter"] dans l'ordre décroissante des valeurs
        """
        if self.__result == None:
            raise SamplingException("Result seems corrupted")
        self.__result["occurence_letter"] = self.__sorted_alphabet_by_value(self.get_result()["occurence_letter"])
        return True

    def __largest(self, data : dict): 
        """
            Choisis 3 lettres parmis les lettres ayant le plus grand valeurs dans le dict
            Parameters
            ----------
            result : bool = False
                indique si self.__result doit etre afficher ou non
           
        """
        largest_values = sorted(data.values(), reverse=True)[:3] 

        return [key for key, value in data.items() if value in largest_values and value !=0 and key != "total"]

    def make_word(self, iteration:int=5, data : dict = None, length : int =-1) -> list:
        """
            Génére des mots ayant une prononciation dans la meme longue que les données dans self.__data/self.__path
            
            Parameters
            ----------
            iteration : int = 5
                Le nombre de mot qui doivent être génerer, si (iteration < 1) SamplingException
            length : int = -1
                La taille des mots génerer, si (length <=0) les mots generer auront une taille aleatoire entre 3 et 7 
            data: dict = None
                Si vous souhaitez utiliser d'autre donnée pour génerer les mots, sinon le programme utilisera self.
            Raises
            --------- 
            SamplingException
        """
        if(self.__has_run==False):
            raise SamplingException("Before can use self.make_word(), must use self.run()")

        if(iteration<1):
            raise SamplingException("self.make_word: iteration must be largest than 1")

        if(data==None):
            dictionnary = self.__result["data"]
        else:
            if("data" in data):
                dictionnary = data["data"]         
            else:
                raise SamplingException("data seems corrupted")

        liste_word_generate = []
        
        while(iteration>0):
            if(length>0):
                size_word = length
            else:
                size_word = random.randint(3,7)
            word = ""
            random_char = chr(random.randint(97, 122)) # 97 = a, 122 = z
            word+=random_char

            while(size_word>1):
                five_letter_reccurent = self.__largest(dictionnary[random_char])
                random_char = random.choice(five_letter_reccurent)
                word += random_char
                size_word-=1

            liste_word_generate.append(word)
            iteration-=1
            
        return liste_word_generate
