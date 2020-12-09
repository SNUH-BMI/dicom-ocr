import os
import pandas as pd
import argparse
from tqdm.notebook import tqdm

def pivot(path):
    df = pd.read_csv(path)
    df = df.fillna('NULL')
    df = df.drop_duplicates(['filename','Region'])
    
    my_pivot = df.pivot(index='filename', columns='Region')
    my_pivot = my_pivot.fillna('NULL')
    my_pivot.columns = [col[1]+" "+col[0] for col in my_pivot.columns.values]
    
    # set format for BMD column
    from tqdm import tqdm
    col = [c for c in my_pivot.columns if 'BMD' in c]
    for c in col:
        for i in tqdm(range(len(my_pivot[col]))):
            try:
                my_pivot[c][i] = round(float(my_pivot[c][i]), 3)
            except ValueError:
                continue
                
                
    col = my_pivot.columns.tolist()
    if ('spine' in path.lower()) or ('tbs' in path.lower()):
        d = {
            "T12": 0,
            "L1": 1,
             "L2": 2,
             "L3": 3,
             "L4": 4,
             "L5": 5,
             "L1-L2": 6,
             "L1-L3": 7,
             "L1-L4": 8,
             "L2-L3": 9,
             "L2-L4": 10,
             "L3-L4": 11
        }
    else:
        d = {
            "Neck": 1,
             "Upper": 2,
             "Lower": 3,
             "Wards": 4,
             "Troch": 5,
             "Shaft": 6,
             "Total": 7
        }
    
    
    
    
    res = sorted(col, key=lambda x:d[x.split()[0]])            
    my_pivot = my_pivot[res]
    my_pivot.to_csv(path.replace('output.csv', 'reshaped_output.csv'), encoding='utf-8', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', required=True)
    args = parser.parse_args()

    file_path = args.infile
    os.chdir(file_path.replace("output.csv",""))
    print(f"Now in {os.getcwd()}")
    
    try:
        pivot(file_path)
    except FileNotFoundError:
        print("** There is no output.csv to pivot! **")
    except Exception as e:
        print("** Unexpected Error **")
        print(e)



