from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Upscale an image.')
parser.add_argument('path', type=str,
                    help='Path to the image')

args = parser.parse_args()

print("Loading")

im = Image.open(args.path)
px = np.array(im)
w = im.width
h = im.height

print("Upscaling")

rmask = np.array([[[1],[0]],[[0],[0]]])
gmask = np.array([[[0],[1]],[[0],[0]]])
bmask = np.array([[[0],[0]],[[0],[1]]])
omask = np.array([[[0,0,0],[0,0,0]],[[1,1,1],[0,0,0]]])
full = np.repeat(np.repeat(px,2,axis=0),2,axis=1)
rmask = np.tile(rmask, (h,w,1))
gmask = np.tile(gmask, (h,w,1))
bmask = np.tile(bmask, (h,w,1))
omask = np.tile(omask, (h,w,1))
red = full[:,:,0] * rmask.reshape(h*2,w*2)
green = full[:,:,1] * gmask.reshape(h*2,w*2)
blue = full[:,:,2] * bmask.reshape(h*2,w*2)
o = full * omask
bias = np.mean(full)
grey = np.ndarray((h*2,w*2,3))
grey[:,:,0] = (o[:,:,0] + o[:,:,1] + o[:,:,2])/3
grey[:,:,1] = (o[:,:,0] + o[:,:,1] + o[:,:,2])/3
grey[:,:,2] = (o[:,:,0] + o[:,:,1] + o[:,:,2])/3
ox = np.ndarray((h*2,w*2,3))
ox[:,:,0] = red + green + blue
ox[:,:,1] = red + green + blue
ox[:,:,2] = red + green + blue
greyscale = ox + grey
del red,green,blue,o,rmask,gmask,bmask,omask
ox = (full+greyscale)/2
del full,greyscale

print("PostProcessing")

out = Image.fromarray(np.uint8(ox))
squared = out.resize((out.width * 2, out.height * 2))
aa = squared.resize((squared.width // 2, squared.height // 2), resample=Image.ANTIALIAS)
saturate = ImageEnhance.Color(aa)
aa = saturate.enhance(2)
blur = ImageEnhance.Sharpness(aa)
aa = blur.enhance(.5)

print("Saving")

def save():
  aa.save("Output.png")
save()

del out,aa,ox,px
