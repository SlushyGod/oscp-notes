Run basic nmap for the first 1000 ports
`nmap -sC -sV -oA nmap/[filename] [address]`

Run scan for all ports
`nmap -p- -oA nmap/[filename] [address]`

Nuiances:
-sC checks for anonymous login for FTP

Important flags:
-Pn is great for passive scans (need to learn more about this)
-sU is good for UDP scans it seems, yet to see it work
-O is good for OS detection
--min-rate [packets/sec]
-A aggresive scan

Scripts:
nmap -sV --script=http-php-version -> enumerate php version

--max-retries 1 to try and speed -p- scans
 - you can also use 0 to make it even faster