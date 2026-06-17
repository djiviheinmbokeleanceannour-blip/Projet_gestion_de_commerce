import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# 1. On charge les variables d'environnement du fichier .env
load_dotenv()

# 2. On essaie de se connecter en utilisant os.getenv()
try:
    connexion = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    curseur=connexion.cursor(cursor_factory=RealDictCursor)
    print("Connexion reussie")
except Exception as e:
     print(f"Une erreur est survenue:{e}")
     exit()

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
                            ajouter()
                            return 0
                         elif choix_a_faire==2:
                              modifier()
                              return 0
                         elif choix_a_faire==3:
                            supprimer()
                            return 0
                         elif choix_a_faire==4:
                              rechercher()
                              return 0
                         elif choix_a_faire==5:
                              benefice()
                              return 0
                       except Exception as e:
                            print(f"erreur reelle {e}")
         except:
              print("Veuillez verifier votre choix")


# Fonction d'identification automatique
def obtenir_id_achat_depuis_nom():
    """ Permet à l'ordinateur de trouver l'id_achat tout seul à partir du nom choisi """
    try:
        curseur.execute("SELECT id_achat, nom, nombre FROM achats ORDER BY id_achat;")
        stocks = curseur.fetchall()
        
        if not stocks:
            print("Aucun achat en stock dans pgAdmin. Ajoutez d'abord un achat !")
            return None
            
        print("\n--- Sélectionnez le produit concerné ---")
        for index, produit in enumerate(stocks, 1):
            print(f"{index}: {produit['nom']} (Quantité initiale : {produit['nombre']}) [ID pgAdmin: {produit['id_achat']}]")
            
        while True:
            choix = gestion_d_echec("le numéro du produit choisi")
            if 1 <= choix <= len(stocks):
                return stocks[choix - 1]['id_achat']
            print("Numéro invalide, choisissez dans la liste.")
    except Exception as e:
        print(f"Erreur de récupération des stocks : {e}")
        return None
def benefice():
     print("--------Tableau general des benefices-------")
     try:
          curseur.execute("select*from vue_benefices;")
          lignes=curseur.fetchall()
          if not lignes:
               print("Aucune donnée disponible")
               return
          print(f"{'ID':<4} | {'Nom':<15} | {'investi':<10} | {'vendu':<6} | {'C.A cumulé':<12} | {'Benefice ou perte':<15} | {'Statut du lot'}")
          for l in lignes:
               print(f"{l['id_achat']:<4} | {l['nom_marchandise']:<15} | {l['investissement_initial']:<10} | {l['quantite_totale_vendue']:<6} | {l['chiffre_d_affaire_cumule']:<12} | {l['balance_benefice_ou_perte']:<17} | {l['statut_du_lot']}")
     except Exception as e:
        print(f"Erreur d'affichage du tableau : {e}")


def rechercher():
     id_recherche=obtenir_id_achat_depuis_nom()
     try:
          curseur.execute("select*from vue_etat_stocks where id_achat=%s;",(id_recherche,))
          resultat=curseur.fetchone()
          if resultat:
               print("marchandise trouvé")
               print(f"Produit:{resultat['nom_marchandise']}")
               print(f"Quantite achetée au depart: {resultat['quantite_initiale_achetee']}")
               print(f"Quantité totale vendue: {resultat['quantite_totale_vendue']}")
               print(f"Reste en stock: {resultat['quantite_restante']}")
          else:
               print("Aucun produit ne possede cet ID")
     except Exception as e:
          print(f"Erreur de recherche{e}")
def supprimer():
     choix=choix_specifique()
     id_a_supprimer=gestion_d_echec(" ID à supprimer ")
     if choix==1:
          table,col_id="achats","id_achat"
     elif choix==2:
           table,col_id="ventes","id_vente"
     elif choix==3:
          table,col_id="dettes","id_dette"
     try:
       requete=f"delete from {table} where {col_id}=%s;"
       curseur.execute(requete,(id_a_supprimer,))
       connexion.commit()
       print(f"L'element id {id_a_supprimer} a été supprimé de la table {table}")
     except Exception as e:
          connexion.rollback()
          print(f"Erreur lors de la suppression: {e}")
def modifier():
   choix=choix_specifique()
   id_cible=gestion_d_echec("L'id exact de la ligne à modifier")
   if choix==1:
        table,col_id,col_cible="achats","id_achat","nom"
   elif choix==2:
        table,col_id,col_cible="ventes", "id_vente", "prix_vente_u"
   elif choix==3:
        table,col_id,col_cible="dettes","id_dette","nom_pretteur"
   nouvelle_valeur=input(f"Entrez la nouvelle valeur pour le champ cible({col_cible}): ")
   try:
        requete=f"update {table} set {col_cible}= %s where {col_id}=%s;"
        curseur.execute(requete,(nouvelle_valeur,id_cible))
        connexion.commit()
        print(f"Donnée mis à jour avec succes")
   except Exception as e:
        connexion.rollback()
        print(f"impossible de modifier")
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
     x=choix_specifique() 
     while True:
         if x==1:
            date1,nom=nom_marchandise_et_date()
            a,unite,prix,prix_unit=prix_calcul()
            print("Données enregistrées avec succès")
            try:
                 curseur.execute("""insert into achats (nom,date_achat,nombre,unite,prix_achat_u,prix_achat_t) values (%s,%s,%s,%s,%s,%s);""",(nom,date1,a,unite,prix_unit,prix))
                 connexion.commit()
                 print("Achat enregistré avec succes, merci")
                 break
            except Exception as e:
                 connexion.rollback()
                 print(f'Erreur {e}')
         elif x == 2: 
                id_achat_lie=obtenir_id_achat_depuis_nom()
                if id_achat_lie is None:
                     return
                date1,nom=nom_marchandise_et_date()
                a,unite,prix,prix_unit=prix_calcul()
                try:
                     curseur.execute("""insert into ventes(date_vente,nombre,prix_vente_u,prix_vente_t,id_achat) values(%s,%s,%s,%s,%s);""",(date1,a,prix_unit,prix,id_achat_lie))
                     connexion.commit()
                     print("Données enregistrées avec succès")
                     break
                except Exception as e:
                     connexion.rollback()
                     print(f'Vente refusé par le syteme:{e}')
         elif x==3:
              statut="1"
              id_achat_lie=obtenir_id_achat_depuis_nom()
              if id_achat_lie is None:
                   return
              r=datetime.now()
              date1=r.strftime("%Y/%m/%d")
              prix_unit=None                     
              a=gestion_d_echec("le nombre:")
              print("choix 1: Entrez le prix unitaire")
              print("choix 2: Entrez le prix total")
              while True:
                  choix=gestion_d_echec("votre choix: ")
                  if choix==1:
                       prix_unit=gestion_d_echec("prix unitaire: ")
                       prix=prix_unit*a
                       nom_pretteur,date_de_paye=demande_nom_pretteur()
                       break
                  else:
                       prix=gestion_d_echec("prix total: ")
                       prix_unit=prix/a
                       nom_pretteur,date_de_paye=demande_nom_pretteur()
                       break
              try:
                        curseur.execute("""insert into ventes(date_vente,nombre,prix_vente_u,prix_vente_t,id_achat) values(%s,%s,%s,%s,%s);""",(date1,a,prix_unit,prix,id_achat_lie))
                        connexion.commit()
                        curseur.execute("""insert into dettes(date_emprunt,nom_pretteur,nombre,prix_dette_u,prix_dette_t,date_paye,id_achat,statut) values(%s,%s,%s,%s,%s,%s,%s,%s);""",[date1,nom_pretteur,a,prix_unit,prix,date_de_paye,id_achat_lie,statut])
                        connexion.commit()
                        print("Données enregistrées avec succès")
                        break
              except Exception as e:
                       connexion.rollback()
                       print(f"Erreur d'enregistrement{e}")
                  
def prix_calcul():                    
           a=gestion_d_echec("le nombre:")
           caracteristique=input("Veuillez entrez l'unité de mesure de la marchandise (par ex sac de riz ou koro de riz)")
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
                       prix_unitaire=prix/a
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
        date=r.strftime("%Y/%m/%d")
        return date,nom
def demande_nom_pretteur():
        nom=input("Nom du pretteur: ")
        date_de_paye=saisir_date("Veuillez entrez la date de paye svp: ")
        return nom,date_de_paye
def saisir_date(message):
    while True:
        date_str = input(f"{message} (format AAAA/MM/JJ) : ")
        try:
            date_objet = datetime.strptime(date_str, "%Y/%m/%d")
            return date_objet.strftime("%Y/%m/%d")
        except ValueError:
              print("Format invalide ! Veuillez respecter le format AAAA/MM/JJ (ex: 2026/04/20)")
affichage_choix()