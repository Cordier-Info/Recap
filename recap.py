import pandas as pd
import numpy as np

L_classes_sauv = [["2nde",17,4.5],["2nde_ND",1,3],["SL",2,1.5],["1ES",12,1.5],["1SPC",8,4],["TES",12,1.5],["TSPC",4,6],["TSI",2,2],["1STI",3,6],["TSTI",3,6]]
L_classes = [["2nde",17,4.5],["2nde_ND",1,3],["SL",3,1.5],["1ES",12,1.5],["1SPC",8,4],["TES",12,1.5],["TSPC",4,6],["TSI",2,2],["1STI",3,6],["TSTI",3,6]]
L_qu = ["Combien de 2nde ? ","2nde non dédoublée ? ","Combien de SL ? ","Combien de 1ES ? ","Combien de 1SPC ? ","Combien de TES ? ","Combien de TSPC ? ","Combien de T-SI ? ","Combien de 1STI ? ","Combien de TSTI ? "]

nb, noms, classes = [],[],[]

for i in range(len(L_qu)):
    nb.append(0)

def init() :
    tableau = pd.DataFrame({'Noms' : [],'2nde' : [],'2nde_ND' : [],'SL' : [],'1ES' : [],'1SPC' : [],'TES' : [],'TSPC' : [],'TSI' : [],\
                        '1STI' : [],'TSTI' : [],'Service_dû' : [],'Service_effectif' : [],'Diff' : []},\
                       columns=['Noms','2nde','2nde_ND','SL','1ES','1SPC','TES','TSPC','TSI','1STI','TSTI','Service_dû','Service_effectif','Diff'])
    return tableau

tableau = init()

def voeux(tableau) :
    row = []
    nom = input("Nom ? ")
    service_du = int(input("Service ? "))
    service_eff = 0
    row += [nom]
    for i in range(len(L_classes)) :
        nb[i] = int(input(L_qu[i]))
        L_classes[i][1] -= nb[i]
        row += [nb[i]]
        service_eff += nb[i]*L_classes[i][2]
    row += [service_du]
    row += [service_eff]
    row += [service_eff-service_du]
    tableau.loc[len(tableau)] = row
    return tableau

def raz(tableau) :
    for i in range(1,len(tableau)) :
        tableau[i]=[]

def lire() :
    df = pd.read_csv('recap.csv',sep=',')
    df.apply(pd.to_numeric, errors='ignore')
    return df

def problemes(tableau) :
    print()
    s , NB , pofs_oui , profs_non  = [] , [] , [] , []
    b = c = pd.DataFrame({'A' : []})
    b = pd.DataFrame(L_classes_sauv)
    b = b[1]
    c = tableau.sum(axis = 0, skipna = True)[1:-2]
    c = pd.to_numeric(c)
    for i in range(len(L_classes_sauv)) :
        if c[i]<b[i] :
            print("- Il manque {} {}".format(int(b[i]-c[i]),L_classes_sauv[i][0]))
            sans = tableau[L_classes_sauv[i][0]] == 0
            profs_sans = tableau[sans]['Noms']
            print("Profs n'en ayant pas :",*profs_sans,sep='  ',end="")
            print()
        if c[i]>b[i] :
            print("- Il y a {} {} en trop".format(int(c[i]-b[i]),L_classes_sauv[i][0]))
            avec = tableau[L_classes[i][0]] >= 1
            profs_avec = tableau[avec]['Noms']
            NB = tableau[avec][L_classes_sauv[i][0]]
            print("Profs en ayant : ",end="")
            for k in range(len(profs_avec)) :
                print("{} ({})".format(list(profs_avec)[k],int(list(NB)[k])),end=" ")
            print()
    print()
    print("Profs n'ayant pas leur quota :")
    endessous = tableau["Diff"] < 0
    profs_endessous = tableau[endessous]['Noms']
    nbh1 = tableau[endessous]['Diff']
    for k in range(len(profs_endessous)) :
        print("{} ({} h)".format(list(profs_endessous)[k],list(nbh1)[k]),end=" ")
    print("")
    print("\nProfs avec bcp d'heures :")
    audessus = tableau["Diff"] > 2
    profs_audessus = tableau[audessus]['Noms']
    nbh2 = tableau[audessus]['Diff']
    for k in range(len(profs_audessus)) :
        print("{} ({} h)".format(list(profs_audessus)[k],list(nbh2)[k]),end=" ")

def aj_suppr(tableau) :
    while 1 :
        nom = input("Nom ? ")
        if nom in tableau.values : break
        print("pas dans la liste")
    A,B,C = zip(*L_classes_sauv)
    while 1 :
        classe = input("Classe ? ")
        if classe in A : break
        print("pas dans la liste")
    var = input("Nombre i de classes à ajouter (i>0) ou à retirer (i>0) : ")
    tableau.loc[tableau['Noms'] == nom, classe] += int(var)
    serv_eff = 0
    for e in L_classes :
        serv_eff += tableau.loc[tableau['Noms'] == nom, e[0]]*e[2]
    tableau.loc[tableau['Noms'] == nom, 'Service_effectif'] = serv_eff
    tableau.loc[tableau['Noms'] == nom, 'Diff'] = serv_eff - tableau.loc[tableau['Noms'] == nom, 'Service_dû']
    return tableau

def echange(tableau) :
    while 1 :
        nom = input("Qui donne ? ")
        if nom in tableau.values : break
        print("pas dans la liste")
    A,B,C = zip(*L_classes_sauv)
    while 1 :
        classe = input("Classe ? ")
        if classe in A : break
        print("pas dans la liste")
    if tableau.loc[tableau['Noms']==nom, classe].values[0] == 0 :
        print("Impossible, {} n'a aucune {} !".format(nom,classe))
        return tableau
    while 1 :
        recipiendaire = input("Qui prend ? ")
        if (recipiendaire in tableau.values) or (recipiendaire == 0): break
        print("pas dans la liste")
    while 1 :
        var = input("Combien ? ")
        if var in ['0','1','2','3'] : break
        print("pas une valeur autorisée")
    tableau.loc[tableau['Noms'] == nom, classe] -= int(var)
    if recipiendaire != '0' :
        tableau.loc[tableau['Noms'] == recipiendaire, classe] += int(var)
    serv_eff = 0
    serv_eff_rec = 0
    for e in L_classes :
        serv_eff += tableau.loc[tableau['Noms'] == nom, e[0]]*e[2]
        serv_eff_rec += tableau.loc[tableau['Noms'] == recipiendaire, e[0]]*e[2]
    tableau.loc[tableau['Noms'] == nom, 'Service_effectif'] = serv_eff
    tableau.loc[tableau['Noms'] == nom, 'Diff'] = serv_eff - tableau.loc[tableau['Noms'] == nom, 'Service_dû']
    if recipiendaire != '0' :
        tableau.loc[tableau['Noms'] == recipiendaire, 'Service_effectif'] = serv_eff_rec
        tableau.loc[tableau['Noms'] == recipiendaire, 'Diff'] = serv_eff_rec - tableau.loc[tableau['Noms'] == recipiendaire, 'Service_dû']
    return tableau

def tri(tableau) :
    tableau = tableau.sort_values('Noms')
    tableau.set_index('Noms',inplace=True)
    tableau.reset_index(inplace=True)
    return tableau

def sauve(tableau) :
    tableau.to_csv('recap.csv', index = False)
    #tableau.to_excel("recap.xlsx", index = False)
