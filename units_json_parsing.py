import os
import json
import pandas


def save_to_json(dir, extension, data):
    json_file_path = os.path.join(dir, extension)
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

def tinhhuyenf(type1, type2, df):
    '''Parsing the district and province data to json entity by type1, type2
    Type 2 has multiple type 1
    '''
    data = df[df['province'].apply(lambda x: x not in ['hà nội', 'hồ chí minh'])]
    sorted_data = data[(data['d_type']==type1) & (data['p_type']==type2)]
    grouped_data = sorted_data.groupby('province')['district'].apply(set).reset_index() # group by province, get unique district
    grouped_data = grouped_data.set_index('province')['district'].apply(list).to_dict() # convert to dict
  
    return grouped_data

def qh_px(type1, type2, df):
    '''Parsing the ward and district data to json entity by type1, type2
    Type 2 has multiple type 1
    '''
    data = df[(df['w_type'] == type1)&(df['d_type'] == type2)]
    data = data.groupby('district')['ward'].apply(set).reset_index()
    data = data.set_index('district')['ward'].apply(list).to_dict()
    return data

def hcm_hn(type1, type2, df):
    '''Parsing the HCM and Hanoi data to json entity by type1, type2
    Type 2 has multiple type 1
    '''
    data = df[df['province'].apply(lambda x: x in ['hà nội', 'hồ chí minh'])]
    data = data[(data['d_type'] == type1)&(data['p_type'] == type2)]
    data = data.groupby('province')['district'].apply(set).reset_index()
    data = data.set_index('province')['district'].apply(list).to_dict()
    return data

if __name__ == '__main__':
    pass
