import sys
import re
import urllib
import json
import os
import traceback
import pprint



pp = pprint.PrettyPrinter(indent=4)

values = dict()


# a cronjob hopefully keeps values.json synched from mbd.hu
def read_values():
    try: 
       with open('values.json') as f:
          v = json.load(f)
          
          #do a littlehealth check
          if (len(v)==0):
              print "values.json: nincs benne adat! "
          else:     
              values = v 
              print "Mostantol alkalmazott RFID<->ertek parosok: (osszesen "+str(len(values))+" darab):"
              pp.pprint (values)
              return
          
    except:
       print "Hiba a json file megnyitasanal... "
       print  "Internal error "+traceback.format_exc()

    
    if (len(values)==0):
       print "Nem sikerult RFID<->forintertek parosokat lehozni az http://mbd.hu/fundamenta/getValues.php -rol, probald kezzel!"
       exit()
          
          
           
        
        
    
    
print "Coin 1.0 ***"

# cronjob is frissiti majd, de biztos ami biztos kezdjuk ezzel
os.system (" wget -O values.json  http://mbd.hu/fundamenta/getValues.php")

read_values()
 

p = re.compile ('[0-9a-fA-F]{10}') 

while True:   
    line = (sys.stdin.readline()).rstrip()
    if (p.match(line)): 
        print ("RFID '"+line+"'")
    else:
        print ("nem RFID input '"+line+"'")
        continue
        
    
    if line in values:
        try:
            v = values.get(line)
            val = int(v)
        except:
            print  "Internal error "+traceback.format_exc()
            
               
        print "RFID erteke: "+str(val)
    else:
        print "Ismeretlen RFID, nincs hozzarendelt erme!"
        
                



