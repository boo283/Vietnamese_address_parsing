import pandas as pd
import numpy as np
import csv
import json
import re
import os


class AddObj(object):
    pass


def ch_xlsx_to_csv(project_path, dir_name):
    dir_path = os.path.join(project_path, dir_name)
    ch = pd.read_excel(os.path.join(dir_path, 'chuanhoa.xlsx'))
    ch.to_csv(os.path.join(dir_path, 'chuanhoa.csv'), index=False)


def load_address_dict(project_path, dir_name):
    # load path
    dir_path = os.path.join(project_path, dir_name)

    # create obj to store data
    add_dicts = AddObj()

    # qh_px
    #add_dicts.huyen_phuong = json.load(open(os.path.join(dir_path, 'px', 'huyen_phuong.json')))
    add_dicts.huyen_thitran = json.load(open(os.path.join(dir_path, 'px', 'huyen_thitran.json')))
    add_dicts.huyen_xa = json.load(open(os.path.join(dir_path, 'px', 'huyen_xa.json')))
    add_dicts.quan_phuong = json.load(open(os.path.join(dir_path, 'px', 'quan_phuong.json')))
    #add_dicts.quan_thitran = json.load(open(os.path.join(dir_path, 'px', 'quan_thitran.json')))
    #add_dicts.quan_xa = json.load(open(os.path.join(dir_path, 'px', 'quan_xa.json')))
    add_dicts.tp_phuong = json.load(open(os.path.join(dir_path, 'px', 'tp_phuong.json')))
    #add_dicts.tp_thitran = json.load(open(os.path.join(dir_path, 'px', 'tp_thitran.json')))
    add_dicts.tp_xa = json.load(open(os.path.join(dir_path, 'px', 'tp_xa.json')))
    add_dicts.tx_phuong = json.load(open(os.path.join(dir_path, 'px', 'tx_phuong.json')))
    #add_dicts.tx_thitran = json.load(open(os.path.join(dir_path, 'px', 'tx_thitran.json')))
    add_dicts.tx_xa = json.load(open(os.path.join(dir_path, 'px', 'tx_xa.json')))

    # tinh_huyen
    add_dicts.thanhpho_huyen = json.load(open(os.path.join(dir_path, 'qh', 'thanhpho_huyen.json')))
    #add_dicts.thanhpho_tp = json.load(open(os.path.join(dir_path, 'qh', 'thanhpho_tp.json')))
    add_dicts.thanhpho_quan = json.load(open(os.path.join(dir_path, 'qh', 'thanhpho_quan.json')))
    add_dicts.tinh_huyen = json.load(open(os.path.join(dir_path, 'qh', 'tinh_huyen.json')))
    #add_dicts.tinh_quan = json.load(open(os.path.join(dir_path, 'qh', 'tinh_quan.json')))
    add_dicts.tinh_tp = json.load(open(os.path.join(dir_path, 'qh', 'tinh_tp.json')))
    add_dicts.tinh_tx = json.load(open(os.path.join(dir_path, 'qh', 'tinh_tx.json')))

    # HCMHN
    add_dicts.hcm_hn_huyen = json.load(open(os.path.join(dir_path, 'hcmhn', 'hcmhn_huyen.json')))
    add_dicts.hcm_hn_quan = json.load(open(os.path.join(dir_path, 'hcmhn', 'hcmhn_quan.json')))
    add_dicts.hcm_hn_tx = json.load(open(os.path.join(dir_path, 'hcmhn', 'hcmhn_tx.json')))
    add_dicts.hcm_hn_tp = json.load(open(os.path.join(dir_path, 'hcmhn', 'hcmhn_tp.json')))

    # qh_duong
    #add_dicts.qh_d = json.load(open(os.path.join(dir_path, 'qh_duong.json')))
    add_dicts.chuanhoa = pd.read_csv(os.path.join(dir_path, 'chuanhoa.csv'), header=None)
    # return huyen_phuong, huyen_thitran, huyen_xa, quan_phuong, quan_thitran, quan_xa, tp_phuong,\
    #        tp_xa, tx_phuong, tx_xa, thanhpho_huyen, thanhpho_quan, thanhpho_tx, tinh_huyen_qh,\
    #        tinh_quan, tinh_tp, tinh_tx, hcm_hn_huyen, hcm_hn_quan, hcm_hn_tx, qh_d, chuanhoa
    return add_dicts


def city_district(data, dict_data, text1, text2):

    # Tim thành phố/tỉnh - huyện/quận/thị xã/thành phố
    for key, values in dict_data.items():
        # key = key +' ' không có trường hợp bắt sai tên tỉnh vd vinhome không bắt vinh
        # kiem tra ten tinh
        if (key + ' ') in (data['Address_ch'][-16:] + ' '):
            if data['t_check'] != 1:
                data['t_check'] = 1
                data['tinh'] = key
                data['tinh_cat'] = text1
                data['Address_ch'] = data['Address_ch'].replace(key, '')

        for value in values:
            #print(value)
            # if len(value) == 1:
            #     value = values
            #print("data: ", (str(data['Address_ch'][-18:]) + ' '))
            if (value + ' ') in (str(data['Address_ch'][-18:]) + ' '):
                if data['h_check'] != 1:
                    data['qh'] = value
                    data['qh_cat'] = text2
                    data['h_check'] = 1
                    data['Address_ch'] = data['Address_ch'].replace(value, '')
                #neu khong co tinh thi fill tinh trong truong hop tim thay huyen/quan
                if data['t_check'] != 1:
                    data['tinh'] = key
                    data['tinh_cat'] = text1
                    data['t_check'] = 1
                    data['Address_ch'] = data['Address_ch'].replace(key, '')
    return data


def district_ward(data, dict_data, text1):
    # kiem tra co phường/xã/thị trấn khong

    if data['h_check'] == 1:
        for key_1, values_1 in dict_data.items():
            if data['qh'] == key_1:
                for value_1 in values_1:
                    # if len(value_1) == 1:
                    #     value_1 = values_1
                    #print(value_1, data['Address_ch'])
                    if (' ' + value_1 + ' ') in (data['Address_ch'] + ' '):
                        data['Address_ch'] = data['Address_ch'].replace(value_1, '')
                        data['px'] = value_1
                        data['px_cat'] = text1
                    # elif (value_1 + ' ') in (data['Address_ch'] + ' '):
                    #     data['Address_ch'] = data['Address_ch'].replace(value_1, '')
                    #     data['px'] = value_1
                    #     data['px_cat'] = text1
    return data


def district_street(data, dict_data):
    # kiem tra co duong khong
    if data['h_check'] == 1:
        for key_2, values_2 in dict_data.items():
            if data['qh'] == key_2:
                for value_2 in values_2:
                    # if value_2 == 1:
                    #     value_2 = values_2
                    if (value_2 + ' ') in (data['Address_ch'] + ' '):
                        data['Address_ch'] = data['Address_ch'].replace(value_2, '')
                        data['duong'] = value_2
    return data


def add_norm(data, chuanhoa):
    # Chuẩn hóa các từ viết tắt thông dụng trong data
    for j in range(len(chuanhoa)):
        if str(chuanhoa[0][j] + ' ') in (data['Address_ch'] + ' '):
            data['Address_ch'] = data['Address_ch'].replace(chuanhoa[0][j], chuanhoa[1][j])
        data['Address_ch'] = data['Address_ch'].replace(',', '')
    return data


def add_proc_1(data, add_dicts):
    # extract
    city_district(data, add_dicts.hcm_hn_huyen, 'thành phố', 'huyện')
    city_district(data, add_dicts.hcm_hn_quan, 'thành phố', 'quận')
    city_district(data, add_dicts.hcm_hn_tx, 'thành phố', 'thị xã')
    city_district(data, add_dicts.hcm_hn_tp, 'thành phố', 'thành phố')  # ---------------update: them
    #district_ward(data, add_dicts.huyen_phuong, 'phường')
    district_ward(data, add_dicts.huyen_thitran, 'thị trấn')
    district_ward(data, add_dicts.huyen_xa, 'xã')
    district_ward(data, add_dicts.quan_phuong, 'phường')
    #district_ward(data, add_dicts.quan_thitran, 'thị trấn')
    #district_ward(data, add_dicts.quan_xa, 'xã')
    district_ward(data, add_dicts.tp_phuong, 'phường')
    #district_ward(data, add_dicts.tp_thitran, 'thị trấn')  # ---------------update: them
    district_ward(data, add_dicts.tp_xa, 'xã')
    district_ward(data, add_dicts.tx_phuong, 'phường')
    #district_ward(data, add_dicts.tx_thitran, 'thị trấn')  # ---------------update: them
    district_ward(data, add_dicts.tx_xa, 'xã')
    #district_street(data, add_dicts.qh_d)
    return data


def add_proc_2(data, add_dicts):
    # TinhHuyen-----ssssssssssssssss
    if data['t_check'] != 1:

        city_district(data, add_dicts.tinh_huyen, 'tỉnh', 'huyện')
        city_district(data, add_dicts.tinh_tp, 'tỉnh', 'thành phố')
        city_district(data, add_dicts.tinh_tx, 'tỉnh', 'thị xã')
        city_district(data, add_dicts.thanhpho_huyen, 'thành phố', 'huyện')
        city_district(data, add_dicts.thanhpho_quan, 'thành phố', 'quận')

        district_ward(data, add_dicts.huyen_thitran, 'thị trấn')
        district_ward(data, add_dicts.huyen_xa, 'xã')
        district_ward(data, add_dicts.quan_phuong, 'phường')
        #district_ward(data, add_dicts.quan_thitran, 'thị trấn')
        #district_ward(data, add_dicts.quan_xa, 'xã')
        district_ward(data, add_dicts.tp_phuong, 'phường')
        #district_ward(data, add_dicts.tp_thitran, 'thị trấn')  # ---------------update: them
        district_ward(data, add_dicts.tp_xa, 'xã')
        district_ward(data, add_dicts.tx_phuong, 'phường')
        #district_ward(data, add_dicts.tx_thitran, 'thị trấn')  # ---------------update: them
        district_ward(data, add_dicts.tx_xa, 'xã')
        #district_street(data, add_dicts.qh_d)
    return data


def add_proc_3(data):
    list_xuly = ['mặt đường', "đường lớn", 'thị xã', "thị trấn", 'thành phố', "đường", '-', '( )', 'tt', "trung tâm",
                 "phường", "huyện", "tỉnh", "tx", "tp", "quận", "xã", "quận"]
    if not data['tinh'] is None:
        for j in list_xuly:
            if j in data['Address_ch']:
                data['Address_ch'] = data['Address_ch'].replace(j, "")
        data['Address_ch'] = re.sub("\s\s+", " ", data['Address_ch'])
    return data


def update_entity_address(entity_dict, add_dicts):
    add_name_dict_keys = ['tinh', 'tinh_cat', 'qh', 'qh_cat', 'px', 'px_cat', 'duong', 'Address_ch',
                          't_check', 'h_check']
    #add_name_dict = dict.fromkeys(add_name_dict_keys)

    data = dict.fromkeys(add_name_dict_keys)
    # for ent_name in add_name_dict_keys: data[ent_name] = []
    try: 
        long_add = entity_dict['address'][0]
    except:
        long_add = entity_dict[0]

    data['Address_ch'] = long_add.lower().replace("_", " ")

    data = add_norm(data, add_dicts.chuanhoa)

    data = add_proc_1(data, add_dicts)
 
    data = add_proc_2(data, add_dicts)

    data = add_proc_3(data)

    try:
        for ent_name in add_name_dict_keys: entity_dict[ent_name] = []
        for ent_name in add_name_dict_keys: 
            entity_dict[ent_name].append(data[ent_name])
    except: #for the case of entity_dict is a list
        return data

    # add_name_dict['Address_ch'] = data['Address_ch']
    # add_name_dict['tinh_cat'] = data['tinh_cat']
    # add_name_dict['tinh'] = data['tinh']
    # add_name_dict['qh_cat'] = data['qh_cat']
    # add_name_dict['qh'] = data['qh']
    # add_name_dict['px_cat'] = data['px_cat']
    # add_name_dict['px'] = data['px']
    #add_name_dict['duong'] = 'address (Đường)'
    return entity_dict


