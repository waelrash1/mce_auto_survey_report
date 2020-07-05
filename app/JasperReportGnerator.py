import os

from pyreportjasper import JasperPy


def compiling():
    input_file = os.path.dirname(os.path.abspath(__file__)) + \
                 '/Invoice.jrxml'
    print(input_file)
    jasper = JasperPy()
    jasper.compile(input_file)


def processing():
    input_file = os.path.dirname(os.path.abspath(__file__)) + '/Invoice.jrxml'
    # output = os.path.dirname(os.path.abspath(__file__)) + '/output/invoice'

    input_file = '/Users/wael.rashwan/JaspersoftWorkspace/MyReports/Invoice.jrxml'

    output = '/Users/wael.rashwan/Documents/Python_code_mce/Image_meger_Script_June_2020/104747/104747-report2'
    jasper = JasperPy()
    jasper.process(
        input_file, output_file=output, format_list=["pdf", "rtf"])


if __name__ == "__main__":
    compiling()
    processing()
