
import sys
import json
import time
import serial
from telnetlib import Telnet

connected = False;
ser = serial.Serial('/dev/cu.usbmodem1421', 9600);

while not connected:
	serin = ser.read();
	connected = True;


tn=Telnet('localhost',13854);
start=time.time();

i=0;
# app registration step (in this instance unnecessary) 
#tn.write('{"appName": "Example", "appKey": "9f54141b4b4c567c558d3a76cb8d715cbde03096"}');
tn.write('{"enableRawOutput": true, "format": "Json"}');


outfile="null";
if len(sys.argv)>1:
	outfile=sys.argv[len(sys.argv)-1];
	outfptr=open(outfile,'w');

eSenseDict={'attention':0, 'meditation':0};
waveDict={'lowGamma':0, 'highGamma':0, 'highAlpha':0, 'delta':0, 'highBeta':0, 'lowAlpha':0, 'lowBeta':0, 'theta':0};
signalLevel=0;

ready=0;
phase=0;

while i<100:
	blinkStrength=0;

	line=tn.read_until('\r');
	if len(line) > 20:  
		timediff=time.time()-start;
		dict=json.loads(str(line));
		if "poorSignalLevel" in dict:
			signalLevel=dict['poorSignalLevel'];
		if "blinkStrength" in dict:
			blinkStrength=dict['blinkStrength'];
		if "eegPower" in dict:
			waveDict=dict['eegPower'];
			eSenseDict=dict['eSense'];
		outputstr=str(timediff)+ ", "+ str(signalLevel)+", "+str(blinkStrength)+", " + str(eSenseDict['attention']) + ", " + str(eSenseDict['meditation']) + ", "+str(waveDict['lowGamma'])+", " + str(waveDict['highGamma'])+", "+ str(waveDict['highAlpha'])+", "+str(waveDict['delta'])+", "+ str(waveDict['highBeta'])+", "+str(waveDict['lowAlpha'])+", "+str(waveDict['lowBeta'])+ ", "+str(waveDict['theta']);
		print "time: " + str(timediff) + " | attn: " + str(eSenseDict['attention']) + " | signal: " + str(signalLevel);
		
		if int(eSenseDict['attention']) == 0 or ready == 0:
			ser.write(str("45;"));
			print (ser.read());
			#print("printing 45");
		else:
			ser.write(str(eSenseDict['attention'])+";");
			print (ser.read());
			if phase == 1 and int((eSenseDict['attention'])) < 10:
				ser.write(str("0;"));
				time.sleep(3);
				tn.close();
				outfptr.close();
				ser.close();
			if phase == 2 and int((eSenseDict['attention'])) < 20:
				ser.write(str("0;"));
				time.sleep(3);
				tn.close();
				outfptr.close();
				ser.close();
			if phase == 3 and int((eSenseDict['attention'])) < 30:
				ser.write(str("0;"));
				time.sleep(3);
				tn.close();
				outfptr.close();
				ser.close();
			if phase == 4:
				ser.write(str("100;"));
				time.sleep(3);
				tn.close();
				outfptr.close();
				ser.close();
		
			if timediff >= 10.0 and phase == 0:
				print("Phase 2 - min limit : 10");
				ser.write(str("101;"));
				phase=1;

			if timediff >= 25.0 and phase == 1:
				print("Phase 3 - min limit : 20");
				ser.write(str("102;"));
				phase=2;

			if timediff >= 30.0 and phase == 2:
				print("Phase 4 - min limit : 30");
				ser.write(str("103;"));
				phase=3;

			if timediff >= 35.0 and phase == 3:
				print("END");
				ser.write(str("105;"));
				phase=4; #end


		if int(eSenseDict['attention']) > 0 and ready == 0:
			start=time.time();
			ready=1;
			ser.write(str("106;"));
			print("START - Phase 1");
		
		if outfile!="null":
			outfptr.write(outputstr+"\n");      


tn.close();
outfptr.close();
ser.close();

