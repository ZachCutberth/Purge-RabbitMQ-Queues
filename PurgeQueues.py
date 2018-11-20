# Purge RabbitMQ day2day queues
# By Zach Cutberth

from subprocess import Popen
from glob import glob
import winreg
from pyrabbit.api import Client
import config

# Open the key and return the handle object.
rabbitMQServerHKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                          "Software\\Wow6432Node\\VMware, Inc.\\RabbitMQ Server")
                          
# Read the value.                      
rabbitMQServerInstallDir = winreg.QueryValueEx(rabbitMQServerHKey, "Install_Dir")
winreg.CloseKey(rabbitMQServerHKey)

# Path to rabbitmqctl
sbinDir = glob(rabbitMQServerInstallDir[0] + '\\rabbitmq_server*' + '\\sbin\\')

# RabbitMQ connection
cl = Client('localhost:15672', username, password, timeout=100)

# Get queue names
queues = [q['name'] for q in cl.get_queues()]

# Find queues with 'day2day' in the name, if they have messages then purge them.
for queue in queues:
    if 'day2day' in queue:
        if cl.get_queue_depth('/', queue) != 0:
            Popen('rabbitmqctl purge_queue ' + queue, cwd=sbinDir[0], shell=True).communicate()
