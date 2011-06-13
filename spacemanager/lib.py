from models import *
import os
import logging
 
def getDriveOverMaxCapacity(disk):
    s = getSpace(disk.Path)
    cap = float(s['capacity'])
    used = float(s['used'])
    capacitySize = cap * (float(disk.MaxUsagePercentage) / float(100))
    over = used - capacitySize
    return formatSpace(over)

def initSettings():
    if Setting.objects.all().count() == 0:
        ih = Setting(SettingKey='IgnoreHidden',  Value='True',  Type='bool')
        ih.save()
        fl = Setting(SettingKey='ForceLogin',  Value='True',  Type='bool')
        fl.save()
        nomc = Setting(SettingKey='NotifyOverMaxCapacity',  Value='False',  Type='bool')
        nomc.save()


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
    
    
def getSetting(key=''):
    if Setting.objects.filter(SettingKey = key).count() != 0:
        return Setting.objects.filter(SettingKey = key)[0].Value
    return ''

def calcSize(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)  #returns MB
    
def calcGBSize(start_path):
    return calcSize(start_path)/1024

    

def getFirstAvailableDumpFolder(excludeFolder='',  monitorFolder=''):
    '''Should return a folder where files can be moved to 
        if none is found then a '' is returned and nothing should be
        moved , it might also be good to indicate this somewhere in the
        system.'''
    '''Get monitor folder type'''
    monitorMediaType = monitorFolder.MediaType
    if Drive.objects.filter(DriveType='D').count() == 0:
        logInfo('GFADF: No Dump Folders found')
        return {'path':'', 'drive':''}

    drives = Drive.objects.filter(DriveType='D').order_by('DumpPreference')

    if drives.count() > 0:
        logInfo('GFADF: '+ drives.count().__str__() + ' dump drives found')
        for d in drives:
            dumpFolders = d.folder_set.filter(MediaType=monitorMediaType).order_by('Path')
            logInfo('GFADF:DFF: '+dumpFolders.count().__str__() + 'Dump Folders found for ' + d.Name )
            s = getRawDriveOverMaxCapacity(d)
            if s < -1:
                logInfo('GFADF:OC: First Available Dump Drive: '+ d.Name +' Over Capacity:'+ s.__str__())
                #there is free space on this drive under the max capacity  and at least 1 gigabyte is free
                for dumpFolder in dumpFolders:
                    logInfo('First Available Dump Folder found: '+ dumpFolder.Path)
                    return {'path':dumpFolder.Path, 'drive':d}
            else: 
                logInfo('GFADF:OC: Dump Drive: '+ d.Name +' Over Capacity:'+ s.__str__()  + ' but still not less than -1?')
    logInfo('First Available Dump Folder not found')
    return {'path':'', 'drive':''}

def getSpaceToFree(monitorDrive, dumpDrive):
    excess = getDriveOverMaxCapacity(monitorDrive)
    vacuum = getDriveOverMaxCapacity(dumpDrive)
    if (vacuum > 0):
        return 0
    if (excess > vacuum):
        return excess
    else:
        return vacuum
        
def logInfo(message):
#    logger = logging.getLogger(__name__)
#    hdlr = logging.FileHandler(LOG_FILE+ '/info.log')
#    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#    hdlr.setFormatter(formatter)
#    logger.addHandler(hdlr)
#    logger.setLevel(logging.INFO)
#    logger.info(message)
    return;
