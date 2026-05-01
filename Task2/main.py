
from socket import *
import os

server_socket = socket(AF_INET, SOCK_STREAM)
mainport=5689
server_socket.bind(("0.0.0.0", mainport))
server_socket.listen(1)

print("server is listening")

while True:
    client_socket, addr = server_socket.accept()
    ip = addr[0]
    port = addr[1]

    request = client_socket.recv(1024).decode("utf-8")

    # request = request.decode('utf-8')

    print(request)




    type=request.split("\n")[0]
    req=type.split(" ")[1]


    # print(type)
    # print(req)



    if req== "/" or req=="/en" or req=="/index.html" or req=="/main_en.html":
          client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
          client_socket.send("Content-Type: text/html\r\n".encode("utf-8"))
          client_socket.send("\r\n".encode())
          htmlenfile=open("main_en.html","r",encoding="utf-8")
          client_socket.send(((htmlenfile.read()).encode("utf-8")))
    elif req=="/styles.css":
        client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
        client_socket.send("Content-Type: text/css\r\n".encode("utf-8"))
        client_socket.send("\r\n".encode())
        css = open("styles.css", "r", encoding="utf-8")
        client_socket.send(((css.read()).encode("utf-8")))





    elif req=="/images/mohmadzaidPfp.png":
        client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
        client_socket.send("Content-Type: image/png\r\n".encode("utf-8"))
        client_socket.send("\r\n".encode("utf-8"))
        mohmadzaidImage=open("images/mohmadzaidPfp.png","rb")
        client_socket.send((mohmadzaidImage.read()))
    elif req == "/images/mohmadOmarPfp.png":
        client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
        client_socket.send("Content-Type: image/png\r\n".encode("utf-8"))
        client_socket.send("\r\n".encode())
        mohmadomarImage = open("images/mohmadOmarPfp.png", "rb")
        client_socket.send((mohmadomarImage.read()))
    elif req == "/images/sariPfp.png":
        client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
        client_socket.send("Content-Type: image/png\r\n".encode("utf-8"))
        client_socket.send("\r\n".encode("utf-8"))
        sariImage = open("images/sariPfp.png", "rb")
        client_socket.send((sariImage.read()))
    elif req == "/images/sum1.jpg":
        client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
        client_socket.send("Content-Type: image/jpg\r\n".encode("utf-8"))
        client_socket.send("\r\n".encode("utf-8"))
        sumImage = open("images/sum1.jpg", "rb")
        client_socket.send((sumImage.read()))
    elif req == "/images/sum2.jpg":
        client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
        client_socket.send("Content-Type: image/jpg\r\n".encode("utf-8"))
        client_socket.send("\r\n".encode("utf-8"))
        sumImage = open("images/sum2.jpg", "rb")
        client_socket.send((sumImage.read()))


    elif req=="/supporting_material_en.html":
        client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
        client_socket.send("Content-Type: text/html\r\n".encode("utf-8"))
        client_socket.send("\r\n".encode("utf-8"))
        htmlenfile = open("supporting_material_en.html", "r", encoding="utf-8")
        client_socket.send(((htmlenfile.read()).encode("utf-8")))



    elif "/supporting_material_en.html?fileType=image&fileName=" in req:

        nameOFImage=req.split("=")[2]
        path=os.path.join(os.getcwd(),"images")
        found=False
        for filename in os.listdir(path):
            if filename == nameOFImage:
                client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
                client_socket.send("Content-Type: image/png\r\n".encode("utf-8"))
                client_socket.send("\r\n".encode("utf-8"))
                found=True
                toOpen="images/"+filename
                theImage = open(toOpen, "rb")
                client_socket.send((theImage.read()))
                print("==================================File  found================================")
                break

        if not found:
            search_url = f"https://www.google.com/search?q={nameOFImage.replace(' ', '+')}&tbm=isch"
            response = (
                "HTTP/1.1 307 Temporary Redirect\r\n"
                "Location:"+ search_url + "\r\n"
                "Content-Length: 0\r\n"
                "Connection: close\r\n"
                "\r\n"
            )


            client_socket.sendall(response.encode('utf-8'))

            print("==================================File not found================================")


    elif "/supporting_material_en.html?fileType=video&fileName=" in req:

        nameOFVideo = req.split("=")[2]
        path = os.path.join(os.getcwd(), "videos")
        found = False
        for filename in os.listdir(path):
            if filename == nameOFVideo:
                client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
                client_socket.send("Content-Type: video/mp4\r\n".encode("utf-8"))
                client_socket.send("\r\n".encode("utf-8"))
                found = True
                toOpen = "videos/" + filename
                theVideo = open(toOpen, "rb")
                client_socket.send((theVideo.read()))
                print("==================================File  found================================")
                break

        if not found:
            search_url = f"https://www.youtube.com/search?q={nameOFVideo.replace(' ', '+')}&tbm=isch"
            response = (
                    "HTTP/1.1 307 Temporary Redirect\r\n"
                    "Location:" + search_url + "\r\n"
                    "Content-Length: 0\r\n"
                    "Connection: close\r\n"
                  "\r\n"
            )

            client_socket.sendall(response.encode('utf-8'))

            print("==================================File not found================================")


    elif req=="/ar" or req=="/main_ar.html":
        client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
        client_socket.send("Content-Type: text/html\r\n".encode("utf-8"))
        client_socket.send("\r\n".encode("utf-8"))
        htmlenfile = open("main_ar.html", "r", encoding="utf-8")
        client_socket.send(((htmlenfile.read()).encode("utf-8")))

    elif req=="/stylesarab.css":
        client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
        client_socket.send("Content-Type: text/css\r\n".encode("utf-8"))
        client_socket.send("\r\n".encode("utf-8"))
        css = open("stylesarab.css", "r", encoding="utf-8")
        client_socket.send(((css.read()).encode("utf-8")))


    elif req == "/supporting_material_ar.html":
        client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
        client_socket.send("Content-Type: text/html\r\n".encode("utf-8"))
        client_socket.send("\r\n".encode("utf-8"))
        htmlenfile = open("supporting_material_ar.html", "r", encoding="utf-8")
        client_socket.send(((htmlenfile.read()).encode("utf-8")))



    elif "/supporting_material_ar.html?fileType=image&fileName=" in req:

        nameOFImage = req.split("=")[2]
        path = os.path.join(os.getcwd(), "images")
        found = False
        for filename in os.listdir(path):
            if filename == nameOFImage:
                client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
                client_socket.send("Content-Type: image/png\r\n".encode("utf-8"))
                client_socket.send("\r\n".encode("utf-8"))
                found = True
                toOpen = "images/" + filename
                theImage = open(toOpen, "rb")
                client_socket.send((theImage.read()))
                print("==================================File  found================================")
                break

        if not found:
            search_url = f"https://www.google.com/search?q={nameOFImage.replace(' ', '+')}&tbm=isch"
            response = (
                    "HTTP/1.1 307 Temporary Redirect\r\n"
                    "Location:" + search_url + "\r\n"
                    "Content-Length: 0\r\n"
                    "Connection: close\r\n"
                    "\r\n"
            )

            client_socket.sendall(response.encode('utf-8'))

            print("==================================File not found================================")


    elif "/supporting_material_ar.html?fileType=video&fileName=" in req:

        nameOFVideo = req.split("=")[2]
        path = os.path.join(os.getcwd(), "videos")
        found = False
        for filename in os.listdir(path):
            if filename == nameOFVideo:
                client_socket.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
                client_socket.send("Content-Type: video/mp4\r\n".encode("utf-8"))
                client_socket.send("\r\n".encode("utf-8"))
                found = True
                toOpen = "videos/" + filename
                theVideo = open(toOpen, "rb")
                client_socket.send((theVideo.read()))
                print("==================================File  found================================")
                break

        if not found:
            search_url = f"https://www.youtube.com/search?q={nameOFVideo.replace(' ', '+')}&tbm=isch"
            response = (
                    "HTTP/1.1 307 Temporary Redirect\r\n"
                    "Location:" + search_url + "\r\n"
                                               "Content-Length: 0\r\n"
                                               "Connection: close\r\n"
                                               "\r\n"
            )

            client_socket.sendall(response.encode('utf-8'))

            print("==================================File not found================================")







    else:

        client_socket.send("HTTP/1.1 404 Not Found\r\n".encode("utf-8"))
        client_socket.send("Content-Type: text/html\r\n".encode("utf-8"))
        client_socket.send("\r\n".encode("utf-8"))
        htmlenfile = open("Error.html", "r", encoding="utf-8")
        client_socket.send(((htmlenfile.read()).encode("utf-8")))
        Message=str("IP and address :")+str(ip)+" "+str(port)
        client_socket.send(Message.encode("utf-8"))
        print("IP address",ip)
        print("Port",port)

