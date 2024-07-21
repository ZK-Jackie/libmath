import pandas as pd


def read_data(file_path, sheet_names=None):
    xls = pd.ExcelFile(file_path)
    data = None
    if file_path.endswith('.xlsx'):
        dfs = [pd.read_excel(xls, sheet_name=sheet) for sheet in sheet_names]
        data = pd.concat(dfs, ignore_index=True)
    elif file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    else:
        raise ValueError("File format not supported")
    return data


def pre_process_daily(data_frame):
    day_cnt = 0
    acc_qm = 0
    acc_qms = 0
    ret_frame = pd.DataFrame(columns=['日期', '流量', '含沙量', '水沙通量'])
    ret_frame = ret_frame.dropna(axis=1, how='all')
    # 1. 以月份为单位，算每个月的流量、含沙量平均值
    for i in range(0, len(data_frame)):
        if i == 0:
            acc_qm = data_frame['流量'][i]
            acc_qms = data_frame['含沙量'][i]
            day_cnt = 1
        else:
            if data_frame['日'][i] == data_frame['日'][i - 1]:
                acc_qm += data_frame['流量'][i]
                if not pd.isna(data_frame['含沙量'][i]):
                    acc_qms += data_frame['含沙量'][i]
                day_cnt += 1
            else:
                ret_frame = pd.concat([ret_frame,
                                       pd.DataFrame([[str.format('{0}-{1}-{2}', data_frame['年'][i - 1],
                                                                 data_frame['月'][i - 1], data_frame['日'][i - 1]),
                                                      acc_qm / day_cnt,
                                                      acc_qms / day_cnt,
                                                      (acc_qm / day_cnt) * (acc_qms / day_cnt)]],
                                                    columns=['日期', '流量', '含沙量', '水沙通量'],
                                                    index=[len(ret_frame)]
                                                    )])
                acc_qm = data_frame['流量'][i]
                acc_qms = data_frame['含沙量'][i]
                day_cnt = 1
    # 2. 最后一天收尾
    ret_frame = pd.concat([ret_frame,
                           pd.DataFrame([[str.format('{0}-{1}-{2}', data_frame['年'][i],
                                                     data_frame['月'][i], data_frame['日'][i]),
                                          acc_qm / day_cnt,
                                          acc_qms / day_cnt,
                                          (acc_qm / day_cnt) * (acc_qms / day_cnt)]],
                                        columns=['日期', '流量', '含沙量', '水沙通量'],
                                        index=[len(ret_frame)]
                                        )])
    return ret_frame


def pre_process_monthly(data_frame):
    month_cnt = 0
    acc_qm = 0
    acc_qms = 0
    acc_cnt = 0
    ret_frame = pd.DataFrame(columns=['日期', '流量', '含沙量', '水沙通量'])
    ret_frame = ret_frame.dropna(axis=1, how='all')
    # 1. 以月份为单位，算每个月的流量、含沙量平均值
    for i in range(0, len(data_frame)):
        if i == 0:
            acc_qm = data_frame['流量'][i]
            acc_qms = data_frame['含沙量'][i]
            acc_cnt = 1
        else:
            if data_frame['月'][i] == data_frame['月'][i - 1]:
                acc_qm += data_frame['流量'][i]
                if not pd.isna(data_frame['含沙量'][i]):
                    acc_qms += data_frame['含沙量'][i]
                acc_cnt += 1
            else:
                ret_frame = pd.concat([ret_frame,
                                       pd.DataFrame([[str.format('{0}-{1}', data_frame['年'][i - 1],
                                                                 data_frame['月'][i - 1]),
                                                      acc_qm / acc_cnt,
                                                      acc_qms / acc_cnt,
                                                      (acc_qm / acc_cnt) * (acc_qms / acc_cnt)]],
                                                    columns=['日期', '流量', '含沙量', '水沙通量'],
                                                    index=[len(ret_frame)]
                                                    )])
                acc_qm = data_frame['流量'][i]
                acc_qms = data_frame['含沙量'][i]
                acc_cnt = 1
                month_cnt += 1
    # 2. 最后一个月收尾
    ret_frame = pd.concat([ret_frame,
                           pd.DataFrame([[str.format('{0}-{1}', data_frame['年'][i],
                                                     data_frame['月'][i]),
                                          acc_qm / acc_cnt,
                                          acc_qms / acc_cnt,
                                          (acc_qm / acc_cnt) * (acc_qms / acc_cnt)]],
                                        columns=['日期', '流量', '含沙量', '水沙通量'],
                                        index=[len(ret_frame)]
                                        )])
    return ret_frame
