import sys

from src.Sampling import Sampling
from src.McmcException import McmcFileException

def get_content():
    return """Aaron
        abaisse
        abaissement
        abaisser
        abandon
        abandonnant
        abandonne
        abandonne
        abandonnee
        abandonnees
        abandonnent
        abandonner
        abandonnes
        abasie
        abasourdi
        abasourdir
        abasourdissement
        abat-jour
        abats
        abattage"""
        
def make_sampling():
    sampling = Sampling()
    return sampling
