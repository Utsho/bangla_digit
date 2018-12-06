from random import randint

import os
from PIL import Image
path='test'
classnames=os.listdir(path)

f1=open('data_set_config.txt','r')
st=f1.readline()
st1=st.split(' ')
image_size=int(st1[0])
images=[]
for temp in classnames:


	images.append(Image.open(path+'/'+temp))
k=len(images)
im2=[]
for i in range(k):	
	img=images[i]
	im2.append(img)
h=0
for i in range(k):
	h=h+image_size*im2[i].size[1]/im2[i].size[0]+5

result = Image.new('L', (image_size,h),'white')
lp=0
for i in range(k):	
	img=im2[i]
	img=img.convert('L')
	h=image_size*img.size[1]/img.size[0]
	if h<1:
		h=1
	img=img.resize((image_size,h),Image.ANTIALIAS)
	result.paste(img, box=(0, lp))
	lp=lp+5+img.size[1]
		
	
result.save('res.png')	
