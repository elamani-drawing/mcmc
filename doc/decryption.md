# Decryption 
## Table des matiéres
1. [Description](#description)
2. [Exemples](#exemples)
3. [Méthodes](#methodes)

## Description 
Decryption devrait à l'origine permettre de décrypter des chaines cryptées. Mais cette fonctionnalité ne fonctionne pas encore.  

Elle permet également de calculer le niveau de plausibilité d'une phrase.  

`Plausibilité d'une phrase`: A quel point les mots d'une phrase semble cohérente par apport a l'object Sampling donnée en entrée. (Permet de savoir si les mots ont un sens ou si c'est des suites de lettres qui n'ont pas de sens)  

Une phrase est : 
1. parfaitement coherente lorsqu'elle à un score au dessu de 1.8
2. cohérente lorsqu'elle à un score entre 1.8 et 1.7 
3. discutable lorsqu'elle à un score entre 1.7 et 1.6
4. du charabia l'orsqu'elle est en dessous de 1.6 (Plus on s'approche de 0 et plus c'est n'importe quoi)

## Exemples 
### Créer un object Decryption
```python
decryption = Decryption()
```
Vous aurez besoin d'un obect [Sampling](sampling.md)
### Lui passer les données en entrée
```py
#le sampling 
#Le sampling lui sert de réference pour savoir quel enchainement de lettre est correcte ou non
decryption.set_sampling(sampling=sampling)

#le texte crypter
#si vous souhaitez decrypter une phrase crypter 
decryption.set_path("words/crypter.txt") #ici nous lui donnons le lien vers un fichier texte contenant une phrase crypter
#decryption.set_data("La phrase crypter qu'il doit décrypter") #vous pouvez par exemple passer une variable ayant du texte crypter reccuperer depuis une api ou un fichier que vous auriez déja charger
```
### Afficher votre sampling
```py
#affichage les attributs de decryption 
decryption.display() #vous permet d'afficher son contenu, que ca soit le path, data, resultat etc. ca peut etre pratique pour débugger
decryption.display(True) #indique que vous voulez également afficher le resultat, pouvant etre assez consequent nous avons décider de le mettre en option
```
### Lancer le processus pour décrypter le texte
ATTENTION apres decryption.run() le programme verifie si un chemin est renseigner (à l'aide de set_path), si c'est le cas, le programme charge le contenu du fichier dans self.__data, et l'attribut self.__path est remis à None.
```py
#ne fonctionne pas encore
decryption.run()
resultat = decryption.get_result()  
```
### Calculer le niveau de plausibiliter d'une chaine de carractere
Cette fonctionnalité est disponnible peux importe que self.run, self.set_data, self.set_path aient été lancer ou non du moment que self.set_sampling aient été réaliser.
```py
decryption.set_sampling(sampling=sampling)
decryption.take_plausibilite("Une chaine de carractere") 
```

## Methodes
Je vous laisse le soin d'utiliser votre éditeur pour avoir plus de détails sur la signature, les arguments de chacunes des methodes de Decryption etc.