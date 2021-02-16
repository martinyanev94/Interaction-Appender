#!/usr/bin/python
import datetime, sys, os, re
from datetime import timedelta

fecha=datetime.datetime.now()


os.system ("clear")
print "-------------------------------------------------------\n"
print "-------- XML Interactions Appending Tool v 0.1 --------\n"
print "------------by Adam Mounter and Martin Yanev-----------\n"
print "-------------------------------------------------------\n"
print "________________________________________________________________________________________________________________________________\n"


file_input = raw_input ("Please insert your XML's file path (starting from the root, e.g. /nats/current_build_slot/File_Name.xml) >> ")
if ".xml" not in file_input:
	print "This is not an XML file!"
	sys.exit(0)

try:
    HeaderType = input("Which type of Interaction would you like: Type '1' for What-Else message, Type '2' for What-If message, Type '3' for Tactical Conflict Detection >> ", )
    print "############################"
except:
    print "ERROR: Number of copies should be an integer."
    sys.exit(0)

try:
         open(file_input, 'r')
except:
        print "Incorrect path!"
	sys.exit(0)


try:
	requiredNoOfInts = input("How many Interactions would you like? >> ", )
	print "############################"
except:
	print "ERROR: Number of copies should be an integer."
	sys.exit(0)


What_If_Header=(
'<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
'<tns:whatIfMessage xmlns:fb="http://www.fixm.aero/base/3.0" xmlns:ff="http://www.fixm.aero/foundation/3.0" xmlns:fx="http://www.fixm.aero/flight/3.0" xmlns:tns="http://nats.aero/gdm/Separation/TacticalSeparationManagementService/V1.0/TacticalConflictDetection" xmlns:tsms="http://nats.aero/gdm/Separation/TacticalSeparationManagementService/V1.0/Common" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
'    <tns:eventMessage>\n'
'        <tns:metadata>\n'
'            <md:UUID xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">55432a2a-2eea-01e9-8fc1-f78bc9450edb</md:UUID>\n'
'            <md:timestamp xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">2019-02-12T10:00:00.000000Z</md:timestamp>\n'
'            <md:event xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">Publication</md:event>\n'
'            <md:serviceInstance xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">FSTBD: Pending SOM  </md:serviceInstance>\n'
'        </tns:metadata>\n'
'        <tns:whatIf>')

whatIfFooter=(
'        </tns:whatIf>\n'
'    </tns:eventMessage>\n'
'</tns:whatIfMessage>')

What_Else_Header=(
'<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
'<tns:whatElseMessage xmlns:fb="http://www.fixm.aero/base/3.0" xmlns:ff="http://www.fixm.aero/foundation/3.0" xmlns:fx="http://www.fixm.aero/flight/3.0" xmlns:tns="http://nats.aero/gdm/Separation/TacticalSeparationManagementService/V1.0/WhatElse" xmlns:tsms="http://nats.aero/gdm/Separation/TacticalSeparationManagementService/V1.0/Common" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
'    <tns:eventMessage>\n'
'        <tns:metadata>\n'
'            <md:UUID xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">784c3fdc-506b-01e9-ac84-b93d54e2bc6f</md:UUID>\n'
'            <md:timestamp xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">2019-02-12T10:00:00.000000Z</md:timestamp>\n'
'            <md:event xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">Publication</md:event>\n'
'            <md:serviceInstance xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">FSTBD: Pending SOM  </md:serviceInstance>\n'
'        </tns:metadata>\n'
'        <tns:whatElse>')

whatElseFooter = (      
'        </tns:whatElse>\n'
'    </tns:eventMessage>\n'
'</tns:whatElseMessage>')

Tactical_Header =(
'<?xml version="1.0" encoding="UTF-8" standalone="no" ?> \n'
'<tns:tacticalConflictDetectionMessage xmlns:fb="http://www.fixm.aero/base/3.0" xmlns:ff="http://www.fixm.aero/foundation/3.0" xmlns:fx="http://www.fixm.aero/flight/3.0" xmlns:tns="http://nats.aero/gdm/Separation/TacticalSeparationManagementService/V1.0/TacticalConflictDetection" xmlns:tsms="http://nats.aero/gdm/Separation/TacticalSeparationManagementService/V1.0/Common" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \n'
'     <tns:eventMessage>\n'
'        <tns:metadata>\n'
'            <md:UUID xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">55432a2a-2eea-01e9-8fc1-f78bc9450edb</md:UUID>\n'
'            <md:timestamp xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">2019-02-12T10:00:00.000000Z</md:timestamp>\n'
'            <md:event xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">Publication</md:event>\n'
'            <md:serviceInstance xmlns:md="http://nats.aero/gdm/Common/Metadata/V1.0">FSTBD: Pending SOM  </md:serviceInstance>\n'
'        </tns:metadata>\n'
'        <tns:tacticalConflictDetection>')

tacticalFooter = (
'        </tns:tacticalConflictDetection>\n'
'    </tns:eventMessage>\n'
'</tns:tacticalConflictDetectionMessage>')



if HeaderType == 1:
    HeaderString = What_Else_Header
    Footer = whatElseFooter
elif HeaderType == 2:
    HeaderString = What_If_Header
    Footer = whatIfFooter
else:
    HeaderString = Tactical_Header
    Footer = tacticalFooter



generatedInts = 0
gufi = 9000
track_id = 1

#What if and Tactical message params
TopOfSepAxis = 14.8
NoOfVertInts = 25
separationDistance = 0.1 
separationIncrement = (TopOfSepAxis / NoOfVertInts)

#What Else message params
FL=3000
trajDistance = 1
FLIncrement= 1000
trajDistanceIncrement= 1
topOfFL=60000


dt=datetime.datetime.now()+datetime.timedelta(hours = 2)
dateTimeIncrement = 36



lineNumber = 1

if HeaderType == 1:
    gufi = 8999
    with open (file_input, 'r') as myXML:
        f = myXML.readlines()
        with open("tactical_ints_"+str(requiredNoOfInts)+"_interactions.xml", "a") as v:
            v.write(HeaderString+"\n")
        while generatedInts < requiredNoOfInts:
            with open("tactical_ints_"+str(requiredNoOfInts)+"_interactions.xml", "a") as v:
                for line in f:
                    if '<tsms:flight codeSpace="urn:uuid">00000000-0000-4000-A000-000000008999</tsms:flight>' in line: #FIX FPID SUBJECT and SPACE
                        v.write(32*' '+str('<tsms:flight codeSpace="urn:uuid">00000000-0000-4000-A000-00000000'+str(gufi).zfill(4)+"</tsms:flight>"+"\n")) 
                        gufi -=1
                    elif "thisFlightDistanceDownTheTrajectory" in line:
                        v.write(str(16*' '+'<tsms:thisFlightDistanceDownTheTrajectory uom="NAUTICAL_MILES">'+str(trajDistance)+".00000E+01"+"</tsms:thisFlightDistanceDownTheTrajectory>"+"\n"))
                    elif "otherFlightDistanceDownTheTrajectory" in line:
                        v.write(str(16*' '+'<tsms:otherFlightDistanceDownTheTrajectory uom="NAUTICAL_MILES">'+str(trajDistance)+".00000E+01"+"</tsms:otherFlightDistanceDownTheTrajectory>"+"\n"))
                    elif "interactionFlightLevel" in line:
                        v.write(str(16*' '+'<tsms:interactionFlightLevel ref="FLIGHT_LEVEL" uom="FEET" xsi:type="tsms:FlightLevelType">'+str(FL).zfill(5)+"</tsms:interactionFlightLevel>"+"\n"))
                    elif "lowerBound" in line:
                        v.write(str(20*' '+'<tsms:lowerBound ref="FLIGHT_LEVEL" uom="FEET" xsi:type="tsms:AltitudeInFeetType">'+str(FL).zfill(5)+"</tsms:lowerBound>"+"\n"))
                    elif "upperBound" in line:
                        v.write(str(20*' '+'<tsms:upperBound ref="FLIGHT_LEVEL" uom="FEET" xsi:type="tsms:AltitudeInFeetType">'+str(FL).zfill(5)+"</tsms:upperBound>"+"\n"))
                    elif "otherFlightLevel" in line:
                        v.write(str(16*' '+'<tsms:otherFlightLevel ref="FLIGHT_LEVEL" uom="FEET" xsi:type="tsms:FlightLevelType">'+str(FL).zfill(5)+"</tsms:otherFlightLevel>"+"\n"))
                    else:
                        v.write(str(line))
            generatedInts +=1
            FL += FLIncrement
            if FL > topOfFL:
                FL = 3000
                trajDistance += trajDistanceIncrement    
        with open("tactical_ints_"+str(requiredNoOfInts)+"_interactions.xml", "a") as v:
            v.write(Footer+"\n")
    print "Created 'tactical_ints.xml' with %d interactions" % generatedInts
else:
    with open (file_input, 'r') as myXML:
        f = myXML.readlines()
        with open("tactical_ints_"+str(requiredNoOfInts)+"_interactions.xml", "a") as v:
            v.write(HeaderString+"\n")
        while generatedInts < requiredNoOfInts:
            with open("tactical_ints_"+str(requiredNoOfInts)+"_interactions.xml", "a") as v:
                for line in f:
                    if "tsms:flight" in line:
                        v.write(32*' '+str('<tsms:flight codeSpace="urn:uuid">00000000-0000-4000-A000-00000000'+str(gufi).zfill(4)+"</tsms:flight>"+"\n")) 
                        gufi -=1
                    elif "tsms:trackNumber" in line:
                        v.write(str(36*' '+"<tsms:trackNumber>"+str(track_id)+"</tsms:trackNumber>"+"\n"))
                        track_id +=1
                    elif "tsms:startTime"in line:
                        v.write(str(16*' '+'<tsms:startTime>'+str(dt.year)+"-"+str(dt.month).zfill(2)+"-"+str(dt.day).zfill(2)+"T"+str(dt.hour).zfill(2)+":"+str(dt.minute).zfill(2)+":"+str(dt.second).zfill(2)+"."+"000000"+"Z</tsms:startTime>"+"\n"))
                    elif "tsms:minimumSeparationDistance" in line:
                        v.write(str(16*' '+'<tsms:minimumSeparationDistance uom="NAUTICAL_MILES">'+str(separationDistance)+"E+00</tsms:minimumSeparationDistance>"+"\n"))
                        separationDistance +=separationIncrement
                        if separationDistance > TopOfSepAxis:
                            separationDistance = .1
                            dt=dt + datetime.timedelta(seconds = dateTimeIncrement)
                    else:
                        v.write(str(line))
            generatedInts +=1
        with open("tactical_ints_"+str(requiredNoOfInts)+"_interactions.xml", "a") as v:
            v.write(Footer+"\n")
    print "Created 'tactical_ints.xml' with %d interactions" % generatedInts



print "________________________________________________________________________________\n"
