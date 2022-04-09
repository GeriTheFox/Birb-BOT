import discord
import ibm_db
from mcstatus import JavaServer
from decouple import config


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

def playtime():
    global conn
    if(reconnect()):
        sql = "SELECT * FROM MC_PLAYTIME ORDER BY 'PLAYTIME' DESC LIMIT 10"
        stmt = ibm_db.exec_immediate(conn, sql)
        tuple = ibm_db.fetch_assoc(stmt)
        array = []
        while tuple != False:
            array.append(tuple)
            tuple = ibm_db.fetch_assoc(stmt)
        disconnect()
        return array
        
    else:
        return False



client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('>mc_info'):
        try:
            server = JavaServer.lookup("172.16.0.3:25565")
            status = server.status()
            query = server.query()
            embed=discord.Embed(title="play.avali.hu", url="https://play.avali.hu", description="if you want to join click on the link above to see instrutions about how to download and install the required modpack", color=0x00ffff)
            embed.set_author(name="The server has "+str(status.players.online)+" / 20 players online")
            embed.set_thumbnail(url="https://avali.hu/mc.png")
            embed.set_footer(text= "online: "+', '.join(query.players.names))
            await message.channel.send(embed=embed)
        except:
            await message.channel.send("The server not responding")

    if message.content.startswith('>mc_top'):
        try:
            data = playtime()
            i = 0
            j = 1
            playtimes = ""
            while (len(data) > i):
                min = int(data[i]['PLAYTIME'])
                if (min > 60):
                    time_string = "{}:{}".format(*divmod(min, 60))
                    playtimes = playtimes + str(j)+'. '+data[i]['USERNAME']+' | '+time_string+' Hour \n'
                else:
                    playtimes = playtimes + str(j)+'. '+data[i]['USERNAME']+' | '+str(min)+' Min \n'
                i = i + 1
                j = j + 1


            embed=discord.Embed(title="play.avali.hu", url="https://play.avali.hu", description=playtimes, color=0xff8c00)
            embed.set_author(name="Top 10 player who wasted the most time there:")
            embed.set_thumbnail(url="https://avali.hu/mc_stat.png")
            embed.set_footer(text= "I am not sorry")
            await message.channel.send(embed=embed)
        except:
            await message.channel.send("The server not responding")


client.run(config('TOKEN'))