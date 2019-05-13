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

def getLicense():
	from Crypto.Cipher import AES
	lic=open('USB_License.lic','rb').read()

	ciphertext=''.join([chr(int(lic[i:i+2],16)) for i in range(0,len(lic),2)])
	key = b'Sixteen byte key'
	iv = b'This is an IV456'

	cipher = AES.new(key, AES.MODE_CBC, iv)
	msg=cipher.decrypt(ciphertext)

	return msg[:4],msg[4:8]

def checkAuthority():
	usblist=getUSBList()
	#print usblist
	AuthUsb=getLicense()
	if AuthUsb in usblist:
		return True
	return False


if __name__=='__main__':
	pass
