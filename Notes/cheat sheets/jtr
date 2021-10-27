Ubuntu download:
`snap install john-the-ripper`

using something like zip2john to extract hash from zip file:
`john-the-ripper.zip2john`

You should pipe this into some sortve hash file, so append ` > zip.hashes` to it

Next you can go ahead and get to just brute force it by using the below command, show is just to show the password found

`john-the-ripper zip.hashes --show`


To crack /etc/shadow and /etc/passwd files you first need to prep them first
`unshadow passwd shadow > passcopy`

Auto detect, go ahead and start cracking
`john-the-ripper --wordlist=/home/slushygod/Documents/oscp-notes/tools/lists/rockyou.txt ./passcopy`

ToDo:
Should look more into how JTR extracts the "non-hash" and uses that for future use