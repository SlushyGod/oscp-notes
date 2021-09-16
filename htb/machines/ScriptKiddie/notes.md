22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
5000/tcp open  http    Werkzeug httpd 0.16.1 (Python 3.8.5)
|_http-title: k1d'5 h4ck3r t00l5
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Seems like it lets us execute basic commands with simple tools
searchsploit on Werkzeug shows a few vulns
- seems like the wont work

searchsploit -m "make a copy of the exploit in cwd"