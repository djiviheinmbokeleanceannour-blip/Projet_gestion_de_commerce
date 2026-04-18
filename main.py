from  globalite_marchandise import Vente,Mes_dettes,Achat,Globalite
from traduction_json import ecriture_dans_json,lecture_json,traduction_en_json
from datetime import datetime
import uuid
import os
'''except KeyError as e:
    print(f"Erreur de structure dans le fichier JSON : la clé {e} est manquante.")
except TypeError:
    print("Erreur de type : impossible de traiter les données.")
except Exception as e:
    print(f"Une erreur inattendue est survenue : {e}")'''
def affichage_choix():
    print("-------Menu action à executer------")
    print("1: AJOUTER")
    print("2: MODIFIER")
    print("3: SUPPRIMER")
    print("4: RECHERCHER")
    print("5: VOIR TABLEAU DE BENEFICE")
    while True:
         choix_a_faire=gestion_d_echec("votre choix: ")
         try:
               if choix_a_faire==1 or choix_a_faire==2 or choix_a_faire==3 or choix_a_faire==4 or choix_a_faire==5:
                   while True:
                       try:
                         if choix_a_faire==1:
                            nombre_de_fois_de_choix_d_ajout()
                            return 0
                         elif choix_a_faire==2:
                              choix,x,y,z=modifications()
                              marchandise_modifier=Globalite()
                              w=marchandise_modifier.modification(choix,x,y,z)
                              ecriture_dans_json(w)
                              return 0
                         elif choix_a_faire==3:
                            choix,id=supression()
                            marchandise_supprimer=Globalite()
                            w=marchandise_supprimer.supprimer(choix,id)
                            ecriture_dans_json(w)
                            return 0
                         elif choix_a_faire==4:
                              choice,iD=affichage()
                              marchandise_rechercher=Globalite()
                              marchandise,w=marchandise_rechercher.rechercher(choice,iD)
                              print(marchandise)
                              ecriture_dans_json(w)
                              return 0
                         elif choix_a_faire==5:
                              marchandise_benefice=Globalite()
                              nom=input("Veuillez entrez le nom de la marchandise: ")
                              benefice=marchandise_benefice.calcul_de_benefice(nom.lower())
                              w=lecture_json("fichier.json")
                              w["les benefices"].append(benefice)
                              ecriture_dans_json(w)
                              return 0
                       except Exception as e:
                            print(f"erreur reelle {e}")
         except:
              print("Veuillez verifier votre choix")
def supression():
     choix=choix_specifique()
     w=lecture_json("fichier.json")
     if choix==1:
        liste_achat=w["les achats"]
        id=suppression_preleminaire(liste_achat)
        return choix,id
     elif choix==2:
        liste_vente=w["les ventes"]
        id=suppression_preleminaire(liste_vente)
        return choix,id
        
     elif choix==3:
        liste_dettes=w["les dettes"]
        id=suppression_preleminaire(liste_dettes)
        return choix,id
        
def suppression_preleminaire(liste):
     if not liste:
                  print("Aucune donnée dans cette section")
                  return None,None,None,None
     while True:
            id=input("l'ID de la marchandise à supprimer: ")
            try:
                for marchandise in liste:
                        if str(marchandise["identifiant"])==str(id):
                          return id
            except:
                print("Veuillez verifier l'ID svp")
def modifications():
            choix=choix_specifique()
            w=lecture_json("fichier.json")
            if choix==1:
              liste_vente=w["les achats"]
              x,y,z=modifications_preleminaire(liste_vente)
              return choix,x,y,z
            elif choix==2:
              liste_vente=w["les ventes"]
              x,y,z=modifications_preleminaire(liste_vente)
              return choix,x,y,z
            elif choix==3:
              liste_vente=w["les dettes"]
              x,y,z=modifications_preleminaire(liste_vente)
              return choix,x,y,z
def modifications_preleminaire(liste_vente):
    if not liste_vente:
        print("Aucune donnée dans cette section")
        return None,None,None,None
    while True:
         x=input("l'ID de la marchandise à modifier: ")
         try:
              for marchandise in liste_vente:
                     if str(marchandise["identifiant"])==str(x):
                           while True:
                                y=input("Veuillez entrez l'information à modifier: ")
                                try:
                                     if y.lower()=="nom":
                                            z=input("Veuillez entrez la valeur de l'information: ")
                                     elif  y.lower()=="prix unitaire" or y.lower()=="nombre":
                                           z=gestion_d_echec("la valeur de l'information")
                                     return x,y,z
                                except:
                                      print("Veuillez verifier ce que vous avez saisie svp")
                                      break
         except:
                          print("Veuillez verifier l'identifiant")
def choix_specifique():
    print("Faites un choix en fonction des nombres svp")
    print("1: ACHAT")
    print("2: VENTE")
    print("3: PRETTEUR")
    while True:
          choix=gestion_d_echec("votre choix")
          try:
               if choix==1 or choix==2 or choix==3 :
                  return choix
          except:
               print("Choix incorrect")
def ajouter():    
     while True:
        w=lecture_json("fichier.json")
        liste_achat = w.get("les achats", [])
        x=choix_specifique() 
        date1,nom=nom_marchandise_et_date()
        a,caracteristique,prix,prix_unit=prix_calcul()
        n= str(uuid.uuid4())
        try:
            if x==1:
                   v=Achat(date1,nom,a,caracteristique,prix,n)
                   v.prix_unitaire=prix_unit
                   return v
            elif x == 2: 
              trouve = False
              for marchandise in liste_achat:
                  if marchandise["nom"].lower() == nom.lower():
                      trouve = True
                      break
              if trouve:
                  v = Vente(date1, nom, a, caracteristique, prix, n)
                  v.prix_unitaire = prix_unit
                  print("Données enregistrées avec succès")
                  return v
              else:
                print(f"Erreur : Vous n'avez jamais acheté de '{nom}'. Veuillez tout d'abord ajouter dans le tableau achat")
                return "Exit"
            elif x==3:
                   nom_pretteur,date_de_paye=demande_nom_pretteur()
                   v=Mes_dettes(nom_pretteur,date1,nom,a,caracteristique,prix,n,date_de_paye)
                   v.prix_unitaire=prix_unit
                   return v
        except SystemExit:
            raise
        except:
                   print("Veuillez verifier votre choix")
def prix_calcul():
           prix_unitaire=None                     
           a=gestion_d_echec("le nombre:")
           caracteristique=input("Veuillez entrez la caractérisque du marchandise (par ex sac de riz ou koro de riz)")
           print("choix 1: Entrez le prix unitaire")
           print("choix 2: Entrez le prix total")
           while True:
                  choix=gestion_d_echec("votre choix: ")
                  try:
                     if choix==1:
                       prix_unitaire=gestion_d_echec("prix unitaire: ")
                       prix=prix_unitaire*a
                       return a,caracteristique,prix,prix_unitaire
                     else:
                       prix=gestion_d_echec("prix total: ")
                       return a,caracteristique,prix,prix_unitaire
                  except ValueError:
                       print("Veuillez verifier votre choix")
def gestion_d_echec(a):
      while True:
         x=input(f"Veuillez entrez {a} ")
         try:
            nombre=int(x)
            if nombre>0:
              return nombre
            else:
                print("Un nombre positif svp")
            exit
         except:
            print("svp, verifier")  
def nom_marchandise_et_date():                
        nom=input("Nom de la marchandise: ")
        r=datetime.now()
        date=r.strftime("%d/%m/%Y")
        return date,nom
def demande_nom_pretteur():
        nom=input("Nom du pretteur: ")
        date_de_paye=input("Veuillez entrez la date de remboursement: ")
        return nom,date_de_paye
def nombre_de_fois_de_choix_d_ajout(): 
    '''elle permet de creer une liste au travers du nombre_de_champs saisi par l'utilisateur, donc tout ce qui sera saisi sera stocké dans cette liste et apres trié pour sctocké chacun de son coté'''                
    nombre_de_champs=gestion_d_echec("le nombre de marchandises à ajouter: ")
    for i in range(nombre_de_champs):
        x=ajouter()
        classe=Globalite() 
        if isinstance(x,Achat)==True:
           classe.achat.append(x)
        elif isinstance(x,Vente)==True:
           classe.vente.append(x)
        elif isinstance(x,Mes_dettes)==True:
           classe.dette.append(x)
        elif x=="Exit":
             os._exit(0)
        w=classe.traduction_dict()
        traduction_en_json(w,"fichier.json")
def affichage():
     choix=choix_specifique()
     id=input("veuillez entrez l'uuid de la marchandise à rechercher: ")
     return choix,id
affichage_choix()