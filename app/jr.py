# -*- coding: utf-8 -*-
import os
from datetime import datetime

from flask import Flask, request, make_response, jsonify, send_file
from flask_httpauth import HTTPBasicAuth
from pyreportjasper import JasperPy

from copyFiles import copyPhotos
from photos2pdf import photosMerge, mergeReportPhotos

app = Flask(__name__)

jasper = JasperPy()
auth = HTTPBasicAuth()

app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']
PDF_DIRECTORY = app.config['PDF_ABS_PATH']
app.jasper_dir = app.config['JASPER_JRXML_PATH']
app.working_dir = app.config['WORKING_DIRECTORY']


def reportInputFile(reportName):
    return app.jasper_dir + reportName + '.jrxml'


def compiling(report_name):
    input_file = reportInputFile(report_name)
    jasper.compile(input_file)


def processing(SurveyID, report_name):
    # Path of the report name
    input_file = reportInputFile(report_name)
    output_file = app.working_dir + SurveyID
    print(output_file)
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    jasper.process(input_file, output_file, format_list=["pdf"])
    return output_file + '/' + report_name + '.pdf'


@auth.get_password
def get_password(username):
    if username == 'mceapi':
        return app.secret_key
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


def sendEmail():
    return 0


def updateDB(conn):
    return 0


@app.route('/report')
def my_route():
    SurveyID = request.args.get('surveyID', default=1, type=str)
    print(SurveyID)
    report_name = request.args.get('reportName', default='surveyReportBefore', type=str)
    # reportName
    # report_name= 'surveyReportBefore'
    # call using url/report?surveyID=104747&reportName=surveyReportBefore

    # SurveyID='104747' # for testing; this should be pass as a parameter in url of the api

    # Copy photo directory from shared photo server
    photoPath = copyPhotos(SurveyID)
    print('Image path....', photoPath)

    # Merge all photos in one pfd file
    PhotosPDFPath = photosMerge(photoPath, SurveyID)
    print('pdf photo path....', PhotosPDFPath)

    reportPDFPath = processing(SurveyID, report_name)

    print('pdf report path....', reportPDFPath)

    # Merge all in one pfd file

    output_dir = "./output/pdfs/"
    outputFilePath = output_dir + SurveyID + "-full_" + datetime.now().strftime("%Y%m%d+%H%M%S") + '.pdf'


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
@auth.login_required
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(PDF_DIRECTORY):
        path = os.path.join(PDF_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@app.route('/download/<filename>', methods=['GET'])
@auth.login_required
def download_file(filename):
    suffix = ".pdf"
    print(filename)
    if filename.lower().endswith(".pdf"):
        path = os.path.join(PDF_DIRECTORY, filename)
    else:
        path = os.path.join(PDF_DIRECTORY, filename + suffix)
        filename = os.path.join(filename + suffix)
    print(filename)
    try:
        return send_file(path, as_attachment=True)
    except:
        return path + " REPORT IS NOT READY YET...IT TAKES A WHILE TO BE GENERATED"


if __name__ == '__main__':
    # compiling()
    print('http://0.0.0.0:8000/report?surveyID=104747&reportName=surveyReportBefore')
    print('http://0.0.0.0:8000/files')
    print('http://0.0.0.0:8000/download/104747.pdf')
    print('lsof -ti:8002 | xargs kill')

    app.run(port='8000')
