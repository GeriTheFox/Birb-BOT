import time
import ibm_db
from decouple import config
from mcstatus import JavaServer

global conn

def reconnect():
    global conn
    try:
        conn = ibm_db.connect("DATABASE="+config('DB_NAME')+";HOSTNAME="+config('DB_HOST')+";PORT="+config('DB_PORT')+";PROTOCOL=TCPIP;UID="+config('DB_USER')+";PWD="+config('DB_PASS')+";", "", "")     
    except:    
        return False
    else:
        return True

def disconnect():
    global conn
    ibm_db.close(conn)


def check_if_exist(username):
    sql = "SELECT * FROM MC_PLAYTIME WHERE USERNAME = '"+str(username)+"'"
    stmt = ibm_db.exec_immediate(conn, sql)
    return ibm_db.fetch_assoc(stmt)

def insert_new_user(username):
    sql = "INSERT INTO MC_PLAYTIME(USERNAME,PLAYTIME) VALUES ('"+str(username)+"','1')"
    stmt = ibm_db.exec_immediate(conn, sql)

def update_time(username):
    sql = "UPDATE MC_PLAYTIME SET PLAYTIME = PLAYTIME + 1 WHERE USERNAME = '"+str(username)+"'"
    stmt = ibm_db.exec_immediate(conn, sql)

def update():
    while True:
        try:
            server = JavaServer.lookup("172.16.0.3:25565")
            query = server.query()
            if(reconnect()):
                i = 0
                while i < len(query.players.names):
                    if (check_if_exist(query.players.names[i])):
                        update_time(query.players.names[i])
                    else:
                        insert_new_user(query.players.names[i])
                    i = i + 1
                disconnect()
            else:
                print("DB not respondign")
            
        except:
            print("Server not respondign")

        time.sleep(60)

update()