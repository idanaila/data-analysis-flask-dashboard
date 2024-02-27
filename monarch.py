import psutil
import os
import time
import logging
from logging.handlers import RotatingFileHandler
import subprocess


# create the log's directory
path = '/var/log/monarch'
if not os.path.exists(path):
    os.makedirs(path)


class SystemUsage:
    """collect system resources"""

    # get the number of system processes
    def count_system_processes(self, cmd):
        self.cmd = cmd

        list_processes = []                     # initiate empty list

        for proc in cmd:        
         list_processes.append(proc)            # loop through and append to the list
        process_count = 0       
        for self.elem in list_processes:        
         process_count += 1                     # count the system processes

        return process_count                    # return the number or running processes


    def psutil_system_usage(self, *cmd):        # get the psutil commands as list
        self.cmd = cmd
       
        with open('/var/log/monarch/system_usage.csv', 'a', newline='') as file:
            file.write(str(','.join(cmd)))      # write the entries to the file separated by ,
            file.write("\n")                    # new line
        file.close()                            # close file


    # rotate the logs - 20MB and 5 backups
    
    logFile='/var/log/monarch/system_usage.csv'
    handler = RotatingFileHandler(logFile, mode='a', maxBytes=20971520, backupCount=10)
    handler.terminator = ''
    handler.setLevel(logging.INFO)
    hrv = logging.getLogger('monarch')
    hrv.setLevel(logging.INFO)
    hrv.addHandler(handler)


class SystemDetails:

    # initiate the file with header
    with open('/var/log/monarch/system_details.csv', 'w', newline='') as file1:
        file1.write(str("######## System details ########\n") + "\n")
    file1.close()

    def system_details(self, description, cmd):
        self.description = description 
        self.cmd = cmd
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]
        with open('/var/log/monarch/system_details.csv', 'a', newline='') as file1:
           file1.write(str(description + output))
        file1.close()

sd = SystemDetails()
su = SystemUsage()

def main():

    # System details
    sd.system_details("Hostname: ", "hostname")
    sd.system_details("Dist: ", "cat /etc/os-release | grep -i pretty_name | awk -F= '{print $2}'")
    sd.system_details("CPU Model:", "cat /proc/cpuinfo | grep 'model name' | awk -F: '{print $2}'| tail -1")
    sd.system_details("CPU Cores:", "cat /proc/cpuinfo | grep 'cpu cores' | awk -F: '{print $2}'|wc -l")
    sd.system_details("Kernel: ", "uname -a | awk '{print $3}'")
    sd.system_details("Memory: ", "free -mh | awk '{print $2}' | head -n +2 | tail -1")
    
    while True:

        # System usage
        su.count_system_processes(psutil.pids())
        su.psutil_system_usage(time.strftime("%d"), time.strftime("%m"), time.strftime("%Y"), time.strftime("%H"), 
                        time.strftime("%M"), time.strftime("%S"), str(int(psutil.cpu_percent(interval=0.1))), 
                        str(int(psutil.cpu_freq().current)), str(int(psutil.virtual_memory().total)),
                        str(int(psutil.virtual_memory().available)), str(int(psutil.virtual_memory().percent)),
                        str(int(psutil.swap_memory().percent)), str(int(psutil.disk_io_counters().read_count)),
                        str(int(psutil.disk_io_counters().write_count)), str(int(psutil.disk_io_counters().read_bytes)),
                        str(int(psutil.disk_io_counters().write_bytes)), str(int(psutil.disk_usage('/').percent)),
                        str(int(psutil.net_io_counters().packets_recv)), str(int(psutil.net_io_counters().packets_sent)),
                        str(int(su.count_system_processes(psutil.pids()))), str(int(psutil.boot_time())))
        su.hrv.info('')         # rotate the logs
        time.sleep(2)        

    

if __name__ == '__main__':
    main()

