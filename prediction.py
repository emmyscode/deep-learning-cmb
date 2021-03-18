#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libs.pconv_model import PConvUnet
from optparse import OptionParser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from copy import deepcopy
import os
parser = OptionParser()
parser.add_option("--weight_dir",
                  dest="weight", default='./',
                  help="output file")

parser.add_option("--index",
                  dest="id", default=0,
                  help="the path and file name of CMB Commander archive file ")

options, args = parser.parse_args()

def complete_image(pred,true,mask):
    com_image = np.zeros((400,400,3))
    for i in range(400):
      for j in range(400):
        if mask[i,j,0] == 1:#vaild pixel
          com_image[i,j,0] = true[i,j,0]
          com_image[i,j,1] = true[i,j,1]
          com_image[i,j,2] = true[i,j,2]
        else:#hole pixel
          com_image[i,j,0] = pred[i,j,0]
          com_image[i,j,1] = pred[i,j,1]
          com_image[i,j,2] = pred[i,j,2]
    return com_image

weight  = options.weight
model = PConvUnet(vgg_weights=None, inference_only=True)
model.load(weight, train_bn=False)
imid = int(options.id)
masks = mpimg.imread('./datasets/mask/data/'+str(imid)+'pict.png')[:,:,:3]
Planck_Image = mpimg.imread('./datasets/test/data/'+str(imid)+'pict.png')[:,:,:3]
PCNN_Image = complete_image(model.predict([np.expand_dims(Planck_Image,0), np.expand_dims(masks,0)])[0],Planck_Image,masks)
masked = deepcopy(Planck_Image)
masked[masks==0] = 1
if not os.path.exists('./datasets/predicted/'):
        os.makedirs('./datasets/predicted/')
fig=plt.imsave('./datasets/predicted/'+str(imid)+'pred.png', PCNN_Image)
