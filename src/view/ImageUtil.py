'''
Created on 23-Dec-2016

@author: vijay
'''

import os

class ImageUtility():
    
    def __init__(self):
        pass
    
    def readImages(self):
        os.chdir(os.path.join('..', 'images'))
        print os.getcwd()
        relevant_path = '.'
        included_extenstions = ['jpg', 'bmp', 'png', 'gif']
        file_names = [fn for fn in os.listdir(relevant_path) if any(fn.endswith(ext) for ext in included_extenstions)]
        file_names.sort(key=str)
        print file_names
    
    def getImageList(self):
        
        return None

if __name__ == '__main__':
    imageUtility = ImageUtility()
    imageUtility.readImages()
    pass
