import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("You MUST have a python version of at least 3.6!")
    quit(1)
from config import *
from set_variables import *
from shutil import copy
import subprocess
import glob
import subprocess
import os
import sqlite3

if not os.path.exists('filters.db'):
     db= sqlite3.connect("filters.db")
     cursor=db.cursor()
     cursor.execute('''CREATE TABLE FILTER(chat_id INTEGER,filter TEXT, reply TEXT)''')
     cursor.execute('''CREATE TABLE NOTES(chat_id INTEGER,note TEXT, reply TEXT)''')
     db.commit()
     db.close()
if not os.path.exists('pmpermit.db'):
     db= sqlite3.connect("pmpermit.db")
     cursor=db.cursor()
     cursor.execute('''CREATE TABLE APPROVED(chat_id INTEGER)''')
     db.commit()
     db.close()
if not os.path.exists("spam_mute.db"):
     db= sqlite3.connect("spam_mute.db")
     cursor=db.cursor()
     cursor.execute('''CREATE TABLE SPAM(chat_id INTEGER,sender INTEGER)''')
     cursor.execute('''CREATE TABLE MUTE(chat_id INTEGER,sender INTEGER)''')
     db.commit()
     db.close()
path=os.getcwd()
os.chdir("modules")
files=[]
for file in glob.glob("*"):
    files.append(file)
for file in files:
     with open(file,'r') as fd:
            os.chdir(path)
            copy('template_start.py','test.py')
            with open('test.py','a') as w:
                string=fd.readlines()
                w.writelines(string)
                subprocess.run('python3 test.py',shell=True)
                os.chdir("modules")
for i in files:
    print("INFO: Successfully Loaded: "+ i)
print("\n\nStarting Bot......")
os.chdir(path)
copy('template_start.py','runner.py')
with open('runner.py','a') as run:
    run.writelines(["print('Bot is running!')\n"])
    if CONSOLE_LOGGER_VERBOSE:
         run.writelines(["import logging\nlogging.basicConfig(level=logging.DEBUG)\n"])
    for file in files:
        os.chdir(path)
        os.chdir('modules')
        with open(file,'r') as fd:
                os.chdir(path)
                string=fd.readlines()
                run.writelines(string)
                os.chdir("modules")
os.chdir(path)
with open('runner.py','a') as run:
    run.writelines(["\nbot.run_until_disconnected()"])
process=subprocess.run('python3 runner.py',shell=True)
