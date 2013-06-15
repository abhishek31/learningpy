#! usr/lib/python2.7

"""
Python script to convert text files in a folder(and all  its subfolders) into pdf files.
Uses Reportlab for pdf creation.
Usage : python txtTopdf.py -d <directory> -i <filename>

"""
import os
import sys
import argparse

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet 


def convertToPdf(fname):
    filename = os.path.splitext(fname)[0] + ".pdf"
    
    doc = SimpleDocTemplate(str(filename),  \
                        rightMargin=40, leftMargin=40, \
                        topMargin=40, bottomMargin=25, \
                        pagesize=A4)

    elements = []    
    
    # Open the model report
    infile   = file(fname).read()
    report_paragraphs = infile.split("\n")
    
    StyleSheet = getSampleStyleSheet()
    
    for para in report_paragraphs:
        if not para:  
            elements.append(Paragraph('<br />\n', style=StyleSheet['Normal']))
        else:
            elements.append(Paragraph(para, style=StyleSheet['Normal']))
    doc.build(elements)
   

def main(argv=None):
    if argv == None:
        argv = sys.argv
    
    parser = argparse.ArgumentParser(description='convert txt file/files in a directory to pdf')
    parser.add_argument('-d','--directory', default = os.getcwd(), required = False)
    parser.add_argument('-i','--filename', action = "store", required = False)
    argv = vars(parser.parse_args())
    
    
    src_file = None    
    if argv is None:
        src_dir = os.getcwd()
    elif argv['filename'] is not None:
        src_file = argv['filename']
    else:
        src_dir = argv['directory']
    
    supported_extensions = [".txt"]
    
    if src_file is None:
        all_files = [os.path.join(root,fls)
                     for root,_,flsnm in os.walk(src_dir)
                     for fls in flsnm
                     if os.path.splitext(fls)[1] in supported_extensions]
        
        if len(all_files) == 0:
            return
        
        for filen in all_files:
            convertToPdf(filen)
    else:
        convertToPdf(src_file)
    
    print "Done Converting"
    
if __name__ == "__main__":
    sys.exit(main())
