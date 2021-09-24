from PIL import Image, ImageEnhance
import numpy as np
import argparse
import time

parser = argparse.ArgumentParser(description='Upscale an image.')
parser.add_argument('path', type=str,
                    help='Path to the image')
t = time.time()

print("Loading")

path = args.path

im = Image.open(path)
px = np.array(im)
w = im.width
h = im.height

print("Upscaling")

# Create masks for each color in a bayer filter

rmask = np.array([[[1],[0]],[[0],[0]]])
gmask = np.array([[[0],[1]],[[0],[0]]])
bmask = np.array([[[0],[0]],[[0],[1]]])

# Create a mask for the original color (on the second bayer green)

origmask = np.array([[[0,0,0],[0,0,0]],[[1,1,1],[0,0,0]]])

# Stretch the original image to a higher resolution

full = np.repeat(np.repeat(px,2,axis=0),2,axis=1)

# Tile the masks to scale

rmask = np.tile(rmask, (h,w,1))
gmask = np.tile(gmask, (h,w,1))
bmask = np.tile(bmask, (h,w,1))
origmask = np.tile(origmask, (h,w,1))

# Correct the mask shapes and extract/mask the colors

red = full[:,:,0] * rmask.reshape(h*2,w*2)
green = full[:,:,1] * gmask.reshape(h*2,w*2)
blue = full[:,:,2] * bmask.reshape(h*2,w*2)

# Mask the streched image

mask = full * origmask

# Create a greyscale image from the combined masks average

grey = np.ndarray((h*2,w*2,3))
grey[:,:,0] = (mask[:,:,0] + mask[:,:,1] + mask[:,:,2])/3
grey[:,:,1] = (mask[:,:,0] + mask[:,:,1] + mask[:,:,2])/3
grey[:,:,2] = (mask[:,:,0] + mask[:,:,1] + mask[:,:,2])/3

# Initialize the output image with the combined colors

outarr = np.ndarray((h*2,w*2,3))
outarr[:,:,0] = red + green + blue
outarr[:,:,1] = red + green + blue
outarr[:,:,2] = red + green + blue

# Mix the output and greyscale images

bias = outarr + grey
del red,green,blue,mask,rmask,gmask,bmask,origmask

# Apply the bias to fill in detail and average.

outarr = (full+bias)/2
del full,bias,grey

print("Post Processing")

# Parse pixel data

out = Image.fromarray(np.uint8(outarr))

# Correct image saturation

saturate = ImageEnhance.Color(out)
out = saturate.enhance(2)

# Blur to reduce jagged edges
# TODO: Find a better method

blur = ImageEnhance.Sharpness(out)
out = blur.enhance(.5)

print("Saving")

# Sometimes the image will fail to save. Make it
# a function that can be called again to save time.

def save():
  out.save("Output.png")
save()

del out,outarr,px

print(f"Completed in {time.time() - t} seconds.")
