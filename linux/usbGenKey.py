#!/usr/bin/env python
#coding=utf-8
# Enumerate usb devices
import usb
import os 
import sys 

def str2hex(s):
	return ''.join(['%02X' %ord(i) for i in s]) 

def getUSBList():
	import usb
	usbList=[]
	if sys.platform == 'linux2': 
		busses = usb.busses()
		for bus in busses:
			devices = bus.devices
			for dev in devices:
				usbList.append((str('%04x')% dev.idVendor,str('%04x')% dev.idProduct))

	elif sys.platform == 'win32': 
		import win32com.client 
		wmi = win32com.client.GetObject ("winmgmts:") 
		for usb in wmi.InstancesOf ("Win32_USBHub"):
			DeviceID=usb.DeviceID 
			try:
				idVendor,idProduct=DeviceID.split('''\\''')[1].split('&')
				usbList.append((str(idVendor[-4:]),str(idProduct[-4:])))
			except:
				pass
	else:
		pass
	return usbList



def GennerateLicense(idVendor,idProduct):
	from Crypto.Cipher import AES
	msg=idVendor+idProduct+'\xff\xfe\xfd\xfc\xfb\xfa\xf9\xf8'
	key = b'Sixteen byte key'
	iv = b'This is an IV456'
	cipher = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = cipher.encrypt(msg)

	lic=str2hex(ciphertext)

	'''
	delic=''.join([chr(int(lic[i:i+2],16)) for i in range(0,len(lic),2)])
	obj = AES.new(key, AES.MODE_CBC, iv)
	demsg=obj.decrypt(delic)
	print msg,ciphertext,lic,delic,demsg
	'''

	return lic


if __name__=='__main__':
	print "Please do not plug in USB device at first time!\nPress Any key to continue."
	s = raw_input(">")
	usblist1=getUSBList()
	print "Please plug in your USB device and press Any key to continue..\n"
	s = raw_input(">")
	usblist2=getUSBList()

	license=''

	for i in usblist2:
		if not i in usblist1:
			print i
			idVendor,idProduct=i
			license= GennerateLicense(idVendor,idProduct)
	if license:
		open('USB_License.lic','wb').write(license)
	else:
		license= GennerateLicense('0781','5571')
		open('USB_License.lic','wb').write(license)
