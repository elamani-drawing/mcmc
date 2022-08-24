from .McmcException import McmcFileException 
import os

class McmcFile:
    """
        La classe McmcFile permet de charger correctement le contenu d'un fichier txt ou d'une chaine de carractere qui pourra etre utiliser.
        Elle est surtout faire pour être hériter et non directement être utiliser. 
    """
    def __init__(self):
        """
        Parameters
        ----------
        _path : str or None
            Le chemin vers le fichier txt
            Le path est vidé apres avoir utiliser son contenu soit charger dans data
        _data : str or None
            Le contenu du fichier pointer par path ou une chaine de charractere python
        """
        self._path = None
        self._data = None

    def get_path(self) -> str or None:
        """
            Retourne le chemin du fichier utiliser ou None s'il n'a pas ete parametrer ou s'il a deja ete utiliser
        """
        return self._path 

    def get_data(self) -> str or None: 
        """
            Retourne le texte que l'utilisateur à donner ou le texte contenu dans self.__path ou None si le texte n'a pas encore ete charger
        """
        return self._data

    def set_path(self, path)->bool:
        """
        Renseigne le chemin du fichier qui doit etre utiliser durant le run 
        ATTENTION: Apres un run, self._path est remis à None
        Parameters
        ----------
        path : str
            le chemin vers le fichier txt
        Raises
        ---------
        McmcFile
        """
        if (os.path.exists(path)): 
            self._path = path
            return True
        message = f"The resource \"{path}\", was not found"
        raise McmcFileException(message)
    
    def set_data(self, data)->bool:
        """
        Parameters
        ----------
        data : str
            Une chaine de charractere
        Raises
        ---------
        McmcFile
        """
        if(type(data) == str):
            if(len(data.replace(" ",''))> 0):
                self._data = data
                return True
            else :
                message = f"The resource: \"{data}\", must not be empty"
        else :
            message = f"The resource: \"{data}\", must be a string"
        raise McmcFileException(message)
    
    def _load_file(self)-> bool:
        """
            Recupere le contenue du fichier de la variable path.
        """
        if(self._path != None):
            with open(f"{self._path}", 'r') as f:
                self._data = f.read()
                #apres utilisation le path est vider
                self._path = None
                return True 
        else:
            message = f"The resource: 'self._data' et 'self._path' are None, must be use self.set_data() or self.set_path()"
            raise McmcFileException(message)

    
    def _create_file(self,name, content): 
        """
            Creer un fichier
            Parameters
            ----------
            name : str
                Le nom qui doit etre crée, exemple : "mcmc.txt"
            content: str or dict
                Le contenu du fichier creer
        """
        with open(f"{name}", 'w') as f:
            f.write(str(content))
    
    
    def toStringMcmcFile(self):
        """
            Affiche le contenu de l'object McmcFile
        """
        affichage = f"path : {self._path},\n"
        if(self._data and len(self._data) > 10):
            affichage += f"data : '{self._data[:3]}...{self._data[len(self._data)-3:]}',\n"
        else:
            affichage +=  f"data : '{self._data}',\n"

        return affichage