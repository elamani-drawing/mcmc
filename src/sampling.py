from file import McmcFile
from errors import SamplingException
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
            
    def __take_stats(self):
        """
            Parcours le contenu de data et compte combien de fois une lettre a la position i-1 est suivis de la lettre à la position i 
        """
        dictionaire = self.__result
        alphabet = self.__alphabet
        data = str(self._data)
        for i in range(len(data)):
            if(i >0 and (data[i] in alphabet) ):
                if(str(letter_before) in dictionaire):
                    if(str(data[i]) in dictionaire[str(letter_before)]):
                        dictionaire[str(letter_before)][str(data[i])] += 1
                        dictionaire[str(letter_before)]["total"] += 1
            letter_before = data[i]
        alphabet = None
    

    def to_percentage(self, export:bool = False, name:str = "mcmc_pourcent.txt")-> dict or None:
        """
            Convertit self.__result en pourcentage 
            ----------
            export: bool = False
                indique si les données doivent etre retourner ou exporter sous forme de fichier txt
            name: str = mcmc_pourcent.txt
                le nom du fichier qui sera exporter
        """
        #formule = (valeur * 100 )/ total
        
        dictionnaire_percentage = self.__result
        dictionnaire = {} 
        #créé un dictionnaire de pourcentage
        for cle in dictionnaire_percentage:
            dictionnaire[cle] = {}
            total = dictionnaire_percentage[cle]["total"]
            for cle_2 in dictionnaire_percentage[cle]:
                if(cle_2 != "total") :
                    dictionnaire[cle][cle_2] = (dictionnaire_percentage[cle][cle_2] * 100) / total
            dictionnaire[cle]["total"] = dictionnaire_percentage[cle]["total"]
        #on a convertit les valeurs en pourcentage
        if(export):
            self._create_file(name, dictionnaire)
            return None
        return dictionnaire

    def to_json(self, data: dict =None, export:bool = False, name:str = "sampling.json") -> dict or None:
        """
            Convertit self.__result en json 
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
        affichage = f"path : {self._path},\n"
        if(self._data and len(self._data) > 10):
            affichage += f"data : '{self._data[:3]}...{self._data[len(self._data)-3:]}',\n"
        else:
            affichage +=  f"data : '{self._data}',\n"
        affichage +=  f"total letters : '{self.__total__letters}',\n"
        if result : 
            affichage+= f"result : {self.__result},\n"
        

        print(affichage)
    
    def run(self) -> bool:
        """
            Lance la simulation
        """
        self.__has_run= True

        if(self._data == None):
            self._load_file()
            
        self.__result  = {}
        self.__alphabet = []
        #generation des dictionnaires de lettres
        for num_lettre in range(ord('a'), ord('z')+1):
            #remplissage du tableau de lettre qui est utile pour eviter les carracteres speciaux
            self.__alphabet.append(chr(num_lettre))
            content2 = {}
            for num_lettre2 in range(ord('a'), ord('z')+1):
                content2[chr(num_lettre2)] = 0
            
            content2["total"] = 0
            self.__result[chr(num_lettre)] = content2
        self.__take_stats()
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

        return [key for key, value in data.items() 

        if value in largest_values and value !=0 and key != "total"]

    def make_word(self, iteration:int=5, length:int= 5, data : dict = None) -> list:
        """
            Génére des mots ayant une prononciation dans la meme longue que les données dans self.__data/self.__path
            
            Parameters
            ----------
            iteration : int = 5
                Le nombre de mot qui doivent être génerer, si (iteration < 1) SamplingException
            length : int = 5
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
            data = self.__result

        liste_word_generate = []
        
        while(iteration>0):
            if(length>0):
                size_word = length
            else:
                size_word = random.randint(3,7)
            word = ""
            random_char = chr(random.randint(97, 122)) # 97 = a, 122 = z
            word+=random_char

            while(size_word>0):
                five_letter_reccurent = self.__largest(data[random_char])
                random_char = random.choice(five_letter_reccurent)
                word += random_char
                size_word-=1

            liste_word_generate.append(word)
            iteration-=1
            
        return liste_word_generate

if __name__ == '__main__':
    print("pas encore disponnible")