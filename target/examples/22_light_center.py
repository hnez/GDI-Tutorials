#!/usr/bin/env python3

import tkinter as tk
import socket as so

class Arduino(object):
    def __init__(self, window, host, port, on_received):
        # Open socket and connect to the Arduino
        self.socket= so.socket()
        self.socket.connect((host, port))
        self.socket.setblocking(0)

        self.on_received= on_received

        self.rd_buff= bytes()

        # Call on_readable whenever the
        # Arduino sends a message
        window.createfilehandler(self.socket, tk.READABLE, self.on_readable)

    def send_command(self, command):
        self.socket.send(command.encode('utf-8') + '\n')

    def on_readable(self, sock, mask):
        self.rd_buff+= self.socket.recv(1024)

        while b'\n' in self.rd_buff:
            line, self.rd_buff= self.rd_buff.split(b'\n', 1)

            self.on_received(line.decode('utf-8'))

class LightCenterWindow(object):
    def __init__(self):
        # Setup the empty window
        self.setup_window()

        host= input('Hostname: ')
        port= input('Port: ')

        self.arduino= Arduino(
            self.window,
            host, int(port),
            self.on_received
        )

    def on_received(self, line):
        print('Got line: "{}"'.format(line))

    def setup_window(self):
        self.window= tk.Tk()
        self.window.title('Light Center')

    def run(self):
        'Execute the tkinter mainloop to display the Light center window'

        self.window.mainloop()

if __name__ == '__main__':
    window= LightCenterWindow()
    window.run()