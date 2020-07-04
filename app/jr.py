# -*- coding: utf-8 -*-
import os
from os import listdir
import pathlib
import shutil 
from pyreportjasper import JasperPy
from flask import Flask, request, make_response, abort, jsonify,send_file, send_from_directory
from copyFiles import copyPhotos
from datetime import datetime
from photos2pdf import photosMerge,mergeReportPhotos

app = Flask(__name__)
PDF_DIRECTORY = "./output/pdfs/"
jasper = JasperPy()

def reportInputFile(reportName):
    input_file =  os.path.dirname(os.path.abspath(__file__)) + \
                 '/JR4O/'+reportName+'.jrxml'
    return input_file

def compiling(report_name):
    input_file= reportInputFile(report_name)
    jasper.compile(input_file)

def processing(SurveyID,report_name):
     # Path of the report name
    input_file= reportInputFile(report_name)
    
    output_file = os.path.dirname(os.path.abspath(__file__)) + '/output/'+SurveyID
    print(output_file)
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    jasper.process(input_file, output_file, format_list=["pdf"])
    return output_file+'/'+report_name+'.pdf'

def sendEmail():
    return 0

def updateDB(conn):
    return 0
    
@app.route('/report')
def my_route():


  SurveyID = request.args.get('surveyID', default = 1, type = str)
  print(SurveyID)
  report_name = request.args.get('reportName', default = 'surveyReportBefore', type = str)
  #reportName
  #report_name= 'surveyReportBefore'
  # call using url/report?surveyID=104747&reportName=surveyReportBefore
  
  #SurveyID='104747' # for testing; this should be pass as a parameter in url of the api
  
  # Copy photo directory from shared photo server
  photoPath= copyPhotos(SurveyID)
  print('Image path....',photoPath)
  
  # Merge all photos in one pfd file
  PhotosPDFPath= photosMerge(photoPath,SurveyID)
  print('pdf photo path....',PhotosPDFPath)

  reportPDFPath=processing(SurveyID,report_name )

  print('pdf report path....',reportPDFPath)

  # Merge all in one pfd file
  
  output_dir = "./output/pdfs/"
  outputFilePath = output_dir+SurveyID +"-full_"+datetime.now().strftime("%Y%m%d+%H%M%S")+'.pdf'


  mergeReportPhotos(reportPDFPath,PhotosPDFPath,outputFilePath)
  
##  #reportPath= os.path.dirname(os.path.abspath(__file__)) + '/output/'+SurveyID
##  
##  # get the pdf of the report
##  dirs = listdir(reportPath)
##  reportname = list(filter(lambda x:os.path.isfile(os.path.join(reportPath, x)), dirs))
##  print(reportname)


  try:
      with app.open_resource(outputFilePath) as f:
          print(f)
          content = f.read()
      resposta = make_response(content)
      resposta.headers['Content-Type'] = 'application/pdf; charset=utf-8'
      resposta.headers['Content-Disposition'] = 'inline; filename=hello_world_params.pdf'
      return resposta
  except IOError:
      return make_response("<h1>403 Forbidden</h1>", 403)

@app.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(PDF_DIRECTORY):
        path = os.path.join(PDF_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

@app.route('/download/<filename>')
def download_file(filename):
    suffix = ".pdf"
    print(filename)
    if filename.lower().endswith(".pdf"):
        path= os.path.join(PDF_DIRECTORY, filename)
    else:
        path= os.path.join(PDF_DIRECTORY, filename + suffix)
        filename=os.path.join(filename + suffix)
    print(filename)
    try:
        return send_file(path, as_attachment=True)
    except:
        return path+" REPORT IS NOT READY YET...IT TAKES A WHILE TO BE GENERATED"

if __name__ == '__main__':
    #compiling()
##    http://0.0.0.0:5000/report?surveyID=104747&reportName=surveyReportBefore
##    http://0.0.0.0:5000/files
##    http://0.0.0.0:5000/download/104747.pdf
##    lsof -ti:8002 | xargs kill

    app.run(port='8000')
