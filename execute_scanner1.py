# Program to run SonarQube, SonarScanner and ElasticSearch which will scan a repo and provide results.
import os
import sys
from sys import *
from threading import Thread
import os
import zipfile
import subprocess
import time
import urllib.request
import sys
import requests
import urllib
import datetime
import random
import requests
from subprocess import Popen
import platform

import datetime
import getopt
import sys
from time import gmtime, strftime
from P4 import P4, P4Exception  # Import the module
import getopt



# Get the current directory where the script is running
dir_path = os.path.dirname(os.path.realpath(__file__))



#os.chdir(p)
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

#path='c:\security_automation\SonarQube_Integration\sonar-scanner-3.3.0.1492'
filename=''
global p

def usage():
    print('\nUsage:')

    print('\ndefine_path.py -f <filepath of workspace>')
    print('\n\nCompulsory:')
    print('-------')
    print('\nemail is for report generation. Please enter path only')
    print('-f	filename of workspace')
    print('-e	email')



def main(argv):


    try:
        print("---------------------------------------------")
        print("Initiated perforce at " + "[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "]")
        print("---------------------------------------------")
        opts, args = getopt.getopt(argv, "hf:", ["filename="])
        if len(opts) == 0:
            usage()
            sys.exit(2)
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()                            #open help
            sys.exit()
        elif opt in ("-f"):
            global filename
            filename = arg

            print("input filename is :", filename)

        else:
            print("Please provide atleast one argument")
    global p
    p = filename
    # fp=open(path,'r+');
    print(p)
    os.chdir(p)
    print(os.chdir(p))

    time = datetime.datetime.now()
    print("Source code SCan Started at: " + str(time))

    from P4 import P4, P4Exception  # Import the module
    p4 = P4()  # Create the P4 instance
    p4.port = "1666"
    p4.user = "Administrator"
    # p4.client = "divya"            # Set some environment variables

    try:  # Catch exceptions with try/except
      p4.connect()  # Connect to the Perforce server
      print("connected")

      # print("give the client perforce working directory")
      #client_root = p
        # Run "p4 edit file.txt"
      

      p4.disconnect()  # Disconnect from the server
    except P4Exception:
      for e in p4.errors:  # Display errors
        print(e)

    template = "INACRA004"
    client_root = p
    p4 = P4()

    try:
      p4.connect()
      # Convert client spec into a Python dictionary
      client = p4.fetch_client("-t", template)
      client._root = client_root
      p4.save_client(client)
      info = p4.run("info")  # Run "p4 info" (returns a dict)
      for key in info[0]:  # and display all key-value pairs
        print(key, "=", info[0][key])
      p4.run("edit", "file.txt")

      p4.run("sync",p)               #sync

    except P4Exception:
      for e in p4.errors:  # Display errors
        print(e)

      print("initiate scan for source code analysis")






# ************************************************************************************
#sonarqube started
#url=path of project file



def downloadRepositoryWindows(url):


    # Fetching the argument from the command line, which contains the real name for the project file

    # Snippet to find the filename from the filepath

    mname=(os.path.basename(url))



    # Path of the properties file
    propertiesFilePath = dir_path + '\conf\sonar-scanner.properties'

    # For comparing purposes
    data1 = open(propertiesFilePath, 'r')

    # Reading the properties file
    with open(propertiesFilePath, 'r') as file:
        data = file.readlines()

    # Reading the properties File and deleting all the contents in them

    print("\nDeleting Old properties ................ \n")

    f = open(propertiesFilePath, 'r+')
    f.truncate(0)
    data = f.readlines()

    #  Appending the properties in the file one by one
    data.append("sonar.sourceEncoding=UTF-8")
    data.append("\n")
    data.append("\n")
    data.append("export SONAR_SCANNER_OPTS=-Xms512m\ -Xmx2048m")
    data.append("\n")
    data.append("\n")
    data.append("sonar.projectKey=" + mname)
    data.append("\n")
    data.append("\n")
    data.append("sonar.projectName=" + mname)
    data.append("\n")
    data.append("\n")
    data.append("sonar.projectVersion=1.0")
    data.append("\n")
    data.append("\n")
    data.append("sonar.scm.disabled=true")
    data.append("\n")
    data.append("\n")

    # data.append("sonar.nodejs.executable=/usr/local/n/versions/node/11.6.0")

    # converting to double slash to write to file
    doubleSlashPathWindows = dir_path.replace('\\', '\\\\')

    data.append("sonar.sources=" + doubleSlashPathWindows + "\\\\" + mname)
    data.append("\n")
    data.append("\n")
    data.append("sonar.java.binaries=" + doubleSlashPathWindows + "\\\\" + mname)
    data.append("\n")

    # and write everything back
    with open(propertiesFilePath, 'w') as file:
        file.writelines(data)

    # Running the command for scanning the files
    print("\n Running sonar-scanner.bat file. \n Scanning of " + mname + " repo started ................. \n")

    p = Popen(dir_path + "\\bin\sonar-scanner.bat")
    stdout, stderr = p.communicate()

    # Renaming the project name with current Date and Time
    #tempTime = datetime.datetime.now()
    #tempTime = tempTime.strftime("%Y-%m-%d--%H-%M")
    #os.rename(projectPathWindows + "\\" + mname, projectPathWindows + "\\" + mname + tempTime)


# ***********************************************************************************************************************

if __name__ == '__main__':
    '''
    # Fetching the argument from the command line
    if len(sys.argv) == 3:
        url = sys.argv[2]
    elif len(sys.argv) == 2:
    '''
    main(sys.argv[1:])
    print(sys.argv[2])
    url =sys.argv[2]
    url = url.strip()

time.sleep(8)
Thread(target=downloadRepositoryWindows, args=(url,)).start()


