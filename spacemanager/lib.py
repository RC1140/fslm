from models import *
import os
 
def getDriveOverMaxCapacity(disk):
    s = getSpace(disk.Path)
    cap = float(s['capacity'])
    used = float(s['used'])
    capacitySize = cap * (float(disk.MaxUsagePercentage) / float(100))
    over = used - capacitySize
    return formatSpace(over)


def getRawDriveOverMaxCapacity(disk):
    s = getSpace(disk.Path)
    cap = float(s['capacity'])
    used = float(s['used'])
    capacitySize = cap * (float(disk.MaxUsagePercentage) / float(100))
    over = used - capacitySize
    return over #in MB


def checkDriveOverMaxCapacity(disk):
    s = getSpace(disk.Path)
    cap = float(s['capacity'])
    used = float(s['used'])
    perc = (used / cap) * 100
    if perc > disk.MaxUsagePercentage:
        return True
    else:
        return False
        

def getSpace(disk):
    s = os.statvfs(disk)
    capacity = (s.f_frsize * s.f_blocks) / (1048576)
    available = (s.f_frsize * s.f_bavail) / (1048576)
    used = (s.f_frsize * (s.f_blocks - s.f_bavail) ) / (1048576)
    return  {'capacity': capacity, 'used': used, 'available': available} #returns megabytes
    
    

def formatSpace(kb):
    '''If Its more than 1024 change it to the next format'''
    format = "MB"
    if (abs(kb) > 1024):
        kb = kb / 1024
        format = "GB"
        if (abs(kb) > 1024):
            kb = kb / 1024
            format = "TB"
            if (abs(kb) > 1024):
                kb = kb / 1024
                format = "PB"
    kb = round(kb, 2)
    return kb.__str__() + format
    
    
def unFormatSpace(str):
    mb =0
    if str.endswith("MB"):
        print(str.replace("MB", ""))
        mb = float(str.replace("MB", ""))
    if str.endswith("GB"):
        print(str.replace("GB", ""))
        mb = float(str.replace("GB", ""))* 1024
    if str.endswith("TB"):
        mb = float(str.replace("TB", ""))* 1024 * 1024
        print(str.replace("TB", ""))
    return int(mb)
