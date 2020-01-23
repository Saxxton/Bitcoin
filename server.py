
#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import urllib.request
import time
import datetime
import hashlib
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  def do_POST(self):
      self.send_response(200)
    # Send headers
      self.send_header('Content-type','text/html')
      self.end_headers()
      content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
      post_data = self.rfile.read(content_length) # <--- Gets the data itself
      post_data = str(post_data)
      temp = post_data.split("'")
      arr = temp[1].split("&")
      names = []
      params = []
      for data in arr:
          tt = data.split("=")
          names.append(tt[0])
          params.append(tt[1])
      if (names[0] == "from" and names[1] == "to" and names[2] == "value"):
          valueisint = True
          try:
              int(params[2])
          except ValueError:
              valueisint = False
          if(str(params[0].strip()) != "" and str(params[1].strip()) != "" and str(params[2].strip()) != "" and valueisint):
              transfer("",self.client_address[0],"A",params[1],params[0],params[2],'0000', True)
              self.wfile.write(('<html><body><h1>Transfer Completed!</h1><br><br><a href="http://'+str(self.client_address[0]) +":" + str(servport)+'"><input type="button" value="Back"></a></body></html>').encode('utf-8'))
          else:
              self.wfile.write(('<html><body><h1>Wrong Data</h1><a href="http://'+str(self.client_address[0]) +":" + str(servport)+'"><input type="button" value="Back"></a></body></html>').encode('utf-8'))
  
  # GET
  def do_GET(self):
    # Send response status code
    self.send_response(200)
    # Send headers
    self.send_header('Content-type','text/html')
    self.end_headers()
    names = []
    params = []
    strr = "{}".format(self.path)
    #print(self.client_address[0])
    if len(strr) > 1:
        req = []
        req = strr.strip().split("/")
        if len(req) == 3:
            if req[1] == "getdata":
                transfers = gettransfers()
                arr = transfers.split("*")
                self.wfile.write("Your's transfer:<br>".encode('utf-8'))
                counter = 0
                for data in arr:
                    if (data.strip() != ""):
                        datas = data.split("|")
                        tempdata = datas[0].split(":")
                        if tempdata[1].strip() == req[2]:
                            counter += 1
                            self.wfile.write(data.encode('utf-8'))
                if counter == 0:
                    self.wfile.write("Not found".encode('utf-8'))
            if req[1] == "getblocks":
                if req[2].strip() != "":
                    transfers = gettransfers()
                    arr = transfers.split("*")
                    booleanka = False
                    self.wfile.write(("Transfers from " + req[2] + ":<br><br>").encode('utf-8'))
                    for data in arr:
                        if (data.strip() != ""):
                            if booleanka:
                                self.wfile.write(data.encode('utf-8'))
                                self.wfile.write("<br>".encode('utf-8'))
                            else:
                                    datas = data.split("|")
                                    tempdata = datas[0].split(":")
                                    if tempdata[1].strip() == req[2]:
                                        booleanka = True
                                        self.wfile.write(data.encode('utf-8'))
                                        self.wfile.write("<br>".encode('utf-8'))
                    if not booleanka:
                        self.wfile.write("Not founded!".encode('utf-8'))
                else:
                    transfers = gettransfers()
                    arr = transfers.split("*")
                    self.wfile.write("Transfers:<br><br>".encode('utf-8'))
                    for data in arr:
                        self.wfile.write(data.encode('utf-8'))
                        self.wfile.write("<br>".encode('utf-8'))
                    self.wfile.write(('<a href="http://'+str(self.client_address[0]) +":" + str(servport)+'"><input type="button" value="Back"></a>').encode('utf-8'))
        if strr.strip() == "/servers/":
            servers = getservers()
            arr = servers.split("|")
            self.wfile.write("Servers:<br><br>".encode('utf-8'))
            for data in arr:
                self.wfile.write(data.encode('utf-8'))
                self.wfile.write("<br>".encode('utf-8'))
            self.wfile.write(('<a href="http://'+str(self.client_address[0]) +":" + str(servport)+'"><input type="button" value="Back"></a>').encode('utf-8'))
        b = strr.split('?')
        if (len(b) > 1):
            if b[0] == "/request": 
                a = b[1].split('&')
                for x in range(0, len(a)):
                    temp = a[x].split('=')
                    names.append(temp[0])
                    params.append(temp[1])
                #Zaprosi
                if (names[0] == "transaction" and params[0] == "delme"):
                    if names[1] == "ip":
                        deleteserver(params[1])
                if (names[0] == "transaction" and params[0] == "addtransfer"):
                    if (names[1] == "port" and names[2] == "id" and names[3] == "ip"
                    and names[4] == "date" and names[5] == "from" and names[6] == "to" and names[7] == "value"):
                        transfer(params[2],params[3],params[4],params[5],params[6],params[7],params[1], False)
                if (names[0] == "transaction" and params[0] == "transfer"):
                    if names[1] == "from" and names[2] == "to" and names[3] == "value":
                        transfer("",self.client_address[0],"A",params[2],params[1],params[3],'0000', True)
                if (names[0] == "transaction" and params[0] == "givetransfers"):
                    self.wfile.write(gettransfers().encode('utf-8'))
                if (names[0] == "transaction" and params[0] == "giveservers"):
                    self.wfile.write(getservers().encode('utf-8'))
                if (names[0] == "transaction" and params[0] == "addme"):
                    if names[1] == "port":
                        if str(servport) == "8080":
                            addme("127.0.0.1:" + params[1], True)
                        else:
                            addme("127.0.0.1:" + params[1], False)
        
    else:
        content = '<html><body><h1>Transfer Form</h1><br><br><form action="/" method="get" target="_self">From: &nbsp;<input type="text" name="from"><br>To: &nbsp; &nbsp; &nbsp; <input type="text" name="to"><br>Value: &nbsp;<input type="text" name="value"><br><br><button type="submit" formmethod="post">Transfer</button></form><a href="http://'+str(self.client_address[0]) +":" + str(servport)+'/servers/"><input type="button" value="Servers"></a><a href="http://'+ "127.0.0.1:" + str(servport)+'/getblocks/"><input type="button" value="Transfers"></a></body></html>' 
        self.wfile.write(content.encode('utf-8'))
    return

def updatetransfers(key,ip,date,frompers,topers,value,port):
    if date == "A":
        date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    temp = "servers"+ str(servport) +".txt"
    already = True
    if str(port) == '0000':
        already = False
    try:
       file = open(temp, 'r')
    except IOError:
       file = open(temp, 'w')
    with open(temp, "r") as ins:
       servers = []
       for line in ins:
           if line.strip() != "":
              servers.append(line)
    for ip in servers:
        ip = ip.replace("\n", "")
        if already:
            if ip.split(":")[1] != str(port):
                request = "http://" + ip + "/request?transaction=addtransfer&port=" + str(port)+ "&id="+str(key)+"&ip="+str(ip)+"&date="+str("A")+"&from="+str(frompers)+"&to="+str(topers)+"&value="+str(value)
                contents = urllib.request.urlopen(request).read()
        else:
            request = "http://" + ip + "/request?transaction=addtransfer&port=" + str(port)+ "&id="+str(key)+"&ip="+str(ip)+"&date="+str("A")+"&from="+str(frompers)+"&to="+str(topers)+"&value="+str(value)
            contents = urllib.request.urlopen(request).read()
    file.close() 

def transfer(key,ip,date,topers,frompers,value,port,mine):
    if date == "A":
        date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    temp = "transfers"+ str(servport) +".txt"
    try:
       file = open(temp, 'a')
    except IOError:
       file = open(temp, 'w')
    if key.strip() == "":
        key = hashlib.sha1(date.encode('utf-8'))
        key = key.hexdigest()[:9]
    file.write("ID:"+str(key)+"|IP:"+str(ip)+"|Date:"+str(date)+"|From:"+str(frompers)+"|To:"+str(topers)+"|Values:"+str(value)+"*" + "\n")
    if str(servport) == "8080":
        updatetransfers(key,ip,time,frompers,topers,value,port)
    else:
        if mine:
            request = "http://127.0.0.1:8080/request?transaction=addtransfer&port=" + str(servport)+ "&id="+str(key)+"&ip="+str(ip)+"&date="+str("A")+"&from="+str(frompers)+"&to="+str(topers)+"&value="+str(value)
            contents = urllib.request.urlopen(request).read()
    
def gettransfers():
    temp = "transfers"+ str(servport) +".txt"
    try:
       file = open(temp, 'r')
    except IOError:
       file = open(temp, 'w')
    with open(temp, "r") as ins:
       first = True
       transfers = ""
       for line in ins:
           if first:
            first = False
            transfers += line
           else:
            transfers += "*" + line
    file.close()
    return transfers

def getservers():
    temp = "servers"+ str(servport) +".txt"
    try:
       file = open(temp, 'r')
    except IOError:
       file = open(temp, 'w')
    with open(temp, "r") as ins:
       first = True
       servers = ""
       for line in ins:
           if first:
            first = False
            servers += line
           else:
            servers += "|" + line
    file.close()
    return servers

def updateserver(port):
    temp = "servers"+ str(servport) +".txt"
    try:
       file = open(temp, 'r')
    except IOError:
       file = open(temp, 'w')
    with open(temp, "r") as ins:
       servers = []
       for line in ins:
           if line.strip() != "":
              servers.append(line)
    for ip in servers:
        ip = ip.replace("\n", "")
        if ip.split(":")[1] != str(port):
            request = "http://" + ip + "/request?transaction=addme&port=" + str(port)
            contents = urllib.request.urlopen(request).read()
    file.close()

def addme(ip,mainserver):
    temp = "servers" + str(servport) + ".txt"
    try:
       file = open(temp, 'a')
    except IOError:
       file = open(temp, 'w')
    arr = ip.split(":")
    add = True
    with open(temp, "r") as ins:
       servers = []
       for line in ins:
          if line == ip:
              add = False
    if add:
        if arr[1] != str(servport):
            if ip.strip() != "":
                file.write(ip + "\n")
            file.close()
    if mainserver:
        updateserver(arr[1])
    
def deleteserver(ip):
    temp = "servers"+ str(servport) +".txt"
    try:
       file = open(temp, 'r')
    except IOError:
       file = open(temp, 'w')
    with open(temp, "r") as ins:
       servers = []
       for line in ins:
           if str(line.strip()) != str(ip.strip()):
               servers.append(line)
    file.close()
    file = open(temp, 'w')
    for data in servers:
        file.write(data)
    file.close()
    if str(servport) == "8080":
      for data in servers:
          data = data.replace("\n", "")
          if data != ip:
            request = "http://" + data + "/request?transaction=delme&ip=" + str(ip)
            contents = urllib.request.urlopen(request).read()  

def run(server_class=HTTPServer, handler_class=testHTTPServer_RequestHandler, port=8080):
  from sys import argv
  print('Starting server...')
  server_address = ('', port)
  print('On port:', port)
  global servport
  servport = port
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  httpd = HTTPServer(server_address, handler_class)
  print('Running server...')
  temp = "servers" + str(servport) + ".txt"
  file = open(temp, 'w')
  if str(servport) != "8080":
      request = "http://127.0.0.1:8080/request?transaction=giveservers"
      contents = urllib.request.urlopen(request).read()
      contents = contents.decode('utf-8')
      arr = contents.split("|")
      file.write("127.0.0.1:8080" + "\n")
      for data in arr:
          if len(data.split(":")) > 1:
              if data.split(":")[1] != str(servport):
                  if data.strip() != "":
                      file.write(data + "\n")
      file.close()
  if str(servport) != "8080":
      temp = "transfers" + str(servport) + ".txt"
      file = open(temp, 'w')
      request = "http://127.0.0.1:8080/request?transaction=givetransfers"
      contents = urllib.request.urlopen(request).read()
      contents = contents.decode('utf-8')
      arr = contents.split("*")
      for data in arr:
          if len(data.split("|")) > 3:
              file.write(data + "*" + "\n")
      file.close()
                   
  if str(servport) != "8080":
      request = "http://127.0.0.1:8080/request?transaction=addme&port=" + str(servport)
      contents = urllib.request.urlopen(request).read()
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      if str(servport) != "8080":
        request = "http://127.0.0.1:8080/request?transaction=delme&ip=" + str("127.0.0.1:"+str(servport))
        contents = urllib.request.urlopen(request).read()
      print("Shutting Down....")
      sys.exit(0)


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
        
