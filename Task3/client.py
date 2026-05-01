import socket
import threading
import time

FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
name = input("Enter your name: ")

IPServer = input("please enter the IP: ") 
IPServer=str(IPServer)

PORT = int(input("please enter the port: "))

joiningMessage = "J@" + name
client.sendto(joiningMessage.encode(FORMAT), (IPServer, PORT))
print("connected to IP: ", IPServer," Port: ", PORT)
lock = threading.Lock()



def handle_connection(serverMessage):
    canNotAnswer = True

    type = serverMessage.split("@")[0]
    if type == "J":
        name = serverMessage.split("@")[1]
        currentClient = serverMessage.split("@")[2]
        print("\n")
        print(name, "joined the game.....\n" + "number of current client :", currentClient)


    elif type == "S":
        text = serverMessage.split("@")[1]
        timeToStart = serverMessage.split("@")[2]
        timeForAnswer = serverMessage.split("@")[3]
        print("\n")
        print(text + timeToStart + timeForAnswer)

    elif type == "Q":
        time.sleep(1)
        theQuestion = serverMessage.split("@")[1]
        print("\n")
        print(theQuestion)

        print("enter exit to end the game\nplease enter your answer:")
        result = input()
        exit=True
        if result == "exit":
            client.sendto("E@exit".encode(FORMAT), (IPServer, PORT))
            exit=False
        else:
            result = "A@" + str(result)
            client.sendto(result.encode(FORMAT), (IPServer, PORT))
        while canNotAnswer:
            if exit:

                print("enter exit to end the game\nplease enter your answer:")
                result = input()
            if result == "exit" and exit:
                client.sendto("E@exit".encode(FORMAT), (IPServer, PORT))
                exit=False
            elif result != "exit":
                result = "A@" + str(result)
                client.sendto(result.encode(FORMAT), (IPServer, PORT))

        lock.acquire()
        canNotAnswer = True
        lock.release()
    elif type == "T":
        theText = serverMessage.split("@")[1]
        print("\n")
        print(theText)

    elif type == "SA":
        lock.acquire()
        canNotAnswer = False
        lock.release()

        theAnswer = serverMessage.split("@")[1]
        print("\n")
        print(theAnswer)
        print("Time up!")

    elif type == "sh":
        theText = serverMessage.split("@")[1]
        print("\n")
        print(theText)
        client.close()

def client_run():
   try:
        while True:

            serverMessage = client.recvfrom(1024)[0].decode(FORMAT)
            type = serverMessage.split("@")[0]
            thread = threading.Thread(target=handle_connection, args=(serverMessage,))
            thread.start()
            if type == "E":
                print("\n")
                print("GAME OVER!")
                break

   except KeyboardInterrupt:
       print("\nKeyboardInterrupt detected. Exiting gracefully...")
   except OSError:
       print("OFF")
   except Exception as e:
       print(f"\nAn error occurred: {e}")
   finally:
       pass


if __name__ == "__main__":
    client_run()