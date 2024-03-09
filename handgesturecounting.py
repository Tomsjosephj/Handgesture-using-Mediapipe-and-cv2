import mediapipe
import cv2

mp_hands=mediapipe.solutions.hands 
draw=mediapipe.solutions.drawing_utils

hand=mp_hands.Hands(max_num_hands=1)

video=cv2.VideoCapture(0)


while True:
    sucess,img=video.read()
    imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hand.process(imgrgb)
    fingertipids=[4,8,12,16,20]
    lmlist=[]


    
    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
             #print(handlms)
             for id,lm in enumerate(handlms.landmark):
              #print(id,lm)  
              cx=lm.x
              cy=lm.y
              lmlist.append([id,cx,cy])
            #   print(lmlist)
              if len(lmlist)!=0 and len(lmlist)==21:
                  fingerlist=[]
                  #thumb
                  if lmlist[20][1]<lmlist[12][1]:
                      if lmlist[4][1]<lmlist[3][1]:
                          fingerlist.append(0)
                      else:
                          fingerlist.append(1)
                  else:
                       if lmlist[4][1]>lmlist[3][1]:
                          fingerlist.append(0)
                       else :
                          fingerlist.append(1)
                       

                  #other fingers
                  for i in range(1,5):
                     if lmlist[fingertipids[i]][2]<lmlist[fingertipids[i]-2][2]:
                         fingerlist.append(1)
                     else:
                         fingerlist.append(0)
                     #print(fingerlist) 

             if len(fingerlist)!=0:
                     fingercount=fingerlist.count(1) 
                     #print(fingercount)
             cv2.rectangle(img,(15,370),(100,450),(255,255,255),thickness=cv2.FILLED)
             cv2.putText(img,str(fingercount),(35,436),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)                             
            #  draw.draw_landmarks(img,handlms,mp_hands.HAND_CONNECTIONS,draw.DrawingSpec(color=(255,255,255),thickness=2,circle_radius=6),draw.DrawingSpec(color=(0,255,0 ),thickness=2))

    cv2.imshow('Hand',img)
    if cv2.waitKey(1) &0XFF==ord('q'):
        break
video.release()
cv2.destroyAllWindows()
