import os

f = open("shell.sh", "w")
f.write("#!/bin/bash\n/bin/sh")
f.close

os.chmod('shell.sh', 0o4777)