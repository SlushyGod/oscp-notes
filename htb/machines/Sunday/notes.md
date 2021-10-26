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

users that we got through rockyoutext
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

NOTES:
ALWAYS KEEP ENUMERATING, at least have something up and running
nmap get a list of what to enumerate after one scan finishes
Just keep swimming, try to use the most common password till you exhaust everything, also ctf names are good hints for the password