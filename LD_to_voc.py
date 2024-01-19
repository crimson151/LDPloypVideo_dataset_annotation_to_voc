from pascal_voc_writer import Writer
import os
import sys
from skimage import measure
from shapely.geometry import Polygon, MultiPolygon
import cv2
import numpy as np

def LDAnnotation_2_voc(folderPath,output_folder,dataname,category):
    Image_Path = folderPath.replace("Annotations","Images")
    for root, dirs, files in os.walk(folderPath):
        subfoldername = os.path.basename(root)
        for file in files:
            if file.endswith('txt'):
                imagePath = "./" + os.path.join(Image_Path, subfoldername, file).replace("\\","/").replace(".txt",".jpg")
                image = cv2.imread(os.path.join(imagePath))
                imageShape = [image.shape[0], image.shape[1], image.shape[2]]

                writer = Writer(imagePath, image.shape[0], image.shape[1], image.shape[2], database=dataname)

                with open((os.path.join(root, file)).replace("\\","/"), 'r', encoding='utf-8') as f:
                    line = f.readline()
                    line = int(line)
                    while line > 0:
                        lines = f.readline()
                        lines_list = lines.split()
                        min_x, min_y, max_x, max_y = lines_list[0], lines_list[1], lines_list[2], lines_list[3]
                        writer.addObject(category,min_x, min_y, max_x, max_y, difficult=0)
                        writer.save(os.path.join(output_folder, subfoldername, file.replace('.txt', '.xml')))
                        line = line - 1


if __name__ == "__main__":
    dataname = 'LDPolypVideo'
    category = 'polyp'
    read_path = 'LDPolypVideo/TrainValid/Annotations'
    save_path = 'LDPolypVideo/TrainValid/Annotations_xml'

    # process
    LDAnnotation_2_voc(read_path, save_path, dataname, category)
