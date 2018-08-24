# -*- coding: utf-8 -*-


'''
VENDER ID : 공급업체
Product ID : 제품번호
'''

from winreg import *
import sys
import re
import requests
import os

#get HKLM_USB Info
def getHKLM_USB():
    usb_list = []
    varUSB_SubKey = 'SYSTEM\\CurrentControlSet\\Enum\\USB'
    varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    varKey = OpenKey(varReg, varUSB_SubKey)  # 레지스트리 핸들 객체 얻기

    try :
        for i in range(10000):
            reg = EnumKey(varKey, i)

            vid = re.search('^V[i?I?][D?d?]_([a-zA-Z0-9]+)&', reg)
            pid = re.search('P[i?I?][D?d?]_([a-zA-Z0-9]+)', reg)
            if vid :
                #print (vid.groups(0)[0], pid.groups(0)[0])
                usb_list.append([vid.groups(0)[0], pid.groups(0)[0]])

    except OSError:
        print ("EnumKey is end Registry Key is ", i)

    CloseKey(varReg)
    CloseKey(varKey)
    return usb_list

#url data to txt file
def setUSB_String(url) :
    response = requests.get(url)

    if not(os.path.isdir('.\\list')):
        os.mkdir(".\\list")
    fp = open(".\\list\\usbList.txt",'w', encoding='utf-8' )
    #fp = open('asd.txt', 'w', encoding='utf-8')
    fp.write(response.text)
    fp.close()

class USB:

    def __init__(self):
        self.val_List = []
        self.val_atList = []

    def setUSB_type(self, fileName):

        find_value = '^([0-9a-zA-Z]+)[\s]{2}(.+)$\n'
        find_value_at = '^\t([0-9a-zA-Z]+)[\s]{2}(.+)$\n'
        fp = open(fileName, 'r')
        count = 0

        while (True):

            text = fp.readline()
            val = re.findall(find_value, text)
            val_at = re.findall(find_value_at, text)

            if val != [] and val_at == []:
                count +=1
                self.val_List.append([count, val[0][0].upper(), val[0][1].upper()])

            elif val_at != []:
                self.val_atList.append([count, val_at[0][0].upper(), val_at[0][1].upper()])

            if text == '' or \
                    '# List of known device classes, subclasses and protocols' in text:
                break
        fp.close()

    def getUSB_Info(self):

        return self.val_List, self.val_atList

if __name__ == "__main__":

    '''
        USB ListDownload
    '''
    url = "http://www.linux-usb.org/usb.ids"
    setUSB_String(url)

    '''
        get Saved USB Info List
    '''

    fileName = '.\\list\\usbList.txt'
    usb = USB()
    usb.setUSB_type(fileName)
    vid, pid = usb.getUSB_Info()


    ''' 
        print my registry USB vid, pid info 
    '''
    usb_list = getHKLM_USB()

    for i in usb_list:
        print ()
        for id in vid:
            if i[0] in id[1]:
                print ("vid : %s"%(id[1]))
                print("Name : %s" % (id[2]))
                for pi in pid :
                    if id[0] == pi[0] and i[1] == pi[1]:
                        print ("\tpid : %s" %(pi[1]))
                        print ("\tName : %s" %(pi[2]))
