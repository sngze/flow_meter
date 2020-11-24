import paho.mqtt.client as mqtt
import pymysql
from datetime import datetime

global db, cur, menulist

def on_connect(client, userdata, flags, rc):
    print("MQTT connected with result code " + str(rc))
    client.subscribe("system")
    client.subscribe("flowRate/+")
    client.publish("system", "Raspi Connect OK!")

def on_message(client, userdata, msg):
    #DB process
    
    sql = ""
    flow = 0.0
    date = "{}-{}-{}".format(datetime.today().year, datetime.today().month, datetime.today().day)
    menu = ""
    line = 1
    liters = 0.0

    #system message
    if "system" in msg.topic:
        print("[SYSTEM] : " + str(msg.payload))

    #flow message
    else:
        if "sensor1" in msg.topic:
            menu = menulist[0] 
            line = 1
        if "sensor2" in msg.topic:
            menu = menulist[1]
            line = 2
        if "sensor3" in msg.topic:
            menu = menulist[2]
            line = 3

        flow = str(msg.payload)
        
        #data availabillity check
        sql = "select max(liters) from flow_meter where date = %s and menu = %s;"
        cur.execute(sql, (date, menu))
        row = cur.fetchone()
        liters = row[0]
        
        if liters is None:
            print("[SYSTEM] : Add Record")
            
            for menu in menulist:
                sql = "insert into flow_meter values (%s, %s, %s, 0.0);"
                cur.execute(sql, (date, menu, line))
                line += 1
            
            db.commit()
        
        else:
            #update liters
            sql = "update flow_meter set liters = liters + %s where date = %s and menu = %s;"
            cur.execute(sql, (flow, date, menu))
            db.commit()
        
            #get liters
            sql = "select liters from flow_meter where date = %s and menu = %s;"
            cur.execute(sql, (date, menu))
            row = cur.fetchone()            
            liters = row[0]
        
            print(menu + " : + " + str(msg.payload) + " L   ( Total : " + str(liters) + " L )") 


#MENULIST
menulist = ["yirgacheffe", "sidamo", "brazil", "guatemala", "el salvador", "colombia", "mandeheling", "kenya"]


#DATABASE
db = pymysql.connect(host="localhost", user="raspi", password="0000", db="brewants", charset="utf8")
cur = db.cursor()



#MQTT
mqtt_broker_ip = "127.0.0.1"

client = mqtt.Client()
client.username_pw_set(username = "raspi", password = "0000")

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, 1883, 60)
client.loop_forever()




