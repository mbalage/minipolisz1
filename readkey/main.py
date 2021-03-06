import time
import sys
import re
import urllib
import json
import os
import traceback
import pprint



sum = 0;

pp = pprint.PrettyPrinter(indent=4)
localwebroot = "/var/www/html"



# a cronjob hopefully keeps values.json synched from mbd.hu
def read_values():
    try: 
       with open('values.json') as f:
          v = json.load(f)
          
          #do a littlehealth check
          if (len(v)==0):
              print "values.json: nincs benne adat! "
          else:     
              #values = v 
              return v
          
    except:
       print "Hiba a json file megnyitasanal... "
       print  "Internal error "+traceback.format_exc()

    
    if (len(values)==0):
       print "Nem sikerult RFID<->forintertek parosokat lehozni az http://mbd.hu/fundamenta/getValues.php -rol, probald kezzel!"
       exit()
          
          
# hol tartottunk legutobb?
def read_sum():      
    try: 
       os.system (" wget -O lastsum.json  http://mbd.hu/fundamenta/getSum.php")         
       with open('lastsum.json') as f:
          v = json.load(f)
          pp.pprint(v)
          return int(v.get("sum", 33))
    except:
       print  "Internal error "+traceback.format_exc()
       return 0
           

# sum elmentese, biztos ami biztos
def write_sum(sum):      
    try: 
       os.system (" wget -O lastsetsum.json http://mbd.hu/fundamenta/setSum.php?newsum="+str(sum))         
    except:
       print  "Internal error "+traceback.format_exc()
    



def notify_client (value, sum):
    try: 
#        notify = dict()
#        notify["value"] = value
#        notify["sum"] = sum
#        notify["timestmap"] = str(int(time.time()))
#        pp.pprint (notify)
#        not_str = json.dumps (notify)

         notifystr = '<?xml version="1.0" encoding="utf-8" ?><newcoin timestamp="'+str(int(time.time())) +'" sum="'+ str(sum)+'" value="'+str(value)+'"></newcoin>'
         print (notifystr)

         file = open(localwebroot+"/newcoin.xml", 'w')
         file.write (notifystr)
         file.close()


    except:
       print  "Internal error "+traceback.format_exc()     
    
    

    
print "Coin 1.0 ***"

# cronjob is frissiti majd, de biztos ami biztos kezdjuk ezzel
os.system (" wget -O values.json  http://mbd.hu/fundamenta/getValues.php")
sum=read_sum()
print "Ezzel SUM-mal indulunk:"+str(sum)


# RFID regex
p = re.compile ('[0-9a-fA-F]{10}') 

while True:   

    values = read_values()
    print "Mostantol alkalmazott RFID<->ertek parosok: (osszesen "+str(len(values))+" darab):"
    pp.pprint (values)
    print "Varakozas RFID-re..."

    line = (sys.stdin.readline()).rstrip()
    if (p.match(line)): 
        print ("RFID '"+line+"'")
    else:
        print ("Nem RFID input '"+line+"'")
        continue
        
 
    pp.pprint (values)
    try:   
        v = values.get(line)
        val = int(v, 0)
        if (val == 0):
            print "Ismeretlen RFID, nincs hozzarendelt erme!"            
            continue
        print "RFID-hez rendelt erme erteke: "+str(val)     
        
        sum += val
        
        print "Az uj SUM: "+str(sum)
        write_sum (sum) 
        
        #write a json file with now timestamp to local web server - client picks it up
        notify_client (val, sum)
        
        print ()
        
              
            
    except:
        print  "Internal error "+traceback.format_exc()
        
                



