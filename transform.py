import extract
import pandas as pd
import os
import json
import units_json_parsing as ujp
import re
import time
import address_module as am 
def rename_columns(df):
    cols = [
        'province', #province_name
        'p_type', #province_type
        'district', #district_name
        'd_type', #district_type
        'ward', #ward_name
        'w_type' #ward_type
    ]
    # apply
    df.columns = cols
    return df

def parse_to_new_columns(df):
    '''Parse the full X name to X name + X_type
    Where X is province, district, ward
    Example: 'Thành phố Hồ Chí Minh' -> 'Hồ Chí Minh' + 'Thành phố'
    '''

    # Tỉnh - Thành phố
    df['p_type'] = df['p_type'].apply(lambda x: 'Thành phố' if 'Thành phố' in x else 'Tỉnh')
    # Quận - Huyện - Thị xã - Thành phố
    df['d_type'] = df['d_type'].apply(lambda x: 'Thị xã' if 'Thị xã' in x else ('Quận' if 'Quận' in x else ('Huyện' if 'Huyện' in x else 'Thành phố')))
    # Phường - Xã - Thị trấn
    df['w_type'] = df['w_type'].apply(lambda x: 'Phường' if 'Phường' in x else ('Thị trấn' if 'Thị trấn' in x else 'Xã'))

    return df

def unify_data(df):
    ''' Format data by remove '0' at the beginning of district and ward'''
   
    df['district'] = df['district'].apply(lambda x: re.sub(r'^0', '', x))
    df['ward'] = df['ward'].apply(lambda x: re.sub(r'^0', '', x))
    return df

def make_entity_json(df, folder_path, qh_dir, hcmhn_dir, px_dir):

    # Create folder if not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if not os.path.exists(qh_dir):
        os.makedirs(qh_dir)
    if not os.path.exists(hcmhn_dir):
        os.makedirs(hcmhn_dir)
    if not os.path.exists(px_dir):
        os.makedirs(px_dir)

    #tinh huyen
    thanhpho_huyen = ujp.tinhhuyenf('huyện', 'thành phố', df)
    ujp.save_to_json(qh_dir, 'thanhpho_huyen.json', thanhpho_huyen)
    thanhpho_quan = ujp.tinhhuyenf('quận', 'thành phố', df)
    ujp.save_to_json(qh_dir, 'thanhpho_quan.json', thanhpho_quan)
    tinh_huyen = ujp.tinhhuyenf('huyện', 'tỉnh', df)
    ujp.save_to_json(qh_dir, 'tinh_huyen.json', tinh_huyen)
    tinh_tp = ujp.tinhhuyenf('thành phố', 'tỉnh', df)
    ujp.save_to_json(qh_dir, 'tinh_tp.json', tinh_tp)
    tinh_tx = ujp.tinhhuyenf('thị xã', 'tỉnh', df)
    ujp.save_to_json(qh_dir, 'tinh_tx.json', tinh_tx)

    #HCMHN
    hcm_hn_huyen = ujp.hcm_hn('huyện', 'thành phố', df)
    ujp.save_to_json(hcmhn_dir, 'hcmhn_huyen.json', hcm_hn_huyen)
    hcm_hn_quan = ujp.hcm_hn('quận', 'thành phố', df)
    ujp.save_to_json(hcmhn_dir, 'hcmhn_quan.json', hcm_hn_quan)
    hcm_hn_tp = ujp.hcm_hn('thành phố', 'thành phố', df)
    ujp.save_to_json(hcmhn_dir, 'hcmhn_tp.json', hcm_hn_tp)
    hcm_hn_tx = ujp.hcm_hn('thị xã', 'thành phố', df)
    ujp.save_to_json(hcmhn_dir, 'hcmhn_tx.json', hcm_hn_tx)

    # qh_px
    huyen_thitran = ujp.qh_px('thị trấn', 'huyện', df)
    ujp.save_to_json(px_dir, 'huyen_thitran.json', huyen_thitran)
    huyen_xa = ujp.qh_px('xã', 'huyện', df)
    ujp.save_to_json(px_dir, 'huyen_xa.json', huyen_xa)

    quan_phuong = ujp.qh_px('phường', 'quận', df)
    ujp.save_to_json(px_dir, 'quan_phuong.json', quan_phuong)

    tp_phuong = ujp.qh_px('phường', 'thành phố', df)
    ujp.save_to_json(px_dir, 'tp_phuong.json', tp_phuong)
    tp_xa = ujp.qh_px('xã', 'thành phố', df)
    ujp.save_to_json(px_dir, 'tp_xa.json', tp_xa)

    tx_phuong = ujp.qh_px('phường', 'thị xã', df)
    ujp.save_to_json(px_dir, 'tx_phuong.json', tx_phuong)
    tx_xa = ujp.qh_px('xã', 'thị xã', df)
    ujp.save_to_json(px_dir, 'tx_xa.json', tx_xa)

    print('Entity json created successfully')

def transform_db(df):

    # rename columns
    df = rename_columns(df)
    # parse to new columns
    df = parse_to_new_columns(df)
    # lowercase data
    df = df.apply(lambda x: x.str.lower() if x.dtype=='object' else x)

    # unify data
    folder_path = 'D:\\ki6\\DS108\\ThucHanh\\address_Data\\Vietnamese_address_parsing\\entities'
    qh_dir = os.path.join(folder_path, 'qh')
    hcmhn_dir = os.path.join(folder_path, 'hcmhn')
    px_dir = os.path.join(folder_path, 'px')

    df = unify_data(df)
    # make entity json
    make_entity_json(df, folder_path, qh_dir, hcmhn_dir, px_dir)

    return df

def transform_raw_data(data, path, dir_name):
    address_dict = am.load_address_dict(path, dir_name)
    
    result = pd.DataFrame(columns = ['address','tinh','tinh_cat', 'qh', 'qh_cat', 'px', 'px_cat', 'duong', 'Address_ch', 't_check', 'h_check'])
    address_list = data['address'].tolist()

    for address in address_list:
        tmp_address = {
            'address': [address]
        }
        data = am.update_entity_address(tmp_address, address_dict)
        result = pd.concat([result, pd.DataFrame(data, index = [0])], ignore_index = True)
    
    return result
def transform_address(data):
    # Transform raw address by user input
    # Load address dictionary
    path = 'D:\\ki6\\DS108\\ThucHanh\\address_Data\\Vietnamese_address_parsing'
    dir_name = 'entities'
    address_dict = am.load_address_dict(path, dir_name)
    address_to_parse = data

    # Update entity address
    result = am.update_entity_address(address_to_parse, address_dict)

    return result

def save_to_excel(df, path, file_name):
    df.to_excel(os.path.join(path, file_name), index=False)
    print('Data saved to excel successfully')

if __name__ == '__main__':
    VN_address_df = extract.extract_vietnamese_administrative_units_data_from_db()
    transformed_df = transform_db(VN_address_df)

# For extracting raw data from excel file

    # data = pd.read_excel('D:\\ki6\\DS108\\ThucHanh\\address_Data\\Vietnamese_address_parsing\\address_full_0712.xlsx')
    # data.drop(columns=['Unnamed: 0'], inplace=True)
    # raw_data = data.loc[101:, :]
    # raw_data.rename(columns={'Address': 'address'}, inplace=True)

    # path = 'D:\\ki6\\DS108\\ThucHanh\\address_Data\\Vietnamese_address_parsing'
    # dir_name = 'entities'

    # transformed_raw_data = transform_raw_data(raw_data, path, dir_name)
    # save_to_excel(transformed_raw_data, path, 'parsed_address_data.xlsx')

# For extracting raw data from input
    address_test = ["123, KTX khu B, Đông Hoà, Dĩ An, BD"]
    print('Raw address:', address_test)
    print('Transformed address:', transform_address(address_test))
    #save to json style raw -> parsed
    


    
