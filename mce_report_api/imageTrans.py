from PIL import Image
import math
def reduceImageSize(imagePath,tempPath,filename):
 #   image = Image.open('./104248-af/img01.jpg')
    image = Image.open(imagePath+filename)
    #print(image.size)
    x,y=image.size
    xnew,ynew=math.floor(x/2),math.floor(y/2)
    newImage = image.resize((xnew,ynew),Image.ANTIALIAS)
 #   newImage.save(path+'/img01_tr1.jpg', quality=95)
    newImage.save(tempPath+filename,optimize=True,quality=85)


if __name__== "__main__":
    reduceImageSize('./104248-af/','img01.jpg')
