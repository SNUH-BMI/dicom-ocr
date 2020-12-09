#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import json
import argparse
from copy import deepcopy
from tqdm.notebook import tqdm


# In[2]:


def get_document_from(response):
    document = {}
    table_starts_from = 0
    rows = []
    lines = []
    for item in response["Blocks"]:
          if item["BlockType"] == "LINE":
            if item['Geometry']['BoundingBox']['Left'] < 0.4 or item['Text'] == ':':
                continue
            row_found=False
            for index, row in enumerate(rows):
                bbox_top = item["Geometry"]["BoundingBox"]["Top"]
                bbox_bottom = item["Geometry"]["BoundingBox"]["Top"] + item["Geometry"]["BoundingBox"]["Height"]
                bbox_centre = item["Geometry"]["BoundingBox"]["Top"] + item["Geometry"]["BoundingBox"]["Height"]/2
                row_centre = (row['Top'] + row['Bottom'])/2

                if (bbox_centre > row['Top'] and bbox_centre < row['Bottom']) or (row_centre > bbox_top and row_centre < bbox_bottom):
                    #Bbox appears inside the row
                    lines.append([index, (item["Text"].replace(",",".").replace("..","."), 
                                          item["Geometry"]["BoundingBox"]["Left"])])
                    row_found=True
                    break
            if not row_found:
                rows.append({'Top':item["Geometry"]["BoundingBox"]["Top"], 'Bottom':item["Geometry"]["BoundingBox"]["Top"] + item["Geometry"]["BoundingBox"]["Height"]})
                lines.append([len(rows)-1, (item["Text"].replace(",",".").replace("..","."), 
                                            item["Geometry"]["BoundingBox"]["Left"])])
            if item["Text"] == 'Region':
                table_starts_from = len(rows)
            if 'ANCILLARY RESULTS' in item["Text"]:
                return None, None
            
    lines.sort(key=lambda x: (x[0],x[1][1]))
    
    for idx in range(len(rows)):
        document[idx] = []
        for l in lines:
            if l[0] == idx:
                document[idx].append((l[1][0]))
            
    return document, table_starts_from


# In[3]:


def get_table_from(document, table_starts_from):
    table = []
    for i, line in enumerate(document.values()):
        if i < table_starts_from:
            continue
        elif line[0] == 'Region':
            continue

        if len(table)>0 and len(line) < 2:
            break
            
        table.append(line)
    return table


# In[4]:


def validate(filename,row):
    res = None
    stop = False
   
    del_target = -1
    while True:
    
        for col_index in range(del_target+1, len(row)):
            word = row[col_index]
            if col_index == 0: #region
                try:
                    word = float(word) # it means it's not string.
                    if word == 12: # probably L2
                        res='ok'
                    else:
                        row.insert(0, ' ')    # insert virtual region
                except ValueError: # it means it's string.
                    try:
                        next_word = row[col_index+1]
                        next_word = float(next_word)
                    except IndexError: # unvalid row
                        return None 
                    except ValueError: # garbage value
                        del_target = col_index
                        break
                    res = 'ok'
            else: 
                res_0_1 = re.match('^-?\d[.]$', word)
                res_0_2 = re.match('^\d[.]\d\d$', word)
                if res_0_1 is not None or res_0_2 is not None: # 마지막 1 인식 x
                    word += '1'
                res_1 = re.match('^-?\d$', word) #소수점 인식 x
                if res_1 is not None: 
                    word += '.1'
                res_2 = re.match('^-\d\d$', word)
                if res_2 is not None:
                    word = word[:2]+'.'+word[-1]
                #--------------------------------------             
                res = re.match('\d[.]\d\d\d', word)
                if res is None:
                    res = re.match('^\d\d$', word)
                    if res is None:
                        res = re.match('^\d\d\d$', word)
                        if res is None:
                            res = re.match('^\d$', word)
                            if res is not None:
                                if word[0] > '2':
                                    res = None
                            if res is None:
                                res = re.match('^-?\d+[.]\d$', word)
                                if res is None:
                                    res = re.match('^-$', word)
           # print(row)
            if res is None:
                del_target = col_index
                break
        else:
            stop = True
        
        if del_target >=0 and stop == False:
#             print('*'*20)
            if len(row) == 6 and del_target != 0:
                print("WARNING!!")
                print(filename)
                print(del_target, row)
            else:
                try:
#                     print(filename)
#                     print(del_target, row)
                    del row[del_target]
#                     print("SUCCESS")
                except:
                    print(filename)
                    print("ERROR")
                    return None
            
        if stop == True:
            break
            
        
        
    return row


# In[9]:

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='path where json files are located')
    args = parser.parse_args()

    file_dir = args.path

    os.chdir(file_dir)
    print(f"Now in {os.getcwd()}")
    tmp = os.listdir(file_dir)
    jsonlst = [f for f in tmp if '.json' in f]

    tables = []

    with open('output.csv',"w") as fout, open('error.csv',"w")as ferror:
        fout.write("filename,Region,BMD,T-Score(%),T-Score,Z-Score(%),Z-Score\n")
        ferror.write("filename,Region,BMD,T-Score(%),T-Score,Z-Score(%),Z-Score\n") 

        for f in tqdm(jsonlst):
            with open(f) as jsonfile:
                response = json.load(jsonfile)
            
            document, table_starts_from = get_document_from(response)
            table = get_table_from(document, table_starts_from)
            copy_table = deepcopy(table)
            for row in copy_table:
                row = validate(f, row)
                if row is None:
                    copy_table = None
                    break

            
            csv = ''
            if copy_table is None:
                for row in table:
                    csv += f.replace('png.json','dcm') + ","
                    csv += (",").join(row)
                    csv += "\n"
                print(csv)
            else:
                for row in copy_table:
                    csv += f.replace('png.json','dcm') + ","
                    csv += (",").join(row)
                    csv += "\n"
                print(csv)