#!/bin/python3

import sys

# Finds information based on the slash notation 

# includes subnet mask, max amount of subnets, and max hosts
def getSubnetInfo(notation):
    fullOctet = int(notation/8)
    modOctet = notation % 8 
    maxSubnets = 2**modOctet
    i = 7
    octList=[]
# Finds remainder octet
    while modOctet-1>=0:
        bit = 2**i
        octList.append(bit)
        modOctet=modOctet-1
        i = i-1
    remainderOctet = (sum(octList))
    subnet= [] 
# Creates a list with the subnet mask (first octet in [0])
    for octs in range(fullOctet):
        subnet.append(255)
    subnet.append(remainderOctet)
    remainingBits = 32-notation
    maxHosts = 2**remainingBits
# If the there are less than 4 bytes in the list, add 0 and add to max hosts
    if len(subnet) != 4:
        for octets in range(4-len(subnet)):
            subnet.append(0)
    subnetInfo = {"subnetMask": subnet, "maxSubs": maxSubnets, "maxHost": maxHosts-2}
    return subnetInfo

def getRange(ipByte, subnetByte):
    i=7
    magicNumber = []
    byteList = []
    while ipByte > 0 or subnetByte > 0:
        subCheck = 2**i
        if ipByte >= subCheck:
            ipByte = ipByte-subCheck
            ipByteCheck = True
        else:
            ipByteCheck = False
        if subnetByte >= subCheck:
            subnetByte = subnetByte-subCheck
            magicNumber.append(subnetByte)
            subByteCheck = True
        else:
            subByteCheck = False
        if ipByteCheck and subByteCheck:
            byteList.append(2**i)
        i = i -1
        i=0
    rangeInfo = {
            "broadcast" : magicNumber[-2] + sum(byteList)-1,
            "netIDHost" : sum(byteList)
        }
        
    return rangeInfo

        

def getNetInfo(ipAddr, maxHosts, subnetMask):
    IP = ipAddr.split('.')
    i = 0
    while i < len(subnetMask):
        if subnetMask[i] < 255:
            targetByte = subnetMask[i]
            targetNode = i
            break
        i=i+1
    rangeInfo = getRange(int(IP[targetNode]),int(targetByte))
    netIDByte = rangeInfo["netIDHost"]
    broadcastByte = rangeInfo["broadcast"]
    broadcast = IP[:]
    netID = IP[:]
    if targetNode != 3:
        n=2
        netID[3] = 0
        broadcast[3] = 255
        while subnetMask[n] == 0:
            broadcast[n] = 255
            netID[n]=0
            n-=1
    gateway=netID[:]
    gateway[3]+=1
    firstIP = gateway[:]
    firstIP[3]+=1
    lastIP = broadcast[:]
    lastIP[3]-=1
    netInfoRaw = [netID, gateway, firstIP, lastIP, broadcast]
    netInfo = []
    for ip in netInfoRaw:
       ip[2] = str(ip[2]) 
       ip[3] = str(ip[3]) 
       ip = ('.').join(ip)
       netInfo.append(ip)
    return netInfo


def main():
   cidrIP = sys.argv[1]
   IP = cidrIP.split('/')[0]
   notation = int(cidrIP.split('/')[1])
   subnetInfo = getSubnetInfo(notation)
   rangeInfo = getNetInfo(IP, subnetInfo['maxHost'],subnetInfo['subnetMask'])
   for mask in range(len(subnetInfo['subnetMask'])):
        mask +=1
        subnetInfo['subnetMask'][mask-1] = str(subnetInfo['subnetMask'][mask-1])
   subnetMask = ('.').join(subnetInfo['subnetMask'])
   netID = rangeInfo[0]
   gateway = rangeInfo[1]
   firstIP = rangeInfo[2]
   lastIP = rangeInfo[3]
   broadcast = rangeInfo[4]
   print("%s \n\n"
        "Network ID:       %s\n"
        "Usable Addressed: %s - %s\n"
        "Gateway:          %s\n"
        "Broadcast:        %s"%(cidrIP,netID, firstIP, lastIP, gateway, broadcast))
        

if __name__ == '__main__':
    main()
