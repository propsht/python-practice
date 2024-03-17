import csv
import secrets
import subprocess
from pathlib import Path

# run the script as administrator rights "sudo python3 create-user-accounts.py"

#Use cwd for “current working directory” and identify the path of the Python directory as a string
cwd = Path.cwd() / "files"

#Next, you use a with statement and an as keyword. The with statement helps with resource management, and the as keyword creates an alias for the resource you want to call. Consider the following code
with open(cwd / "users_in.csv", "r") as file_input, open(cwd / "users_out.csv", "w") as file_output:
    #use a DictReader object so that each row in the file is read into a dict() with the field names and values
    reader = csv.DictReader(file_input)
    writer = csv.DictWriter(file_output,fieldnames=reader.fieldnames)
    writer.writeheader()

    #loop for run through each record
    for user in reader:
        #use the secrets library that you imported at the beginning of the script to generate a random password of eight hex bytes
        user["password"] = secrets.token_hex(8)
        # run the /sbin/useradd command to create each user
        useradd_cmd = [
                       #for Linux use "/usr/sbin/useradd" and for Mac "/usr/bin/dscl"
                       #"/usr/bin/dscl",
                       #"-c", user["real_name"],
                       #"-m",
                       #"-G", "users",
                       #"-p", user["password"],
                       #user["username"]]

                        #for Mac "/usr/bin/dscl"
                        "/usr/bin/dscl",
                        ".",  # "." means the local directory domain
                        "-create", f"/Users/{user['username']}",
                        "UserShell", "/bin/bash",
                        "RealName", user["real_name"],
                        "UniqueID", "1001",  # Update with desired UID
                        "PrimaryGroupID", "80",  # Update with desired GID
                        "NFSHomeDirectory", f"/Users/{user['username']}",
                        "Password", user["password"]
        ]




        #The check=True parameter causes the script to exit with a CalledProcessError if the command fails for any reason
        subprocess.run(useradd_cmd, check=True)

        writer.writerow(user)
