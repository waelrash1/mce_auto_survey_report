# /usr/local/bin/python3
# **** Merge all images in a path in a  pdf file and then merge this file
# with the generated report in one pdf ****

import os
import pathlib
import shutil
import sys
from datetime import datetime
from os import listdir

from PyPDF2 import PdfFileMerger
from fpdf import FPDF

from imageTrans import reduceImageSize


def makeReport(reportCode):
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")
    print(__file__)
    imagePath = './' + reportCode + '/'
    tempPath = imagePath + 'temp/'
    imageProcessing(imagePath, tempPath)
    output = '<p> <h3>The processof merging all images in ./' + reportCode + ' Directory has been started... <br/>'
    print(output)
    filename = reportCode  # '104747-be' #input("insert file name")
    path = tempPath  # "./"+filename+"/" # get the path of images
    # Allowed Extensions
    extensions = ('jpg', 'jpeg', 'png')
    try:
        # get list of all images, excluding sub-directories
        dirs = listdir(path)
        imagelist = list(filter(lambda x: os.path.isfile(os.path.join(path, x)), dirs))
        imagelist = sorted(imagelist)
    except FileNotFoundError:
        output += 'file directory path: ' + path + ' is not found. <br/> </h3>'

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
    pdf.output(imagePath + filename + "-images.pdf", "F")

    # Merging the image pdf with the report
    print(filename)
    pdfs = [imagePath + '/' + filename + '-report.pdf', imagePath + '/' + filename + '-images.pdf']
    merger = PdfFileMerger()
    # output+='<p> <h3>The merging process has been started... <br/>'
    for pdf in pdfs:
        try:
            merger.append(pdf)
            output += 'The file name: ' + pdf + ' has been merged sucessfully. <br/>'
        except FileNotFoundError:
            output += 'file name: ' + pdf + ' is not found. <br/> </h3>'
    reportNameFull = imagePath + '/' + filename + "-full_" + datetime.now().strftime("%Y%m%d+%H%M%S") + '.pdf'

    merger.write(reportNameFull)
    merger.close()
    output += 'The task has been completed sucessfully! </h3>'

    # delete temp directory and all its files
    shutil.rmtree(tempPath, ignore_errors=False, onerror=None)
    return output


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
    # Generate report and name as assicode_report
    # processing()
    makeReport('104747')
    # imageProcessing('./104747-be')
