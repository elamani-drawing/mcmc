### Sampling 

## Description 
Sampling prend une chaine de caractère en entrée (ou un fichier.txt) et recueille des renseignements dessu. 
Le résultat sera un dictionnaire python ayant comme clé : 
1. 'occurrence_letter': l'occurrence de x dans les données en entrée, avec `x compris dans [a, z]`. 
2. 'data':  de fois x et suivi de y, avec `x compris dans [a, z]` et `y compris dans [a, z]`.

Après avoir recueilli les informations nécessaires, Sampling d'exporter les données dans un fichier txt/json et/ou de générer des mots ayant la même allure (forme et/ou prononciation) que les données en entrées. (Ex : si la chaine de caractère en entrée est allemande, les mots ressembleront à des mots allemand).

### Exemples 
## Créer un object Sampling
```python
sampling = Sampling()
```
## Lui passer les données en entrée
```py
#Vous pouvez lui passer une chaine de carractere si vous voulez juste reccueillir des renseignements sur la chaine de carractere
#Mais si vous prevoyez de generer des mots, ils faudraient lui passer le plus de mots possible, par exemple tout les mots d'un dictionnaires ou un long texte (comme les paroles d'une musique, un livre etc.)
sampling.set_path("./words/francais_30000.txt") #ici nous lui donnons le lien vers un fichier texte contenant 30000 mots
#sampling.set_data("une chaine carractere") #vous pouvez par exemple passer une variable ayant du texte reccuperer depuis une api ou un fichier que vous auriez déja charger
```
## Afficher votre sampling
```py
#affichage des attributs de Sampling 
sampling.display() #vous permet d'afficher son contenu, que ca soit le path, data, resultat etc. ca peut etre pratique pour débugger
sampling.display(True) #indique que vous voulez également afficher le resultat, pouvant etre assez consequent nous avons décider de le mettre en option
```
## Lancer le processus pour recueillir les données
ATTENTION apres sampling.run() le programme verifie si un chemin est renseigner (à l'aide de set_path), si c'est le cas, le programme charge le contenu du fichier dans self.__data, et l'attribut self.__path est remis à None.
```py
sampling.run()  
```
Apres le run, vous pouvez soit generer des mots soit exporter les données.
## Generer des mots
```py
print(sampling.make_word()) #les mots générés sont renvoyés dans une liste
```
## Exporter les données
```py
#en json
sampling.to_json() #convertit les données en json et les renvoies 
sampling.to_json(export=True, name="sampling.json") #convertit les données en json et les exportes dans un fichier json

#en txt
#(Si vous vous demandez pourquoi c'est sous la forme d'un json) Au fur et à mesure du développement la complexité du dictionnaire contenant les résultat à évoluer, nous ne savions plus sous quel forme les representés pour les exportées dans un format txt ou csv donc nous avons repris le meme format que pour le json -.-', il n'y a plus trop d'interet à utiliser la methode to_txt mais elle existe toujours!
sampling.to_txt() #convertit les données en json et les renvoies
sampling.to_txt(export=True, name="sampling.txt") #convertit les données en json et les exportes dans un fichier txt
```
## Convertir les valeurs données en pourcentage
```py
print(sampling.to_percentage()) #Copie le dictionnaire de résultat en convertsissant les valeurs en pourcentage et retourne le nouveau dictionnaire
sampling.to_percentage(export=True, name="sampling_percentage.txt") #Copie le dictionnaire de résultat en convertsissant les valeurs en pourcentage et les exportes dans un fichier .txt
sampling.to_json(data = sampling.to_percentage()) #les valeur en pourcentage et retourne les données sous la forme de json
sampling.to_json(data = sampling.to_percentage(),export=True, name="sampling_percentage_tojson.json") #les valeur en pourcentage et exporte les données sous la forme de json
```

## Ranger les données du plus grand au plus petit
```py
sampling.sorted() #Range les valeurs de 'occurence_letter' dans l'ordre décroissant par apport au valeur
```

### Methodes
Je vous laisse le soin d'utiliser votre éditeur pour avoir plus de détails sur la signature, les arguments de chacunes des methodes etc.