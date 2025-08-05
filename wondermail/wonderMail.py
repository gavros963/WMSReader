import math

class WMSParser:
	encryptionData = [
			0x2E, 0x75, 0x3F, 0x99, 0x09, 0x6C, 0xBC, 0x61, 0x7C, 0x2A, 0x96, 0x4A, 0xF4, 0x6D, 0x29, 0xFA, 
			0x90, 0x14, 0x9D, 0x33, 0x6F, 0xCB, 0x49, 0x3C, 0x48, 0x80, 0x7B, 0x46, 0x67, 0x01, 0x17, 0x59, 
			0xB8, 0xFA, 0x70, 0xC0, 0x44, 0x78, 0x48, 0xFB, 0x26, 0x80, 0x81, 0xFC, 0xFD, 0x61, 0x70, 0xC7, 
			0xFE, 0xA8, 0x70, 0x28, 0x6C, 0x9C, 0x07, 0xA4, 0xCB, 0x3F, 0x70, 0xA3, 0x8C, 0xD6, 0xFF, 0xB0, 
			0x7A, 0x3A, 0x35, 0x54, 0xE9, 0x9A, 0x3B, 0x61, 0x16, 0x41, 0xE9, 0xA3, 0x90, 0xA3, 0xE9, 0xEE, 
			0x0E, 0xFA, 0xDC, 0x9B, 0xD6, 0xFB, 0x24, 0xB5, 0x41, 0x9A, 0x20, 0xBA, 0xB3, 0x51, 0x7A, 0x36, 
			0x3E, 0x60, 0x0E, 0x3D, 0x02, 0xB0, 0x34, 0x57, 0x69, 0x81, 0xEB, 0x67, 0xF3, 0xEB, 0x8C, 0x47, 
			0x93, 0xCE, 0x2A, 0xAF, 0x35, 0xF4, 0x74, 0x87, 0x50, 0x2C, 0x39, 0x68, 0xBB, 0x47, 0x1A, 0x02, 
			0xA3, 0x93, 0x64, 0x2E, 0x8C, 0xAD, 0xB1, 0xC4, 0x61, 0x04, 0x5F, 0xBD, 0x59, 0x21, 0x1C, 0xE7, 
			0x0E, 0x29, 0x26, 0x97, 0x70, 0xA9, 0xCD, 0x18, 0xA3, 0x7B, 0x74, 0x70, 0x96, 0xDE, 0xA6, 0x72, 
			0xDD, 0x13, 0x93, 0xAA, 0x90, 0x6C, 0xA7, 0xB5, 0x76, 0x2F, 0xA8, 0x7A, 0xC8, 0x81, 0x06, 0xBB, 
			0x85, 0x75, 0x11, 0x0C, 0xD2, 0xD1, 0xC9, 0xF8, 0x81, 0x70, 0xEE, 0xC8, 0x71, 0x53, 0x3D, 0xAF, 
			0x76, 0xCB, 0x0D, 0xC1, 0x56, 0x28, 0xE8, 0x3C, 0x61, 0x64, 0x4B, 0xB8, 0xEF, 0x3B, 0x41, 0x09, 
			0x72, 0x07, 0x50, 0xAD, 0xF3, 0x2E, 0x5C, 0x43, 0xFF, 0xC3, 0xB3, 0x32, 0x7A, 0x3E, 0x9C, 0xA3, 
			0xC2, 0xAB, 0x10, 0x60, 0x99, 0xFB, 0x08, 0x8A, 0x90, 0x57, 0x8A, 0x7F, 0x61, 0x90, 0x21, 0x88, 
			0x55, 0xE8, 0xFC, 0x4B, 0x0D, 0x4A, 0x7A, 0x48, 0xC9, 0xB0, 0xC7, 0xA6, 0xD0, 0x04, 0x7E, 0x05  
		]

	bitValues = "&67NPR89F0+#STXY45MCHJ-K12=%3Q@W"

	byteSwap = [
			0x07, 0x1B, 0x0D, 0x1F, 0x15, 0x1A, 0x06, 0x01,
			0x17, 0x1C, 0x09, 0x1E, 0x0A, 0x20, 0x10, 0x21,
			0x0F, 0x08, 0x1D, 0x11, 0x14, 0x00, 0x13, 0x16,
			0x05, 0x12, 0x0E, 0x04, 0x03, 0x18, 0x02, 0x0B,
			0x0C, 0x19
		]


	WMSStruct = [
		{"name":"nullBits", "note":"Null bits", "size":8},
		{"name":"specialFloor", "note":"Special floor marker", "size":8},
		{"name":"floor", "note": "Floor", "size":8},
		{"name":"dungeon", "note": "Dungeon", "size":8},
		{"name":"flavorText", "note": "Modifies the flavor text", "size":24},
		{"name":"restriction", "note": "Restriction data", "size":11},
		{"name":"restrictionType", "note": "Restriction type; mon = 1, type = 0", "size":1},
		{"name":"reward", "note": "Reward", "size":11},
		{"name":"rewardType", "note": "Reward type", "size":4},
		{"name":"targetItem", "note": "Target item", "size":10},
		{"name":"target2", "note": "Additional target Poke for certain mission types", "size":11},
		{"name":"target", "note": "Target Poke", "size":11},
		{"name":"client", "note": "Client Poke", "size":11},
		{"name":"missionSpecial", "note": "Mission special texts", "size":4},
		{"name":"missionType", "note": "Mission type", "size":4},
		{"name":"mailType", "note": "Mail type marker (must be 0100 = 4)", "size":4},
		{"name":"checksum", "note":"checksum", "size":32, "noinclude":True}
	]


	def sanitize(wmString):
		wmString = wmString.upper()
		outstring = ''
		for i in wmString:
			if WMSParser.bitValues.find(i) != -1:
				outstring = outstring+i
        
    
		if len(outstring) != 34:
			print("sanitized WMS code is %d chars long, should be 34", len(outstring))
		return outstring

	def unscrambleString(wmString, swapArray=byteSwap):
		outstring = ''
		for i in swapArray:
			outstring = outstring + wmString[i]    
		return outstring
	def numToBits(num, outputSize):
		bits = f'{num:b}' + ''
		while len(bits) < outputSize:
			bits = '0'+bits
		return bits
     
	def bytesToBits(wmIntString):
		outString = ''
		for i in reversed(wmIntString):
			index = WMSParser.bitValues.find(i)
			if index != -1:
				outString = outString + WMSParser.numToBits(index, 5)
			else:
				raise ValueError
		return outString



	def getEncryptionEntries(checksum):
		amount = 17
		entries = []
		encPointer = checksum
		backwards = not(checksum % 2)
		i = 0
		while i != amount:
			entries.append(WMSParser.encryptionData[encPointer])
			if backwards:
				encPointer -= 1
				if encPointer < 0:
					encPointer = len(WMSParser.encryptionData) -1
			else:
				encPointer += 1
				if encPointer >= len(WMSParser.encryptionData):
					encPointer = 0
			i += 1
	
		return entries


	def getResetByte(checksum):
		checksumByte = checksum % 256
		resetByte = math.floor((checksumByte / 16) + 8 + (checksumByte % 16))
		if resetByte < 17:
			return -1
		else:
			return resetByte


	def decryptbitstream(curbitstream, encrypt=False):
		bitPtr = 0

		blocks = []
		origblocks = []


		checksumByte = 0
		checksumBits = ''
		skyChecksumBits = ''


		bitPtr = len(curbitstream)-8
		checksumBits = curbitstream[bitPtr:bitPtr+8]
		checksumByte = int(checksumBits, base=2)


		bitPtr -= 24
		skyChecksumBits = curbitstream[bitPtr:bitPtr+24]
		fullChecksum = int((skyChecksumBits + checksumBits), base=2)
		while bitPtr > 7:
			bitPtr -= 8
			data = int(curbitstream[bitPtr:bitPtr+8], base=2)
			blocks.append(data)
			origblocks.append(data)



		twoBitStart = curbitstream[0:2]
		bitPtr -= 2


		entries = WMSParser.getEncryptionEntries(checksumByte)


		resetByte = 255
		resetByte = WMSParser.getResetByte(fullChecksum)
		# Do the encryption
		tblPtr = 0
		encPtr = 0
		i = 0
		while i < len(blocks):
		
			if encPtr == resetByte:
				remaining = len(blocks) - i
				encPtr = 0
			inputByte = blocks[tblPtr]

			result = ''

			if encrypt:
				result = (inputByte + entries[encPtr]) & 0xFF
			else:
				result = (inputByte - entries[encPtr]) & 0xFF
		

			blocks[i] = result

			tblPtr += 1
			encPtr += 1
			i += 1
	
		outString = twoBitStart
		for blockPtr in reversed(blocks):
			outString += WMSParser.numToBits(blockPtr, 8)
	
		outString += skyChecksumBits + checksumBits

		return outString



	def bitsToStructure(bitString):
		bitPtr = 0
		outputStrut = {}
		outputStrutBit = {}


		for strutInfo in WMSParser.WMSStruct:
			bitData = bitString[bitPtr:bitPtr+strutInfo['size']]
			bitPtr += strutInfo['size']


			numData = int(bitData, base=2)

			outputStrut[strutInfo['name']] = numData
			outputStrutBit[strutInfo['name']] = bitData
	
		if bitPtr != len(bitString):
			print(f"WARNING: Not all available data was parsed into struct. Final bitPtr is {bitPtr}, length is {len(bitString)}")

		return outputStrut



     
     








