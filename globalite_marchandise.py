from traduction_json import lecture_json
class Marchandise:
   def __init__(self,date,nom,nombre,caracteristique,prix_total,identifiant):
        self.identifiant=identifiant
        self.nom=nom
        self.nombre=nombre
        self.caracteristique=caracteristique
        self.date=date
        self.prix_unitaire=None
        self.prix_total=prix_total
   def __str__(self):   
       return f"date:{self.date}\nnom:{self.nom}\nnombre:{self.nombre}\nprix total:{self.prix}"
   def affichage(self):
         print(self.__str__)
   def traduction_en_dict(self):
        return {
             "identifiant":self.identifiant,
             "date":self.date,
             "nom":self.nom,
             "nombre":self.nombre,
             "prix unitaire": self.prix_unitaire,
             "prix total":self.prix_total,
             "caracterisque":self.caracteristique
        }
class Vente(Marchandise):
        def __init__(self, date,nom,nombre,caracteristique,prix_total,identifiant):
           super().__init__(date, nom,nombre,caracteristique, prix_total,identifiant)
class Mes_dettes(Marchandise):
   def __init__(self, nom_pretteur, date, nom,nombre,caracterisque,prix_total,identifiant,date_de_paye):
       super().__init__(date, nom, nombre,caracterisque,prix_total,identifiant)
       self.nom_pretteur=nom_pretteur
       self.date_de_paye=date_de_paye
   def __str__(self):
       return super().__str__()+f"\nnom pretteur:{self.nom_pretteur}\ndate de paye:{self.date_de_paye}\n"
class Achat(Marchandise):
        def __init__(self, date,nom,nombre,caracterisque,prix_total,identifiant):
           super().__init__(date, nom, nombre,caracterisque,prix_total,identifiant)
class Globalite:
     def __init__(self):
          self.vente=[]
          self.achat=[]
          self.dette=[]
     def traduction_dict(self):
          meuble_de_rangement={
               "les achats":[],
               "les ventes":[],
               "les dettes":[]
          }
          for i in self.achat:
               meuble_de_rangement["les achats"].append(i.traduction_en_dict())
          for i in self.vente:
               meuble_de_rangement["les ventes"].append(i.traduction_en_dict())
          for i in self.dette:
               meuble_de_rangement["les dettes"].append(i.traduction_en_dict())
          return meuble_de_rangement
     def modification(self,choix,x,y,z):
         w=lecture_json("fichier.json")
         if choix==1:
              liste_vente=w["les achats"]
              for marchandise in liste_vente:
                   if str(marchandise["identifiant"])==str(x):
                        print("ID trouvé")
                        marchandise[y.lower()]=z
                        if y.lower()=="nombre" or y.lower()=="prix unitaire":
                              if marchandise["prix unitaire"]!=None:
                                 marchandise["prix total"]=marchandise["prix unitaire"]*marchandise["nombre"]
         elif choix==2:
              liste_vente=w["les ventes"]
              for marchandise in liste_vente:
                   if str(marchandise["identifiant"])==str(x):
                        print("ID trouvé")
                        marchandise[y.lower()]=z
                        if y.lower()=="nombre" or y.lower()=="prix unitaire":
                             if marchandise["prix unitaire"]!=None:
                                 marchandise["prix total"]=marchandise["prix unitaire"]*marchandise["nombre"]
         elif choix==3:
              liste_vente=w["les dettes"]
              for marchandise in liste_vente:
                   if str(marchandise["identifiant"])==str(x):
                        print("ID trouvé")
                        marchandise[y.lower()]=z
                        if y.lower()=="nombre" or y.lower()=="prix unitaire":
                              if marchandise["prix unitaire"]!=None:
                                 marchandise["prix total"]=marchandise["prix unitaire"]*marchandise["nombre"]
         return w
     def supprimer(self,choix,id):
          w=lecture_json("fichier.json")
          if choix==1:
               liste_vente=w["les achats"]
               for marchandise in liste_vente:
                   if str(marchandise["identifiant"])==str(id):
                        liste_vente.remove(marchandise)
                        break
          elif choix==2:
                liste_vente=w["les ventes"]
                for marchandise in liste_vente:
                   if str(marchandise["identifiant"])==str(id):
                       liste_vente.remove(marchandise)
                       break
          elif choix==3:
               liste_vente=w["les dettes"]
               for marchandise in liste_vente:
                   if str(marchandise["identifiant"])==str(id):
                       liste_vente.remove(marchandise)
                       break
          return w
     def rechercher(self,choix,id):
           w=lecture_json("fichier.json")
           if choix==1:
                liste_vente=w["les achats"]
                for marchandise in liste_vente:
                     if str(marchandise["identifiant"])==str(id):
                         print("trouvé")
                         return marchandise,w
     def benefice(self):
          pass