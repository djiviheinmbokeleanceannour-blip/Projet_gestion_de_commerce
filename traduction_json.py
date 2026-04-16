import json
import os

def traduction_en_json(nouveau_dict,fichier):  
     donnees_existant={ "les achats":[], "les ventes":[], "les dettes":[] }
     if os.path.exists(fichier) and os.path.getsize(fichier)>0:
        with open(fichier, "r", encoding="utf-8") as data:
               try:
                 donnees_existant=json.load(data)
               except json.JSONDecodeError:
                   pass
        donnees_existant["les achats"].extend(nouveau_dict.get("les achats", []))
        donnees_existant["les ventes"].extend(nouveau_dict.get("les ventes", []))
        donnees_existant["les dettes"].extend(nouveau_dict.get("les dettes", []))
     ecriture_dans_json(donnees_existant)
def lecture_json(fichier):
      donnees_existant={ "les achats":[], "les ventes":[], "les dettes":[] }
      with open(fichier, "r", encoding="utf-8") as data:
               try:
                 donnees_existant=json.load(data)
               except json.JSONDecodeError:
                   pass
      return donnees_existant
def ecriture_dans_json(donnees_existant):
     with open("fichier.json","w",encoding="utf-8") as f:
             json.dump(donnees_existant,f,indent=4)
     print("Données enregistrer avec succes")