import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import math


def find_box(_img,ksize):
    r = _img.shape[0]
    c = _img.shape[1]
    
    ret3, th3 = cv2.threshold(_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    blur = cv2.medianBlur(th3, ksize)

    #plt.imshow(blur)
    #plt.show()

    blur = cv2.medianBlur(blur, ksize)
    #plt.imshow(blur)
    #plt.show()
    t, contours, hierarchy = cv2.findContours(blur, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    _box = [[None, None], [None, None]]

    for cnt in contours:
        
        x, y, w, h = cv2.boundingRect(cnt)
        #print w,h

        if 25 < w < 40 and 25 < h < 40:
            a = 0 if x < r / 2 else 1
            b = 0 if y < c / 2 else 1
            _box[a][b] = (x + (w / 2), y + (h / 2))
            #print _box
            #cv2.rectangle(_img, (x, y), (x + w, y + h), 0, 20)
    #plt.imshow(_img)
    #plt.show()


    return _box

def view_find_box(_img,ksize):
    r = _img.shape[0]
    c = _img.shape[1]
    
    ret3, th3 = cv2.threshold(_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    blur = cv2.medianBlur(th3, ksize)

    plt.imshow(blur)
    plt.show()

    blur = cv2.medianBlur(blur, ksize)
    plt.imshow(blur)
    plt.show()
    t, contours, hierarchy = cv2.findContours(blur, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    _box = [[None, None], [None, None]]

    for cnt in contours:
        
        x, y, w, h = cv2.boundingRect(cnt)
        print w,h

        if 25 < w < 40 and 25 < h < 40:
            a = 0 if x < r / 2 else 1
            b = 0 if y < c / 2 else 1
            _box[a][b] = (x + (w / 2), y + (h / 2))
            #print _box
            cv2.rectangle(_img, (x, y), (x + w, y + h), 0, 20)
    plt.imshow(_img)
    plt.show()


    return _box





cwd = os.getcwd()
path = cwd + '/raw_images/'

f=open('not_working_list.txt','w')


file_list = os.listdir(path)

it=int(sys.argv[1])


total=len(file_list)

cnt=0

for file in file_list:
    print cnt,'/',total, '=',it
    cnt+=1
    img_original = cv2.imread(path + file, 0)
    color_image = cv2.imread(path + file)
    img = cv2.imread(path + file, 0)
    r = img.shape[0]
    c = img.shape[1]
    #plt.imshow(img)
    #plt.show()

    box = find_box(img,39)

    if box[0][0] is None or box[0][1] is None or box[1][0] is None or box[1][1] is None:
        #print 'before'
        #view_find_box(img_original,39)
        f.write(file+'\n')
        continue


    dy = box[0][1][1] - box[0][0][1]
    dx = box[0][1][0] - box[0][0][0]

    angle = math.atan(dy / dx) if dx!=0 else math.pi/2
    angle=90-math.degrees(angle)
    if angle > 90 :
        angle=-(180-angle)
    #print (dy/dx),angle
   

    M = cv2.getRotationMatrix2D((c / 2, r / 2), -angle, 1)
    img_original = cv2.warpAffine(img_original, M, (c, r))
   


    box = find_box(img_original,35)

    if box[0][0] is None or box[0][1] is None or box[1][0] is None or box[1][1] is None:

        #print 'after'

        
        #view_find_box(img_original,35)

        f.write(file+'\n')
        continue



    #plt.imshow(img_original)
    #plt.show()


    #continu




    x1=box[0][0][0]
    y1=box[0][0][1]







    '''for i in range(0,10):
        cv2.line(img_original,(x1,y1+266+i*213),(x1+2500,y1+266+i*213),0,2)
    for i in range(0,10):
        cv2.line(img_original,(x1+30+i*180,y1),(x1+30+i*180,y1+2500),0,2)'''

    ret3, img_original = cv2.threshold(img_original, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)


    for i in range(0,10):
        for j in range(0,9):
            x=x1+34+i*180
            y=y1+266+j*213

            if(j>6) :
                y+=20
            if (j==6) :
                y+=15

            cut=img_original[y+15:y+200,x+15:x+170]

            final_cut=cut
            kernel = np.ones((13,13),np.uint8)
            dilation = cv2.dilate(cut,kernel,iterations = 1)
          

            edge=cv2.Canny(dilation,100,200)
            max_w=-1
            max_h=-1

            t, contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
          

            for cntr in contours:
                
                x, y, w, h = cv2.boundingRect(cntr)
                #print w,h

                if w>max_w and h>max_h:
                    c1=img_original[y+15:y+200,x+15:x+170]

                    xs= x-2 if x-2>0 else x
                    xe= x+w+2 if x+w+2<cut.shape[0] else x+w
                    ys= y-2 if y-2>0 else y
                    ye= y+h+2 if y+h+2<cut.shape[1] else y+h

                    final_cut=cut[ys:ye,xs:xe]
                    max_w=w
                    max_h=h


            
            #cv2.imshow('a',cut)
            
            #cv2.imshow('b',final_cut)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()



                

            p=cwd+"/datasetOriginal/"+str(i)+"/"+str(it)+"."+str(j)+".jpg"

            cv2.imwrite(p,final_cut)
    it+=1
    

f.close()


