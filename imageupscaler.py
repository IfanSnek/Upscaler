from pil import Image, ImageFilter, ImageEnhance
import urllib.request
import os

size = 4032
bright = 50
sat = (20,20,20)
bias = 80

print("Downloading")

urllib.request.urlretrieve(f"https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/CornSnake.jpg/{size}px-CornSnake.jpg", r"in.jpeg")
urllib.request.urlretrieve(f"https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/CornSnake.jpg/{size/2}px-CornSnake.jpg", r"orig.jpeg")

im = Image.open(r"in.jpeg")
ot = Image.new("RGB", ((im.width*2), (im.height*2)))
px = im.load()
ox = ot.load()
w = im.width
h = im.height

print("Upscaling")



def add(first,second):
  return (first[0]+second[0]-bright,first[1]+second[1]-bright,first[2]+second[2]-bright)
def sub(first,second):
  return (first[0]-second[0],first[1]-second[1],first[2]-second[2])
countery = -1
for y in range(0,h*2-1):
  counterx = -1
  if y%2==0:
    countery += 1
  if y>0 and y%100==0:
    print(str(y/h*200/4)[:5]+"%")
  for x in range(0,w*2-1):
      if x%2==0:
        counterx += 1
      color = add(px[counterx,countery], (bias,bias,bias))
      red = (color[0],color[0],color[0])
      green = (color[1],color[1],color[1])
      blue = (color[2],color[2],color[2])
      orig = add(color,sat)
      #R
      ox[x+1,y] = sub(add(red, orig), green)
      #G
      ox[x,y] = orig
      ox[x+1,y+1] = orig
      #B
      ox[x,y+1] = sub(add(blue, orig), green)

print("Saving")
def save():
  #ot.save("out.jpeg", compression='jpeg')
  out=ot
  squared = out.resize((out.width * 2, out.height * 2))
  aa = squared.resize((squared.width // 2, squared.height // 2), resample=Image.ANTIALIAS)
  aa.save("Output.png")
save()
