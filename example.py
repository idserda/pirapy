#!/usr/bin/python
from pira import PiraRDS

rds = PiraRDS('/dev/ttyUSB0', 1200, autostore=True)

if rds.setDps1('This is your favorite radio station!') is PiraRDS.SUCCES:
	print "PS1 Changed succesfully"

if rds.isRt1en(): 
	print "Radiotext 1 enabled"

print "Current PI is %s" % rds.getPi()
