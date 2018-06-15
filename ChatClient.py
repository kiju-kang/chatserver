#!/usr/bin/python3
import socket
import threading
import tkinter

BUFSIZ=1024
host='127.0.0.1'
port=19787

def recv_message(sock):
    while True:
        try:
            message=sock.recv(BUFSIZ).decode()
            message_box.insert(tkinter.END, message)
            #for auto-scroll
            message_box.select_clear(message_box.size()-2)
            message_box.select_set(tkinter.END)
            message_box.yview(tkinter.END)
        except:
            break

def send_message(event=None):
    message=input_text.get()
    input_text.set("")
    sock.sendall(message.encode())
    if message=="Bye!":
        sock.close()
        top.quit()

def on_closing(event=None):
    input_text.set("Bye!")
    send_message()

top=tkinter.Tk()
top.title("Chat Box")
top.protocol("WM_DELETE_WINDOW", on_closing)

frame=tkinter.Frame(top)
scrollbar=tkinter.Scrollbar(frame)
message_box=tkinter.Listbox(frame, height=15, width=50)

scrollbar.configure(command=message_box.yview)
message_box.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_box.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
frame.pack()

input_text=tkinter.StringVar()
input_text.set("")

text_field=tkinter.Entry(top, textvariable=input_text)
text_field.bind("<Return>", send_message)
text_field.pack()

send_button=tkinter.Button(top, text="Send")
send_button.bind("<Button-1>", send_message)
send_button.pack()

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

recv_thread=threading.Thread(target=recv_message, args=(sock, ))
recv_thread.start()

tkinter.mainloop()
