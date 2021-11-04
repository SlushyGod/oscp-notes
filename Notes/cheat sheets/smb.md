Some guides that are useful:


SMB can have anonymous access
smbclient -L [ip address] lists the shares if you have a connection

After listing out shares, check to see if you can connect to any of them
`smbclient //[ip address]/[share]`


Nmap has a few scripts for enumeration:
nmap --script smb-enum-shares -p 139,445 [ip address]

Also has script to check for vulnerabilities
nmap --script smb-vuln* -p 139,445 [ip]


Really good to try and list out the SMB

https://0xdf.gitlab.io/2018/12/02/pwk-notes-smb-enumeration-checklist-update1.html

- nmblookup, can be installed with sudo apt install samba-common-bin
- smbmap
- need to checkout enum4linux