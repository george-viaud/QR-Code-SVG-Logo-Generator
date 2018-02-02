#! /usr/bin/python

#
#	pyqrcode.py
#
#	George Viaud
#	Modified for the CrypTile open-source hardware project 
#	Details can be found in the readme and at https://CrypTile.us/
#
#	This is mildly altered fork of QR-Code-SVG-Logo-Generator by David Janes
#

import pyqrcode
from lxml import etree
import math
import sys
import logging
logging.basicConfig(level=logging.DEBUG if __debug__ else logging.INFO)

block_size = 10
offset = block_size / 2
circle_radius = block_size * 2

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def generateQRImageForUrl(url):
    qr_image = pyqrcode.MakeQRImage(url, errorCorrectLevel = pyqrcode.QRErrorCorrectLevel.M, block_in_pixels = 1, border_in_blocks=0)
    return qr_image

def getSVGFileContent(filename):
    '''
    root may be the svg element itself, so search from tree

    solution for multiple (or no) namespaces from
    http://stackoverflow.com/a/14552559/493161
    '''
    document = etree.parse(filename)
    logging.debug('document: %s', document)
    svg = document.xpath('//*[local-name()="svg"]')[0]
    logging.debug('svg: %s', svg)
    return svg

def touchesBounds(center, x, y, radius, block_size):
    scaled_center = center / block_size
    dis = distance((scaled_center , scaled_center), (x, y))
    rad = radius / block_size
    return dis <= rad + 1	

if len(sys.argv) < 4:
    print "Incorrect args, try:"
    print './generate.py ./octocat.svg "http://github.com" ./out.svg'
    print "or"
    print './generate.py --nologo "http://github.com" ./out.svg'
	
    sys.exit(0)

if str(sys.argv[1]) == '--nologo':
	circle_radius = 0
	logoPath = 0
else:
	logoPath = sys.argv[1]
	
url = sys.argv[2]
outputname = sys.argv[3]

im = generateQRImageForUrl(url);

imageSize = str(im.size[0] * block_size)

# create an SVG XML element (see the SVG specification for attribute details)
doc = etree.Element('svg', width=imageSize, height=imageSize, version='1.1', xmlns='http://www.w3.org/2000/svg')

pix = im.load()

center = im.size[0] * block_size / 2


rEye = 34.1
rWhite = 26
rPupil = 14

rEyeColor = 'black'
rWhiteColor = 'white'
rPupilcolor = 'black'

etree.SubElement(doc, 'circle', cx=str(3*block_size + offset), cy=str(3*block_size + offset), r=str(rEye), fill=rEyeColor)
etree.SubElement(doc, 'circle', cx=str(3*block_size + offset), cy=str(3*block_size + offset), r=str(rWhite), fill=rWhiteColor)
etree.SubElement(doc, 'circle', cx=str(3*block_size + offset), cy=str(3*block_size + offset), r=str(rPupil), fill=rPupilcolor)

etree.SubElement(doc, 'circle', cx=str((im.size[0]-4)*block_size + offset), cy=str(3*block_size + offset), r=str(rEye), fill=rEyeColor)
etree.SubElement(doc, 'circle', cx=str((im.size[0]-4)*block_size + offset), cy=str(3*block_size + offset), r=str(rWhite), fill=rWhiteColor)
etree.SubElement(doc, 'circle', cx=str((im.size[0]-4)*block_size + offset), cy=str(3*block_size + offset), r=str(rPupil), fill=rPupilcolor)

etree.SubElement(doc, 'circle', cx=str(3*block_size + offset), cy=str((im.size[1]-4)*block_size + offset), r=str(rEye), fill=rEyeColor)
etree.SubElement(doc, 'circle', cx=str(3*block_size + offset), cy=str((im.size[1]-4)*block_size + offset), r=str(rWhite), fill=rWhiteColor)
etree.SubElement(doc, 'circle', cx=str(3*block_size + offset), cy=str((im.size[1]-4)*block_size + offset), r=str(rPupil), fill=rPupilcolor)

for xPos in range(0,im.size[0]):
    for yPos in range(0, im.size[1]):

        color = pix[xPos, yPos]
        if color == (0,0,0,255):

            withinBounds = not touchesBounds(center, xPos, yPos, circle_radius, block_size)
            withinBounds = withinBounds and not (xPos < 7 and yPos < 7)
            withinBounds = withinBounds and not (xPos < 7 and yPos > (im.size[1] - 8))
            withinBounds = withinBounds and not (xPos > (im.size[0] - 8) and yPos < 7)
			
            if (withinBounds):
                etree.SubElement(doc, 'circle', cx=str(xPos*block_size + offset), cy=str(yPos*block_size + offset), r='4', fill='black')
			
if logoPath:
	logo = getSVGFileContent(logoPath)
	test = str(logo.get("viewBox"))
	Array = []

	if (test != "None"):
		Array = test.split(" ")
		width = float(Array[2])
		height = float(Array[3])
	else :
		width = float(str(logo.get("width")).replace("px", ""))
		height = float(str(logo.get("height")).replace("px", ""))

	dim = height
	if (width > dim):
		dim = width
	scale = circle_radius * 2.0 / width

	scale_str = "scale(" + str(scale) + ")"

	xTrans = ((im.size[0] * block_size) - (width * scale)) / 2.0
	yTrans = ((im.size[1] * block_size) - (height * scale)) / 2.0

	translate = "translate(" + str(xTrans) + " " + str(yTrans) + ")"

	logo_scale_container = etree.SubElement(doc, 'g', transform=translate + " " + scale_str)

	for element in logo.getchildren():
		logo_scale_container.append(element)


# ElementTree 1.2 doesn't write the SVG file header errata, so do that manually
f = open(outputname, 'w')
f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
f.write(etree.tostring(doc))
f.close()
