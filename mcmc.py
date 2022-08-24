from multiprocessing.dummy import active_children
from ssl import ALERT_DESCRIPTION_HANDSHAKE_FAILURE
from errors import McmcException
import os, json, random

class MCMC:
    """
    """
    def __init__(self):
        """
        Parameters
        ----------
        __path : str or None
            le chemin vers le fichier txt
        __data : str or None
            le contenu du fichier pointer par path ou une chaine de charractere python
        __result : dict or None 
            Le resultat de donnée génerer par self.run()
        __alphabet : list or None
            L'alphabet de a à Z, il est vide sauf durant l'execution de self.run()
        __total__letters: int 
            Le nombre de lettre qu'il y a dans data
        """
        self.__path = None
        self.__data = None
        self.__result = None
        self.__alphabet = None
        self.__total__letters = 0 

    def set_path(self, path)->bool:
        """
        Renseigne le chemin du fichier qui doit etre utiliser durant le run 
        ATTENTION: Apres un run, self.__path est remis à None
        Parameters
        ----------
        path : str
            le chemin vers le fichier txt
        Raises
        ---------
        McmcException
        """
        if (os.path.exists(path)): 
            self.__path = path
            return True
        message = f"The resource: \"{path}\", was not found"
        raise McmcException(message)
    
    def set_data(self, data)->bool:
        """
        Parameters
        ----------
        data : str
            Une chaine de charractere
        Raises
        ---------
        McmcException
        """
        if(type(data) == str):
            if(len(data.replace(" ",''))> 0):
                self.__data = data
                return True
            else :
                message = f"The resource: \"{data}\", must not be empty"
        else :
            message = f"The resource: \"{data}\", must be a string"
        raise McmcException(message)
    
    def __load_file(self)-> bool:
        """
            Recupere le contenue du fichier de la variable path.
        """
        if(self.__path != None):
            with open(f"{self.__path}", 'r') as f:
                self.__data = f.read()
                #apres utilisation le path est vider
                self.__path = None
                return True 
        else:
            message = f"The resource: 'self.__data' et 'self.__path' are None, must be set self.__data or self.path"
            raise McmcException(message)
            
    def __take_stats(self):
        """
            Parcours le contenu de data et compte combien de fois une lettre a la position i-1 est suivis de la lettre à la position i 
        """
        dictionaire = self.__result
        alphabet = self.__alphabet
        data = str(self.__data)
        for i in range(len(data)):
            if(i >0 and (data[i] in alphabet) ):
                if(str(letter_before) in dictionaire):
                    if(str(data[i]) in dictionaire[str(letter_before)]):
                        dictionaire[str(letter_before)][str(data[i])] += 1
                        self.__total__letters += 1
            letter_before = data[i]
        alphabet = None
    
    def __create_file(self,name, content): 
        """
        """
        with open(f"{name}", 'w') as f:
            f.write(str(content))

    def to_percentage(self, export:bool = False, name:str = "mcmc_pourcent.txt")-> dict or None:
        """
            Convertit self.__result en pourcentage 
            ----------
            export: bool = False
                indique si les données doivent etre retourner ou exporter sous forme de fichier txt
            name: str = mcmc_pourcent.txt
                le nom du fichier qui sera exporter
        """
        # (valeur * 100 )/ total
        total = self.__total__letters
        dictionnaire_percentage = self.__result
        dictionnaire = {} 
        #créé un dictionnaire de pourcentage
        for cle in dictionnaire_percentage:
            dictionnaire[cle] = {}
            for cle_2 in dictionnaire_percentage[cle]:
                dictionnaire[cle][cle_2] = (int(dictionnaire_percentage[cle][cle_2]) * 100) / total

        #on a convertit les valeurs en pourcentage
        if(export):
            self.__create_file(name, dictionnaire)
            return None
        return dictionnaire

    def to_json(self, data: dict =None, export:bool = False, name:str = "mcmc.json") -> dict or None:
        """
            Convertit self.__result en json 
            ----------
            data : dict or None = None
                est un dictionnaire de donner comme self.__result comme self.to_percentage(...)
            export: bool = False
                indique si les données doivent etre retourner ou exporter sous forme de fichier json
            name: str = mcmc.json
                le nom du fichier qui sera exporter
        """
        if(data==None):
            data = self.__result
        json_data = json.dumps(data, indent = 4) 
        if(export):
            self.__create_file(name, json_data)
            return None
        return json_data

    def to_txt(self, name:str = "mcmc_txt.txt") -> None:
        """
            Exporte self.__result en fichier.txt 
            ----------
            name: str = mcmc_txt.txt
                le nom du fichier qui sera exporter
        """
        self.__create_file(name, self.__result)
        return None

    def display(self, result: bool = False):
        """
            Affiche le contenu de l'object MCMC
            Parameters
            ----------
            result : bool = False
                indique si self.__result doit etre afficher ou non
        """
        affichage = f"path : {self.__path},\n"
        if(self.__data and len(self.__data) > 10):
            affichage += f"data : '{self.__data[:3]}...{self.__data[len(self.__data)-3:]}',\n"
        else:
            affichage +=  f"data : '{self.__data}',\n"
        affichage +=  f"total letters : '{self.__total__letters}',\n"
        if result : 
            affichage+= f"result : {self.__result},\n"
        

        print(affichage)
    
    def run(self) -> bool:
        """
            Lance la simulation
        """
        if(self.__data == None):
            self.__load_file()
            
        self.__result  = {}
        self.__alphabet = []
        #generation des dictionnaires de lettres
        for num_lettre in range(ord('a'), ord('z')+1):
            #remplissage du tableau de lettre qui est utile pour eviter les carracteres speciaux
            self.__alphabet.append(chr(num_lettre))
            content2 = {}
            for num_lettre2 in range(ord('a'), ord('z')+1):
                content2[chr(num_lettre2)] = 0
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

        if value in largest_values]

    def make_word(self, iteration:int=5, length:int= 5, data : dict = None):
        if(data==None):
            data = self.__result

        liste_word_generate = []
        size_word = length
        while(iteration>0):
            word = ""
            random_char = chr(random.randint(97, 122)) # 97 = a, 122 = z
            word+=random_char

            while(size_word>0):
                five_letter_reccurent = self.__largest(data[random_char])
                random_char = random.choice(five_letter_reccurent)
                word += random_char
                size_word-=1
                
            size_word = length
            # if word[len(word)-1:] == 's' and not 'x' in word and not 'a' in word:
            #     liste_word_generate.append(word)
            #     iteration-=1
            liste_word_generate.append(word)
            iteration-=1
            
        return liste_word_generate
