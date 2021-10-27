First thing we see if port 79 which service is finger
quick google search pops up hacktricks to test it

finger users:
root
user

https://book.hacktricks.xyz/pentesting/pentesting-finger
http://pentestmonkey.net/tools/user-enumeration/finger-user-enum
`perl finger-user-enum.pl -U ~/Documents/oscp-notes/tools/lists/rockyou.txt -t 10.129.244.250`

we do get NFS Anonymous Access
need to look at how to mount an NFS share

mounting nfs didnt work, also nfs port isnt even open

looks like the OS is solaris

running the enumeration script from pentest monkey we get a user sammy

turns out I was using the finger tool wrong, I ended up using the tool on my local system
`finger user@host` is how it should be
the windows documention says to display all users then use the command
`finger @host` but that just said their were no logged in users

users that we got through rockyoutext, with pentest monkey script
sammy@10.129.244.250:
rock you@10.129.244.250:
sunny@10.129.244.250:
i love you@10.129.244.250:
te amo@10.129.244.250:

there are some blogs about rce through the finger command, but that didnt work
https://zarsec.co.uk/2018/07/29/command-injection-using-finger-service/

trying to ssh as sammy
`ssh -p 22022 sammy@10.129.244.250`
gives a key exchange error
`ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -p 22022 sammy@10.129.244.250`

That got it! `sunny:sunday`
Looking at stuff, checking out some things like the bash history and whatnot

id:`uid=65535(sunny) gid=1(other) groups=1(other)`

running sudo -l shows us that we can 
`(root) NOPASSWD: /root/troll`
executing that just prints 'testing'

SunOS sunday 5.11 snv_111b i86pc i386 i86pc Solaris

OpenSolaris 2009.06 snv_111b X86
Copyright 2009 Sun Microsystems, Inc.  All Rights Reserved.
Use is subject to license terms.
Assembled 07 May 2009

Get used to going ahead and trying to crack /etc/shadow files if you can read them

Look for local backups??
Also look at directories in `/`, maybe there are some wierd ones

In the /backup directory there were two wierd files
`agent22.backup`
`shadow.backup`

Prepping the files for cracking
`unshadow passwd shadow > passcopy`

Start cracking
`john-the-ripper --wordlist=/home/slushygod/Documents/oscp-notes/tools/lists/rockyou.txt ./passcopy`

gave us the password!
`sammy:cooldude!`

logging in as sammy, we run sudo -l
`(root) NOPASSWD: /usr/bin/wget`

Looking at the man pages and some pages into wget, this came up
https://unix.stackexchange.com/questions/107864/is-it-possible-to-execute-the-result-of-wget-as-a-command
which shows that we can execute a script using wget

tried to pop a reverse shell using sudo, didnt seem to get root, just ended up getting a reverse shell for sammy, so the script is executed with sammy bash

using id, looks like there is a group staff

get a random idea to try and overide the /etc/shadow file to change the root password
- sudo doesnt even have write permissions, so no luck, but good effort

remembering that sunny was able to execute something as sudo with nopassword
- i tried to replace /root/troll but didnt have any luck there

sooo....im dum, my script had /bin/bash...their bash was in /usr/bin/bash, I should prob use which bash, or just bash from now on. check to make sure it exists

i just dunno, maybe too tired, had to add add the `#!/bin/bash` to the beginning of the script

NOTES:
ALWAYS KEEP ENUMERATING, at least have something up and running
nmap get a list of what to enumerate after one scan finishes
Just keep swimming, try to use the most common password till you exhaust everything, also ctf names are good hints for the password