import paramiko
import sys
import time
import getpass
import os

print "This is the script for changing the Training Room Environment."

ip = "10.255.254.101"
enable = "enable"
conf = "configure terminal"
termlength = "terminal length 0"
wr = "wr mem"
FrontRowPorts = ["2/39"  , "2/43" , "2/45" , "2/47" , "3/36" , "3/40" , "3/42" , "3/44" , "3/46"]
BackRowPorts =  ["2/23" , "3/24" , "2/25" , "3/26" , "2/27" , "3/28" , "2/29" , "3/30" , "2/31" , "3/32" , "2/33" , "3/34" , "2/35" , "2/37" , "3/38"]
TrainingRoomPorts = FrontRowPorts + BackRowPorts
F = len(FrontRowPorts)
B = len(BackRowPorts)
T = len(TrainingRoomPorts)
DIR = os.path.normpath("TrainingRoomChange.txt")
username = raw_input("Please provide the username to connect:\t")
password = getpass.getpass()

class REPLACE():
 
    def __init__(self, ipaddr):
        self.ipaddr = ipaddr
        self.DIR = DIR
        remote_conn_pre = paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(self.ipaddr, username=username, password=password, look_for_keys= False, allow_agent= False)
        print "SSH connection established to %s" % self.ipaddr
        remote_conn = remote_conn_pre.invoke_shell()
        remote_conn.send(termlength + "\r") 
        time.sleep(1)
        output = remote_conn.recv(1000)
        remote_conn.send("\r") 
        remote_conn.send(conf + "\r") 
        i = 0
        while i != F:
            remote_conn.send("interface " + FrontRowPorts[i] + "\r") 
            remote_conn.send("untagged vlan " +Vlan + "\r") 
            i += 1
        remote_conn.send("end" +"\r")
        remote_conn.send(wr +"\r")
        time.sleep(1)
        h = 0
        while h != F:
            remote_conn.send("show run interface " + FrontRowPorts[h] + "\r") 
            output += remote_conn.recv(65534)
            h += 1
            time.sleep(2)
        self.output = output
        self.conn = remote_conn

    def Replace_IP(self):
        time.sleep(2)
        f = open(self.DIR, "w")
        f.write(self.output)
        f.close()

class REPLACE_ALL():
 
    def __init__(self, ipaddr):
        self.ipaddr = ipaddr
        self.DIR = DIR
        remote_conn_pre = paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(self.ipaddr, username=username, password=password, look_for_keys= False, allow_agent= False)
        print "SSH connection established to %s" % self.ipaddr
        remote_conn = remote_conn_pre.invoke_shell()
        remote_conn.send(termlength + "\r") 
        time.sleep(1)
        output = remote_conn.recv(1000)
        remote_conn.send("\r") 
        remote_conn.send(conf + "\r") 
        i = 0
        while i != T:
            remote_conn.send("interface " + TrainingRoomPorts[i] + "\r") 
            remote_conn.send("untagged vlan " +Vlan + "\r") 
            i += 1
        remote_conn.send("end" +"\r")
        remote_conn.send(wr +"\r")
        time.sleep(1)
        h = 0
        while h != T:
            remote_conn.send("show run interface " + TrainingRoomPorts[h] + "\r") 
            output += remote_conn.recv(65534)
            h += 1
            time.sleep(2)
        self.output = output
        self.conn = remote_conn

    def Replace_All_IP(self):
        time.sleep(2)
        f = open(self.DIR, "w")
        f.write(self.output)
        f.close()
    

while True:
    FrontRow = raw_input("Would you like to change the Front Row only: y/n?\t")
    FrontRow = FrontRow.lower()
    print FrontRow
    if FrontRow == "y":
        Vlan = raw_input("Which vlan, ex:233?\t")
        FR = REPLACE(ip)
        FR.Replace_IP()
        break
    elif FrontRow == "n":
        Vlan = raw_input("Which vlan, ex:233?\t")
        TR = REPLACE_ALL(ip)
        TR.Replace_All_IP()
        break
    print "Invalid entry, try again."