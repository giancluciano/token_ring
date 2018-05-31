#!bin/bash/python
# -*- coding: utf-8 -*-

import socket
import time
import threading
import sys
from typing import Tuple
from collections import deque
from packet import Packet


class Computer(object):
    """xd"""
    
    def __init__(self, my_id: int):
        """
        from reading setup file
        my_socket_address: Tuple[str, int] = ('localhost', 5000),
        next_computer_address: Tuple[str, int] = ('localhost', 6000),
        tokenizer: bool=False

        It gets a tuple to set where to host the server,
        another tuple to set where to send his packets
        and a boolean to set whether it is the first computer on a network
        (defaults to false because this will only be used once)
        """
        # read setup file
        setup = self.read_file(my_id)
        # find IP, socket from id
        self.my_id = my_id
        self.my_socket_address = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.my_socket_address)

        self.next_computer_address = ""
        self.tokenizer = ""
        self.lock = threading.Lock()
        self.threads = []
        self.last_time = 0
        self.visited = False

    def start(self):

        if self.tokenizer:
            self.pass_token()

        user = threading.Thread(target=self.user_thread)
        token = threading.Thread(target=self.token_thread)
        timer = threading.Thread(target=self.time_thread)
        self.threads.append(user)
        self.threads.append(token)
        self.threads.append(timer)
        user.start()
        token.start()
        timer.start()
        
    def token_thread(self):
        print("Iniciou a thread token:")
        while True:
            # start thread to receive and send token
            # get packets from socket, cast to str, split(';')
            pckt = self.wait_connection().decode('utf-8').split(';')
            print("Recebi o token.")
            time.sleep(2)
            # write file with self.ip
            file = open("file.txt","w")
            file.write(str(self.my_socket_address))
            file.close()
            self.pass_token()
            self.last_time = time.time()
            self.visited = True

    def time_thread(self):
        print("iniciou thread time")
        # if time > than 10, read file to create new token and ask new IP
        if self.visited and time.time() - self.last_time > 10:
            file = open("file.txt","w+")
            text = file.read()
            if text == str(self.my_socket_address):#see if self was the last to write
                print(text)
                # ask user to type new ip and socket
                # pass new token
            else:
                time.sleep(10)
            file.close()
            
    def user_thread(self):
        print("iniciou thread user")
        while True:    
            if input() == "q":
                sys.exit()

    
    def connect(self, text: bytes=b"teste"):
        self.sock.sendto(text, self.next_computer_address)

    def wait_connection(self):
        incoming = self.sock.recv(1024)
        return incoming

    def pass_token(self):
        print("Sending token to", str(self.next_computer_address))
        self.connect(Packet('1234', 'nãocopiado', '', '', '').to_bytes())

    def read_file(self, my_id: int): #-> list:
        """
        id;'ip';socket
        """
        with open("setup.txt",'r') as setup_file:
            # create dictionary
            for line in setup_file:
                # split line
                # fill dictionary with id: tuple (ip,sock)
                print(line)
            return ''
            #return dictionary



"""
To run on a single machine,
open three ipython sessions and copypaste this
(must cd token_ring first)

from computer import Computer
pc = Computer('Gian', ('0.0.0.0', 5000), ('localhost', 6000),True)
pc.start()

from computer import Computer
pc = Computer('Nei', ('0.0.0.0', 6000), ('localhost', 7000))
pc.start()

from computer import Computer
pc = Computer('João', ('0.0.0.0', 7000), ('localhost', 5000))
pc.start()

Done with sending your texts, press Enter to leave a blank destination 
to start the token thread   

"""
# if __name__ == "__main__":
    # setup = read_file("")
