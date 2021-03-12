import cv2 as cv
import cgi, os
import cgitb; cgitb.enable()
from PIL import Image
from PIL import ImageChops
import PIL.ImageDraw
import face_recognition
import sendEmails


toClownOrNotToClown=True

theClown=face_recognition.load_image_file("chris.png")
clownEncoding=face_recognition.face_encodings(theClown)[0]

imageNAME="class1.png"

personImg=Image.open(imageNAME)
personImg.save("duplicate.png")
image="duplicate.png"
personImg=Image.open(image)


hat=Image.open("hat.png")
beard=Image.open("beard.png")
clown=Image.open("clownwig.png")

#FACIAL RECOGNITION
givenImage=face_recognition.load_image_file(image)
face_locations=face_recognition.face_locations(givenImage)
pilImage=PIL.Image.fromarray(givenImage)

def hatFun(hat, left, right):
	hatWidth, hatHeight=hat.size
	hatDilation=1.3
	hatWidth=int((left-right)*hatDilation)
	hatHeight=hatWidth
	hatnewsize=(hatWidth, hatHeight)
	hat=hat.resize(hatnewsize)
	return hat

def beardFun(beard, left, right):
	beardWidth, beardHeight=beard.size
	beardDilation=1
	beardWidth=int((left-right)*beardDilation)
	beardHeight=beardWidth
	beardnewsize=(beardWidth, beardHeight)
	beard=beard.resize(beardnewsize)

	return beard

def clownFun(clown, left, right):
	clownWidth, clownHeight=clown.size
	clownDilation=2
	clownWidth=int((left-right)*clownDilation)
	clownHeight=clownWidth
	clownnewsize=(clownWidth, clownHeight)
	clown=clown.resize(clownnewsize)

	return clown


for location in face_locations:
	top, left, bottom, right=location
	# print("Top: ", top)
	# print("Left: ", left)
	# print("Bottom: ", bottom)
	# print("Right: " , right)
	# print()
	face_image=givenImage[top:bottom, right:left]
	pil_image=Image.fromarray(face_image)
	
	draw=PIL.ImageDraw.Draw(pilImage)
	draw.rectangle([left, top, right, bottom], outline="green", width=10)

	personImgWidth, personImgHeight=personImg.size

	hat=hatFun(hat, left, right)
	beard=beardFun(beard, left, right)
	clown=clownFun(clown, left, right)

	personImgWidth, personImgHeight=personImg.size
	results=face_recognition.compare_faces([clownEncoding], face_recognition.face_encodings(face_image)[0], .34)
	
	if results[0] and toClownOrNotToClown:
		#Clown
		image=Image.new("RGBA", (personImgWidth, personImgHeight), (0,0,0,0))
		image.paste(personImg, (0,0))
		image.paste(clown, (int(right+(right-left)/2.6), 2*top-bottom), mask=clown)
		personImg=Image.open("duplicate.png")

		image.save("duplicate.png")
		personImg=Image.open("duplicate.png")

	
	else:
		image=Image.new("RGBA", (personImgWidth, personImgHeight), (0,0,0,0))
		image.paste(personImg, (0,0))
		image.paste(beard, (right, int((bottom+top)/2)), mask=beard)

		image.save("duplicate.png")
		personImg=Image.open("duplicate.png")
		

		#HAT		
		image=Image.new("RGBA", (personImgWidth, personImgHeight), (0,0,0,0))
		image.paste(personImg, (0,0))
		image.paste(hat, (right, 2*top-bottom), mask=hat)
		personImg=Image.open("duplicate.png")

		image.save("duplicate.png")
		personImg=Image.open("duplicate.png")


try:
	image.show()
except:
	print("No humans in this pic ;)")
	exit()

if __name__=="__main__":
	sendEmails.addImage(imageNAME)