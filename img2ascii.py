import sys
from PIL import Image
from time import sleep

argv = sys.argv

global readFile
global color
global dim
global writeFile
global save

save = False
dim = 1
color = False

#Colors

head = "\033[95m"
blue = "\033[94m"
green = "\033[92m"
orange = "\033[93m"
red = "\033[91m"

bold = "\033[1m"

def displayHelp():
	print "img2ascii - Command-line image viewing utility"
	print "----------------------------------------------"
	print "Usage: img2ascii [-h] <file> [-cds] [options]..."
	print " "
	print "It is recommended that you render images no larger than 64x64 on the default scale"
	print "This program works best with grayscale/ black and white images"
	print " "
	print "-c Adds color to the letters in the console based on the parent image"
	print "-d Sets the dimensions of the ascii image with a single integer. This is defaulted to 1 character per pixel"
	print "-h -help -? Displays this help file"
	print "-s Saves the rendered ascii image to a text file - THIS OVERWRITES THE FILE"
	print "----------------------------------------------"
	print "Module created by Galen Nare."

if len(argv) < 2:
	displayHelp()
else:
	for i in argv:
		if i == "-h" or i == "-help" or i == "-?":
			displayHelp()
			break
		elif ".png" in i.lower() or ".jpg" in i.lower() or ".jpeg" in i.lower() or ".gif" in i.lower():
			readFile = Image.open(i,"r")
			writeFile = open(i + ".txt","w+")
		elif i == "-d":
			dim = int(float(raw_input("Enter scale: ")))
		elif i == "-s":
			save = True
		elif i == "-c":
			color = True
	w,h = readFile.size
	w = w / dim
	print dim
	h = h / dim
	newsize = int(w),int(h)
	unRot = readFile.resize(newsize, Image.ANTIALIAS)
	thumb = unRot.rotate(90)
	print "Image size: "+str(thumb.size)
	sleep(1)
	pix = thumb.load()
	line = ""
	lineBuf = []
	for p in range(w):
		for q in range(h):
			pixel = pix[p,q]
			if isinstance(pixel,int):
				r,b,g = pixel,pixel,pixel
			else:
				r,b,g = pixel
			rbdiff = abs(r-b)
			bgdiff = abs(b-g)
			diff = abs(rbdiff-bgdiff)
			if diff < 32:
				if 64 > g > 128:
					line = line + "H"
				elif 32 > g > 64:
					line = line + "I"
				elif g > 32:
					line = line + " "
				elif g < 128:
					line = line + "#"
			else:
				if r > b and r > g:
					if color:
						line = line + red
					line = line + "I"
				elif g > r and g > b:
					if color:
						line = line + green
					line = line + "#"
				elif b > r and b > g:
					if color:
						line = line + blue
					line = line + "H"
		print line
		lineBuf.append(line)
		line = ""
	if save:	
		for ln in lineBuf:
			writeFile.write(ln+"\n")
	writeFile.close()
	readFile.close()
