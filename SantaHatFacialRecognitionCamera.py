import cv2
import dlib
from math import hypot

# Loading Camera and Nose image and Creating mask
cap = cv2.VideoCapture(0)


detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
	hat=cv2.imread("hat.png")
	beard=cv2.imread("beard.png")

	_, frame=cap.read()
	gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	faces=detector(frame)
	dilation=1.6
	for face in faces:
		landmarks=predictor(gray_frame, face)
		
		#HAT

		toReduceYHat=(landmarks.part(27).y-landmarks.part(8).y)+(landmarks.part(29).y-landmarks.part(27).y)
		toReduceXHat=(landmarks.part(34).x-landmarks.part(32).x)
		if (landmarks.part(8).y+toReduceYHat<=0):
			continue
		topHat=(landmarks.part(19).x-toReduceXHat, 2*landmarks.part(27).y-landmarks.part(8).y+toReduceYHat)
		leftHat=(landmarks.part(17).x-toReduceXHat, 2*landmarks.part(17).y-landmarks.part(36).y+toReduceYHat)
		rightHat=(landmarks.part(26).x-toReduceXHat, 2*landmarks.part(26).y-landmarks.part(45).y+toReduceYHat)

		hatWidth=int(dilation*hypot(leftHat[0]- rightHat[0], leftHat[1]-rightHat[1]))
		hatHeight=hatWidth

		topLeftHat=(int(leftHat[0]), int(topHat[1]))

		hat=cv2.resize(hat, (hatWidth, hatHeight))
		hatGray=cv2.cvtColor(hat, cv2.COLOR_BGR2GRAY)
		_, hatMask=cv2.threshold(hatGray, 25, 255, cv2.THRESH_BINARY_INV)

		hatArea=frame[topLeftHat[1]:topLeftHat[1]+hatHeight, topLeftHat[0]: topLeftHat[0]+hatWidth]
		
		try:
			hatAreaNoHat=cv2.bitwise_and(hatArea, hatArea, mask=hatMask)
			finalHat=cv2.add(hatAreaNoHat, hat)

			frame[topLeftHat[1]:topLeftHat[1]+hatHeight, topLeftHat[0]: topLeftHat[0]+hatWidth]=finalHat
		except:
			pass

		#BEARD
		
		#Reduce for BEARD
		toReduceYBeard=(landmarks.part(15).y-landmarks.part(16).y)
		toReduceXBeard=(landmarks.part(34).x-landmarks.part(31).x)
		topBeard=(landmarks.part(51).x-toReduceXBeard, landmarks.part(51).y-toReduceYBeard)
		leftBeard=(landmarks.part(6).x-toReduceXBeard,  landmarks.part(6).y-toReduceYBeard)
		rightBeard=(landmarks.part(10).x-toReduceXBeard, landmarks.part(10).y-toReduceYBeard)
		
		beardWidth=int(dilation*hypot(leftBeard[0]-rightBeard[0], leftBeard[1]-rightBeard[1]))
		beardHeight=int(1.354*beardWidth)

		topLeftBeard=(int(leftBeard[0]), int(topBeard[1]))

		beard=cv2.resize(beard, (beardWidth, beardHeight))
		beardGray=cv2.cvtColor(beard, cv2.COLOR_BGR2GRAY)
		_, beardMask=cv2.threshold(beardGray, 25, 255, cv2.THRESH_BINARY_INV)

		#if beardHeight>500:
	#		break

		beardArea=frame[topLeftBeard[1]: topLeftBeard[1]+beardHeight, topLeftBeard[0]: topLeftBeard[0]+beardWidth]
		try:
			beardAreaNoBeard=cv2.bitwise_and(beardArea, beardArea, mask=beardMask)
			finalBeard=cv2.add(beardAreaNoBeard, beard)

			frame[topLeftBeard[1]:topLeftBeard[1]+beardHeight, topLeftBeard[0]:topLeftBeard[0]+beardWidth]=finalBeard
		except:
			pass

		#cv2.imshow("Hat Area", topBeard)
		#cv2.imshow("Hat mask", hatMask)
		#cv2.imshow("Hat area no hat", hatAreaNoHat)


		#cv2.circle(frame, topBeard, 3, (255,0,0), -1)
		#cv2.circle(frame, rightBeard, 3, (255,0,0), -1)
		#cv2.rectangle(frame, (int(leftHat[0]), int(topHat[1])), (int(rightHat[0]), int(rightHat[1])), (0,255,0), 2)
		#cv2.imshow("hat", beard)
		

	cv2.imshow("Frame", frame)
	#cv2.imshow("hat", hat)
	key=cv2.waitKey(1)

	#Is user presses esc, code exits
	if (key==27):
		break
cap.release() 
cv2.destroyAllWindows() 