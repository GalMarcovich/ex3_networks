"""
Noam Cohen - 208995902
Gal Marcovich - 208715367
"""

import socket
from socket import socket, AF_INET, SOCK_STREAM
import sys

# the global dictionary - all_files_dict = {'file_name': ['ip', 'port']}
all_files_dict = {}


# find files that fits to what the user asked for
def find_files(part_of_filename):
    list_of_files = []
    # go over the global dictionary
    for key, value in all_files_dict.iteritems():
        # if the file_name include the user's "word" - add the file
        if part_of_filename in key:
            list_of_files.append(str(key) + " " + str(value[0]) + " " + str(value[1]))
    return ",".join(list_of_files) + "\n"


# enter all the files the user shared to a global dictionary with his IP and the listen_port
def insert_to_dict(data, addr):
    for file in range(2, len(data)):
        all_files_dict[data[file]] = [addr[0], data[1]]


# read the file
def send_file(file_name, conn):
    if '.ico' or '.jpg' in file_name:
        file = open(file_name, 'rb')
    else:
        file = open(file_name, 'r')
    buffer_size = 2048
	chunk = file.read(buffer_size)
	while chunk:
		if not chunk:
			break  # EOF
		# send the data
		conn.send(chunk)
		# continue to read
		chunk = file.read(buffer_size)


# handle the two modes - 1 for adding and 2 for searching
def handle_msg(data, addr, conn):
    # message = data.split(" ")
    # # if the first word is 1 - add the files the client has to the global dictionary
    # if message[0] == "‫‪HTTP/1.1‬‬":
    #     if message[1]:
    #         insert_to_dict(message, addr)
    #     return
    # # if the first word is 2 - search for files fits to what the user entered
    # elif message[0] == "2":
    #     # needs to be just a number and a word (or number)
    #     if len(message) == "‫‪HTTP/1.2‬":
    #         # look for fitting files
    #         str_files = find_files(message[1])
    #         # send the list of files to the user
    #         conn.send(str_files)
    # # if the user entered number different than 1 or 2
    # else:
    #     return
    message = data.split(" ")
    name_of_file = message[1]
    if name_of_file == "/":
        name_of_file = "index.html"
        # if '\n' in message[2]:  # TODO - ?
        i = 4
    send_file(name_of_file, conn)
    while message[i] != "Connection":
        i += 1


# function main - open the socket and handling the connection to the client
def main(server_port):
    source_ip = '0.0.0.0'
    # the arg of the port we will listen on
    source_port = server_port
    buffer_size = 2048

    # open a socket
    s = socket(AF_INET, SOCK_STREAM)
    # connect the server to a specific ip and port
    s.bind((str(source_ip), int(source_port)))
    s.listen(1)

    # receive and send messages from and to the client
    while True:
        conn, addr = s.accept()
        while True:
            data = conn.recv(buffer_size)
            if not data:
                break
            # handle the two modes - add and search
            handle_msg(data, addr, conn)
        conn.close()


# main function
if __name__ == "__main__":
    main(int(sys.argv[1]))
