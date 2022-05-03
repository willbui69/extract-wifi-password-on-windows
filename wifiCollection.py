# Import subprocess module for using OS commands
import subprocess

# Import re module for using regular expressions
import re

# Run the command to access wifi passwords
wifiCommandAccess = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True)

# List the result as string
commandResult = wifiCommandAccess.stdout.decode()

# Use regular expression to find all wifi names
wifiNames = (re.findall("All User Profile     : (.*)\r", commandResult))

# Create an empty list to save wifi names and passwords
wifiList = []

# Check any available wifi
if len(wifiNames) != 0:
    for name in wifiNames:
        # Make a dictionary to save each wifi name as key and its value as password
        wifiProfile = {}
        # Run command to check security key is available or not
        profileInfo = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
        if re.search("Security key           : Absent", profileInfo):
            continue
        else:
            # If security key is available save wifi name as key in the dic
           wifiProfile["ssid"] = name
           # Run command to get password for that ssid
           profileInfoPass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
           password = re.search("Key Content            : (.*)\r", profileInfoPass)
           # Save password in the dic
           if password == None:
               wifiProfile["password"] = None
           else:
               wifiProfile["password"] = password[1]
        wifiList.append(wifiProfile)

# Print out all wifi names nad passwords
for i in range(len(wifiList)):
    print(wifiList[i])











