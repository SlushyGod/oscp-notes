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