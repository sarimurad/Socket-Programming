import socket
import threading
import time
import random

# UDP SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PORT = 5689
IP = socket.gethostbyname(socket.gethostname())
print(socket.gethostname())
print(IP)
server.bind((IP, PORT))
FORMAT = 'utf-8'

minNumberToStart = 2
numberOfQuestion = 3
CounterForQuestion = 0
timeForResponse = 30
timeBetweenQuestions = 20
timeBetweenRounds = 10
theRightAnswer = str()

activeClients = []
question = []
answerClient = []
correctClient = []
roundQuestions = []
nameOfClient = []


def readQuestion(questionInFile=0):
    file = open('question.txt', 'r')
    while True:
        Q = file.readline().strip()
        A = file.readline().strip()
        if not Q and not A:
            break

        questionInFile += 1
        question.append((Q, A))
    file.close()
    return questionInFile


def generateNumberOfQuestion(questionInFile):
    for i in range(numberOfQuestion):
        random_number = random.randint(0, questionInFile-1)
        roundQuestions.append([str(question[random_number][0]), str(question[random_number][1])])


def checkTheChanceAndUpdate(address):
    for client in nameOfClient:
        if address == client[1]:
            if client[5] == True:
                client[5] = False
                if client[1] not in answerClient:
                    answerClient.append(client[1])
                return True
            else:
                return False


def checkTheAnswerAndUpdate(address, answer):
    if answer == theRightAnswer:
       for client in nameOfClient:
          if address == client[1]:
            score = (len(activeClients)-len(correctClient))/len(activeClients)
            client[4] = score
            client[3] += score
            correctClient.append(address)


def printTheScore():
    global nameOfClient
    scoreMessageToClient = "T@SCORE:\n"
    for client in nameOfClient:
        scoreMessage = str(client[0])+" total "+str(client[3])+" this Question " + str(client[4])
        print(scoreMessage)
        scoreMessageToClient+=(str(scoreMessage)+"\n")

    for client in nameOfClient:
        server.sendto(scoreMessageToClient.encode(FORMAT), client[1])



def findWinderThisRoundAndPrintIt():
    if len(nameOfClient)>0:
        max=nameOfClient[0][3]
        playerInfo=nameOfClient[0]
        for client in nameOfClient:
            if client[3] > max:
                max=client[3]
                playerInfo=client

        playerInfo[2]+=1
        winnerMessage="the winner this round is: "+str(playerInfo[0])+" with total rounds :"+str(playerInfo[2])
        print(winnerMessage)
        clientWinnerMessage="T@"+winnerMessage
        for client in activeClients:
            server.sendto(clientWinnerMessage.encode(FORMAT), client)
        for client in nameOfClient:
            client[3] = 0

def clearTheScoreForEveryQuestion():
     for client in nameOfClient:
         client[4] = 0
     correctClient.clear()

def handle_client(message, address):
    clientMessage=message.decode(FORMAT)
    type=clientMessage.split("@")[0]


    if type=="J":
        data = clientMessage.split("@")[1]
        if address not in activeClients:
            for client in nameOfClient:
                joinMessage = "J@"+data+" with address: "+str(address)+"@" + str(len(activeClients))
                server.sendto(joinMessage.encode(FORMAT), client[1])
            nameOfClient.append([data, address, 0, 0.0, 0.0,True])
            activeClients.append(address)
            print("===>" + data + " joined the game" + ", with IP address and Port: " + str(address))

    elif type=="A":
        state=checkTheChanceAndUpdate(address)
        if state == True:
            theAnswer = clientMessage.split("@")[1]
            theAnswer = str(theAnswer).lower()
            whoAnswer=""
            for client in nameOfClient:
                if client[1] == address:
                    whoAnswer=client[0]
            if theAnswer == theRightAnswer:
               print(theAnswer, "who answer it", whoAnswer,address," Right answer" )
            else:
                print(theAnswer, "who answer it", whoAnswer,address, " Wrong answer")
            checkTheAnswerAndUpdate(address,theAnswer)

    elif type=="E":
          whoLeft ="T@left the game:"
          for client in nameOfClient:
             if address == client[1]:
                server.sendto("E@GAME OVER!".encode(FORMAT), client[1])
                whoLeft += client[0]
                nameOfClient.remove(client)
                activeClients.remove(address)
                if address in answerClient:
                  answerClient.remove(address)


          for client in nameOfClient:
              server.sendto(whoLeft.encode(FORMAT), client[1])

def removeNotActive():
    global activeClients
    global nameOfClient
    global answerClient
    activeClients = answerClient
    for i in range(len(nameOfClient)):
        for client in nameOfClient:

            if client[1] not in activeClients:
                nameOfClient.remove(client)
                print(client[0],"removed.......")
                server.sendto("E@GAME OVER!".encode(FORMAT), client[1])
    answerClient= []


def oneChance():
    for client in nameOfClient:
         client[5]=True


def server_run():
    print("server is running on IP and Port",IP,PORT)
    questionInFile = readQuestion()
    generateNumberOfQuestion(questionInFile)
    global numberOfQuestion
    global CounterForQuestion
    global minNumberToStart
    global timeBetweenRounds
    global timeBetweenQuestions
    global roundQuestions
    global theRightAnswer
    global activeClients
    global nameOfClient
    try:
        while True:

            try:
                server.settimeout(2)
                message, address = server.recvfrom(1024)

                thread = threading.Thread(target=handle_client, args=(message, address))
                thread.start()
                thread.join()

                while len(activeClients) >= minNumberToStart:


                    counterForQuestion = 0
                    for client in activeClients:
                        startingMeessage = "S@" + "the game start after: " + "@" + str(timeBetweenQuestions) + "  time for answer " + "@" + str(timeForResponse)
                        server.sendto(startingMeessage.encode(FORMAT), client)

                    while counterForQuestion < numberOfQuestion :

                        time.sleep(timeBetweenQuestions)
                        theQuestion = roundQuestions[counterForQuestion][0]
                        theRightAnswer = roundQuestions[counterForQuestion][1]
                        print(theRightAnswer)
                        sendNumber=counterForQuestion+1
                        questionMessage = "Q@"+str(sendNumber)+"- " + theQuestion
                        for client in activeClients:
                            server.sendto(questionMessage.encode(FORMAT), client)

                        oneChance()

                        timer=time.time()
                        server.settimeout(0.01)
                        while (time.time() - timer) < 0.5:
                            try:
                                message, address = server.recvfrom(1024)
                                theMessage = message.decode(FORMAT)
                                type = theMessage.split("@")[0]
                                if type == "A":
                                    print("duplicate removed")
                                else:
                                    if address not in activeClients:
                                        server.sendto(questionMessage.encode(FORMAT), address)
                                    thread = threading.Thread(target=handle_client, args=(message, address))
                                    thread.start()
                                    thread.join()
                            except socket.timeout:
                                pass


                        server.settimeout(1)
                        startTime = time.time()
                        while (time.time() - startTime) < timeForResponse:
                            try:
                                message, address = server.recvfrom(1024)
                                if address not in activeClients:
                                    server.sendto(questionMessage.encode(FORMAT), address)
                                thread = threading.Thread(target=handle_client, args=(message, address))
                                thread.start()
                                thread.join()


                            except socket.timeout:
                                print("waiting for answer..............")

                            except ConnectionResetError:
                                    print("closing connection.........")

                        for client in activeClients:
                            sendAnswer="SA@"+"right answer :"+theRightAnswer
                            server.sendto(sendAnswer.encode(FORMAT), client)

                        counterForQuestion += 1
                        printTheScore()
                        clearTheScoreForEveryQuestion()
                    removeNotActive()
                    findWinderThisRoundAndPrintIt()
                    for client in activeClients:
                        countDownMessage = "T@" + "Next round after: " + str(timeBetweenRounds)
                        server.sendto(countDownMessage.encode(FORMAT), client)
                    time.sleep(timeBetweenRounds)
                    roundQuestions = []
                    generateNumberOfQuestion(questionInFile)
                else:

                    tellClientToWait="waiting for clients to be more than "+ str(minNumberToStart)+"\n"+"active clients: "+str(len(activeClients))
                    print(tellClientToWait)
                    formatForSending="T@"+tellClientToWait
                    for client in activeClients:
                        server.sendto(formatForSending.encode(FORMAT), client)



            except socket.timeout:
                print("waiting for response")
                print("active clients: ", len(activeClients))
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Exiting gracefully...")
        for client in activeClients:
            byeMessage = "sh@" + "the server is shutting down..."
            server.sendto(byeMessage.encode(FORMAT), client)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        for client in activeClients:
            byeMessage = "T@" + "the server is shutting down..."
            server.sendto(byeMessage.encode(FORMAT), client)

    finally:
        pass

if __name__ == '__main__':
    server_run()
