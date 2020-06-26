#-*-coding:utf-8-*-

import pydicom as pdicom
import numpy as np
import argparse
import os


lstFilesDCM = [] 

def load_scan(path):
  
    for dirName, subdirList, fileList in os.walk(path):
        for filename in fileList:
            if ".dcm" in filename.lower():
                lstFilesDCM.append(os.path.join(dirName,filename))
    return lstFilesDCM

def encode_tags():

    elem = pdicom.dataelem.DataElement(0x00080005,'CS','\ISO 2022 IR 149')
    
    for filenameDCM in lstFilesDCM:
        ds = pdicom.dcmread(filenameDCM)
        ds.add(elem)
        try:
            ret = pdicom.charset.encode_string(ds.ProtocolName,  ['iso8859'])
            ds.ProtocolName = str(ret, 'euc-kr')
        except:
            pass
        ds.save_as(filenameDCM)
    return None

def print_element(csvpath):
    
    f = open(csvpath,'w',encoding='utf-8')
    
    # What elements do you want to print?
    elem = ['SOPInstanceUID',
            'StudyDate',
            'ManufacturerModelName',
            'PatientID', 'PatientSize', 'PatientWeight', 
            'DeviceSerialNumber',
            'SoftwareVersions',
            'ProtocolName',
            'SeriesDescription']

    
    # write header
    string = "filename,"+",".join(elem)+"\n"
    f.write(string)
    
    for filenameDCM in lstFilesDCM:
        #read the file
        ds = pdicom.read_file(filenameDCM)
        
        #read elem
        line = []
        line.append(filenameDCM)
        print(filenameDCM)
        for e in elem:
            if not (hasattr(ds, e)):
                if e is 'SeriesDescription':
                    if ('Femur' or 'Spine' or 'DXA') in ds.ProtocolName:
                        token = "DXA Reports"
                else:
                    token = "None"
            else:
                token = str(ds[e].value)
            line.append(token)
        string = ",".join(line) + "\n"
        f.write(string)
        
    f.close()     

if __name__ == '__main__':
  # Collect all dicom images
    parser = argparse.ArgumentParser(description='Pass in valid arguments if you don\'t want my default configuration')
    parser.add_argument('--infile', default='./dicom', help='path to dicom files')
    parser.add_argument('--outfile', default='dataset.csv', help='path to output csv file')
    args = parser.parse_args()

    lstFilesDCM = load_scan(args.infile)
    encode_tags()
    print_element(args.outfile)

          
        