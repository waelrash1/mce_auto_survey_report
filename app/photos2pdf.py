# /usr/local/bin/python3
# -*- coding: utf-8 -*-
# **** Merge all images in a path in a  pdf file and then merge this file
# with the generated report in one pdf ****

import os
import pathlib
import shutil
import sys
from os import listdir

from PyPDF2 import PdfFileMerger
from fpdf import FPDF

from imageTrans import reduceImageSize


def photosMerge(imagePath, filename):
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")
    # print(__file__)
    # imagePath= './'+reportCode+'/'
    tempPath = imagePath + 'temp/'
    print('Start image processing to reduce size...')
    imageProcessing(imagePath, tempPath)
    print('image processing is compeleted')

    print('Start the process of merging all images in ' + imagePath + ' Directory has been started... ')

    # filename=reportCode # 104747
    path = tempPath
    # Allowed Extensions
    extensions = ('jpg', 'jpeg', 'png')
    try:
        # get list of all images, excluding sub-directories
        dirs = listdir(path)
        imagelist = list(filter(lambda x: os.path.isfile(os.path.join(path, x)), dirs))
        imagelist = sorted(imagelist)
    except FileNotFoundError:
        print(' file directory path: ' + path + ' is not found.')

    pdf = FPDF('P', 'mm', 'A4')  # create an A4-size pdf document
    # pdf.SetMargins(10., 10., 10.)

    pdf.add_page('P')
    pdf.set_font('Times', 'B', 28)
    pdf.multi_cell(200, 5, ('Survey\'s Pictures Appendix.'))
    pdf.ln()

    # Merging the images.
    # Start the pdf at coordinate (x,y)
    # Set the width and height to w and h
    x, y, w, h = 5, 5, 200, 200

    try:
        for image in imagelist:
            if (image.split('.')[1] in extensions):
                print(image)
                pdf.add_page()
                pdf.image(path + image, x, y, w, h)
    except UnboundLocalError:
        output += 'file directory path: ' + path + ' is not found. <br/> </h3>'

    # Save the generated pdf
    imgPDFPath = imagePath + filename + "-images.pdf"
    pdf.output(imgPDFPath, "F")

    # delete temp directory and all its files
    shutil.rmtree(tempPath, ignore_errors=False, onerror=None)
    return imgPDFPath


def mergeReportPhotos(ReportPDFPath, ImgPDFPath, outputfile):
    # Merging the image pdf with the report

    pdfs = [ReportPDFPath, ImgPDFPath]
    merger = PdfFileMerger()
    print('The merging process has been started... ')
    for pdf in pdfs:
        try:
            merger.append(pdf)
            print('The file name: ' + pdf + ' has been merged sucessfully.')
        except FileNotFoundError:
            print('file name: ' + pdf + ' is not found.')

    merger.write(outputfile)
    merger.close()
    print('The task has been completed sucessfully!')


def imageProcessing(imagePath, tempPath):
    #  reportCode = '104747-be'
    # make a directory for reducing the image size- same report name with _trans as suffix
    # tempPath=imagePath+'temp/'
    pathlib.Path(tempPath).mkdir(parents=True, exist_ok=True)
    extensions = ('jpg', 'jpeg', 'png')
    try:
        # get list of all images, excluding sub-directories
        dirs = listdir(imagePath)
        imagelist = list(filter(lambda x: os.path.isfile(os.path.join(imagePath, x)), dirs))
        imagelist = sorted(imagelist)
        print(imagelist)
    except FileNotFoundError:
        output += 'file directorimagePathy path: ' + path + ' is not found. <br/> </h3>'
    try:
        for image in imagelist:
            if (image.split('.')[1] in extensions):
                print(image)
                reduceImageSize(imagePath, tempPath, image)
    except UnboundLocalError:
        output += 'file directory path: ' + path + ' is not found. <br/> </h3>'


if __name__ == "__main__":
    photosMerge('./output/104747/', '104747')
