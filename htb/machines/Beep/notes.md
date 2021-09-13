we ran searchsploit on apache 2.2, didnt seem to find much
went to the website and saw "PRTG Network Monitor (NETMON)" and searched that and got an auth RCE vuln, which looks pretty interesting
- tried default creds like admin:admin, admin:password

- went ahead and started some gobuster commands, but they kept getting redirected with code 302
the basic stuff doesnt work, so time to take a look at other services

seems like there is something interesting on port 10000, going there, we are told to go into ssl mode, so https://
looks like we got an old protocol error, just a simple google search takes us here -> https://askubuntu.com/questions/1250787/when-i-try-to-curl-a-website-i-get-ssl-error
so we add the cnf file then run 
`OPENSSL_CONF=allow_tls1.conf curl --insecure -v https://10.129.1.226:10000`

Getting the html for the, what looks to be, login portal, we see that it is webmin
quick searchsploit shows a LOT of red

Tried to login with this command
OPENSSL_CONF=allow_tls1.conf curl --insecure -d "user=admin&pass=password" -X POST https://10.129.1.226:10000/session_login.cgi --cookie "testing=1; path=/;"