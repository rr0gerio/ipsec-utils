import os

RED = '31m'
GREEN = '32m'

def colorize(color, text):
    colored_text = f"\033[{color}{text}\033[00m"
    return colored_text

def getConnections():
    conns = os.popen("ipsec auto --status | grep '==='| awk -F ' ' '{print $2}' | awk -F '/' '{print $1}' | sed -E -e 's/\"|://g' | uniq | sort").read().split("\n")
    del conns[-1]
    return conns

def verifyConnections(conns):
    
    for conn in conns:
        publicIP = os.popen("ipsec auto --status | grep -w \\\""+conn+"\\\": | grep 'their id=' | awk -F ';' '{print $4}'| uniq | awk -F'=' '{print $2}'").read()
        try:
            tunnels = os.popen("ipsec auto --status | grep -w \\\""+conn+"\\\": | grep ===")
            print(f"\nConexão: {conn.upper()} - {publicIP}")
            for tunnel in tunnels:
                host = tunnel.split("===")[2].split(";")[0]
                status = tunnel.split("===")[2].split(";")[1]
                con_type = 'Host' if host.find("/32") != -1 else 'Subnet'
                if status == " erouted":
                    msg = colorize(GREEN,'OK!')
                else:
                    msg = colorize(RED, 'Verifique a conexão com o cliente') 
                print(f"    {con_type}: {host} {msg}")

        except Exception as e:
            print ("Error occured: {}".format(e))


if __name__ == "__main__":
    conns = getConnections()
    verifyConnections(conns)