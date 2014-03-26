# -*- coding: cp1252 -*-
import time
from lang import *

def apply_settings():
    global path, lang
    f = open("config.cfg", "r")
    line = f.readline()
    while line != "":
        if line.startswith("lang="):
            t = line.split("=")
            if "English" in t[1]:
                lang = en_EN
            elif "Français" in t[1]:
                lang = fr_FR
        if line.startswith("gamefile_path="):
            t = line.split("=")
            path = t[1][:-1] #remove the \n
        line = f.readline()
    if not lang:
        lang = en_EN
    f.close()
    return lang

apply_settings()

apbook = {
    "[item:186000066;ver4;;;;]":lang["i_i"],
    "[item:186000065;ver4;;;;]":lang["i"],
    "[item:186000064;ver4;;;;]":lang["i_s"],
    "[item:186000063;ver4;;;;]":lang["i_m"],
    "[item:186000062;ver4;;;;]":lang["s_i"],
    "[item:186000061;ver4;;;;]":lang["s"],
    "[item:186000060;ver4;;;;]":lang["s_s"],
    "[item:186000059;ver4;;;;]":lang["s_m"],
    "[item:186000058;ver4;;;;]":lang["t_i"],
    "[item:186000057;ver4;;;;]":lang["t"],
    "[item:186000056;ver4;;;;]":lang["t_s"],
    "[item:186000055;ver4;;;;]":lang["t_m"],
    "[item:186000054;ver4;;;;]":lang["c_i"],
    "[item:186000053;ver4;;;;]":lang["c"],
    "[item:186000052;ver4;;;;]":lang["c_s"],
    "[item:186000051;ver4;;;;]":lang["c_m"]
    }

apbank= {
    lang["c_m"]:[0,9600],
    lang["c_s"]:[0,7200],
    lang["c"]:[0,4800],
    lang["t_m"]:[0,4800],
    lang["t_s"]:[0,3600],
    lang["c_i"]:[0,2400],
    lang["t"]:[0,2400],
    lang["s_m"]:[0,2400],
    lang["s_s"]:[0,1800],
    lang["t_i"]:[0,1200],
    lang["s"]:[0,1200],
    lang["i_m"]:[0,1200],
    lang["i_s"]:[0,900],
    lang["s_i"]:[0,600],
    lang["i"]:[0,600],
    lang["i_i"]:[0,300]
    }

#----------------- class Sharer() ---------------------

class Sharer(list):
    def __init__(self,nb_j):
        list.__init__(self)
        self.nb_j=nb_j
        distrib=Distribution(self.nb_j)
        self.append(distrib)
		
    def newDistribution(self):
        distrib = Distribution(self.nb_j)
        self.append(distrib)
		
    def add(self,d,j,relic):
        self[d-1].add(j,relic) #Ajout au joueur j dans la distribution d +relic

    def total(self):
        t = []
        for n in range(self.nb_j):
            t.append(0)
        for i in range(len(self)):
            for j in range(len(self[i])):
                n = self[i][j].total()
                t[j]+= n
        return t
        
    def share(self,ls):
        st = []
        #Calque de ls traduit en int (ex: ["Icône antique"]->[600])
        for i in ls:
            n = apbank[i][1]
            st.append(n)
        #Boucle de partage tant que ls n'a pas été vidé
        while ls != []:
            n = 99999999999
            p = 0
            t = self.total()
            #On determine qui va recevoir les AP
            for i in range(len(t)):
                if t[i]<n:
                    n = t[i]
                    joueur = i+1
            #On determine la relique la plus haute qui va Ãªtre envoyée
            for i in range(len(ls)):
                if st[i]>p:
                    p = st[i]
                    k = i
                    relic = ls[i]
            ls.pop(k)
            st.pop(k)
            self.add(len(self),joueur,relic)
        #Distribution terminée, création d'une nouvelle Distribution.
        self.newDistribution()
                    

class Distribution(list):
    def __init__(self, nb_j):
        list.__init__(self)
        for i in range(nb_j):
            joueur = Joueur()
            self.append(joueur)
            
    def add(self,j,relic):
    	self[j-1].add(relic) #Ajout au joueur j +relic
   
    def total(self):
        t = []
        for j in self:
            st = j.total()
            t.append(st)
        return t

class Joueur(dict):
    def __init__(self):
        dict.__init__(self)
        self[lang["c_m"]]=0
        self[lang["c_s"]]=0
        self[lang["c"]]=0
        self[lang["c_i"]]=0
        self[lang["t_m"]]=0
        self[lang["t_s"]]=0
        self[lang["t"]]=0
        self[lang["t_i"]]=0
        self[lang["s_m"]]=0
        self[lang["s_s"]]=0
        self[lang["s"]]=0
        self[lang["s_i"]]=0
        self[lang["i_m"]]=0
        self[lang["i_s"]]=0
        self[lang["i"]]=0
        self[lang["i_i"]]=0

    def add(self,relic):
        self[relic]+=1

    def total(self):
        t = 0
        for r in self:
            t += self[r]*apbank[r][1]
        return t

##################### End of class Sharer()#####################
    
def save_settings(**kwargs):
    statments = ["gamefile_path","lang"]
    f = open("config.cfg", "w")
    for key, value in kwargs.iteritems():
        f.write(key+"="+value+"\n")
    f.close()

def get_the_roll(line, f):
    dic = {}
    n = int(line.split(" ")[-2])
    while(n>0):
        if line.find(lang["statment1"]) != -1:
            splitted = line.split(" ")
            dic[splitted[3]] = splitted[-4]
            print "Got it : "+splitted[3]+" "+splitted[-4]
            n=n-1
        line = f.readline()
    return dic

def string_position(n):
    if n==1:
        return lang["first"]
    if n==2:
        return lang["second"]
    else:
        return lang["rd"]
