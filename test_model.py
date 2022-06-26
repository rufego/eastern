#import cv2
import torch
#import tensorflow
#import PIL
#from PIL import Image


model = torch.hub.load('.',
                       'custom',
                       #path='C:/Users/rfernand/OneDrive - Cox Communications/Documents/eastern/project/data/yolov5/runs/train/exp_good/best_all_done-fp16.tflite',
                       path='best_all_done-fp16.tflite',
                       source='local')

model.names = ['firearm']


def inference(fic):
    results = model(fic)
    results.save()

#inference('C:/Users/rfernand/projecto/flask/test/1.jpeg')