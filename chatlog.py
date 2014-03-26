# -*- coding: cp1252 -*-

def editsyscfg(path):
    f = open(path+"\\system.cfg", "r")
    l=f.readline()
    myf = ""
    while l!='':
        if l.startswith("˜ œ—ž‹"):
            gchatlog = '˜ œ—ž‹'+chr(147)+chr(144)+chr(152)+chr(223)+chr(194)+chr(223)+chr(221)+chr(206)+chr(221)+chr(10)
            myf+=gchatlog
        else:
            myf+=l
        l=f.readline()
    f.close()
    g = open(path+"\\system.cfg", "w")
    g.write(myf)
    g.close()
