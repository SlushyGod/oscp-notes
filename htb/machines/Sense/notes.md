pfsense console
running php
just taking a look at the login screen there is a parameter for __csrf_magic

just on a guess took a look at changelog.txt looking for the version number and we see
https://10.129.222.161/changelog.txt
# Security Changelog 

### Issue
There was a failure in updating the firewall. Manual patching is therefore required

### Mitigated
2 of 3 vulnerabilities have been patched.

### Timeline
The remaining patches will be installed during the next maintenance window

- So we know there is an unpatched vulnerability
- So we should probably look for a vulnerability in 3? test this -> php/webapps/47413.py

xmlrpc.php has something interesting
index.html has dragonflyBSD installation??

Tried default creds, didnt work (prob should tried this at the beginning) -> didnt work tho

printed out the exploit for 47413 and used curl to see if maybe the script was messing up
We know we dont need to be authed, cause its retuning Xml about invalid strings
So I sent `curl --data-urlencode @xmlrpc https://10.129.222.161/xmlrpc.php --insecure`
--data-urlencode -> obvious, it encodes our data as url
@xmlrpc -> put the xml in a file called xmlrpc, just got that
--inscure -> ignore ssl errors

If SSL is being used, view the cert that is being used to see if you can learn anything

burpsuite has a right click option to copy as a curl command

sometimes creds that say "company defaults, password here, extra password, yadadada" if it doesnt work then try default password. Needless to say this is more CTFy, but you have a username to go with brute forcing the password (why yould you change the username and not the password? if anything its the opposite)

eventually gobuster gets us an interesting file:
/system-users.txt
####Support ticket###

Please create the following user


username: Rohit
password: company defaults

Also the username was not capitalized
company defaults? trying basic paswords like password, admin, root, tried pfsense default password which worked

So you can login through rohit:pfsense

we get that the pfsense version is v2.1.3
which we could try php/webapps/43560.py
- had already looked into using this but it didnt credentials

- this exploit gives us instant root on the machine, so that was pretty easy