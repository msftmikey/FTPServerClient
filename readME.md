#  FTP Server and Client: Socket Programming

by Joel Perez, Miguel Mancera, and Michael Duenas

This project consists of an FTP server and FTP client. The client should connect to the server and be able to upload and download files to/from the server. 

## Setting up the Connection 

Place the client and server in two separate directories. 

Open two seperate terminals. 

## Begin the Server Connection 
Before beginning the server.py file, make sure to use the "cd" command to be in the correct respective directory in both terminals. 

``` 
cd server
``` 
OR 

``` 
cd client
```
Start the server.py file from the terminal with whatever port you wish to listen on. 

```
python3 server.py 8000
```

## Begin the Client Connection

Start the client.py file from the terminal with the localhost IP address and the port you wish to listen on. 

``` 
python3 client.py 127.0.0.1 8000
```

# Running Commands 

On the client, run the indicated commands. 

```  
ftp>ls    (lists files on the server)
ftp>get <filename>  (downloads <filename> from the server)
ftp>put <filename>  (uploads <filename> from the client to the server)
ftp>quit  (disconnects)
```

##
