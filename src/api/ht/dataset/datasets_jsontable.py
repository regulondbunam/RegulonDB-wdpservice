from .introspection import Dataset


def dataset_jsontable(datasets):
    # Make Columns!
    columns = []
    for key in Dataset:
        column = False
        if type(Dataset[key]) is list:
            column = proses_head_list(key, Dataset[key])
        elif type(Dataset[key]) is dict:
            column = proses_head_dict(key, Dataset[key])
        else:
            column = {
                'Header': key,
                'accessor': key
            }
        if column:
            columns.append(column)
        # print(column)
    # print(columns)
    data = []
    for dataset in datasets:
        row = {}
        for key in dataset:
            if type(dataset[key]) is str:
                row[key] = dataset[key]
            elif type(dataset[key]) is list:
                if len(dataset[key]) > 0:
                    row = {**row, **proses_data_list(key, dataset[key])}
            elif type(dataset[key]) is dict:
                if len(dataset[key]) > 0:
                    row = {**row, **proses_data_dict(key, dataset[key])}
        if len(row) > 0:
            data.append(row)
    return {
        "columns": columns,
        "data": data,
    }


def proses_data_list(key, data_list):
    row = {}
    for dt in data_list:
        try:
            if type(dt) is str:
                row[key] = dt
            elif type(dt) is list:
                row = {**row, **proses_data_list(key, dt)}
            elif type(dt) is dict:
                row = proses_dict(proses_data_dict(key, dt), row)
        except Exception as e:
            print("error prosses data list: "+str(e)+" on dt: "+str(dt))
    return row


def proses_dict(d_a, d_b):
    row = {}
    for key in d_a:
        try:
            if key in d_b.keys():
                dt_a = d_a[key]
                dt_b = d_b[key]
                if type(dt_b) is type(dt_a):
                    if type(dt_b) is str:
                        row[key] = d_a[key]+", "+d_b[key]
                    elif type(dt_b) is list:
                        print("unsupported list add list")
                    elif type(dt_b) is dict:
                        print("unsupported dict add dict")
            else:
                row[key] = d_a[key]
        except Exception as e:
            print("error prosses data list: "+str(e))
    for key in d_b:
        if key not in d_a.keys():
            row[key] = d_b[key]
    return row



def proses_data_dict(key, data_dict):
    row = {}
    for sub_key in data_dict:
        try:
            dt = data_dict[sub_key]
            nw_key = key + '_' + sub_key
            if type(dt) is str:
                row[nw_key] = dt
            elif type(dt) is list:
                if len(dt) > 0:
                    row = {**row, **proses_data_list(nw_key, dt)}
            elif type(dt) is dict:
                row = {**row, **proses_data_dict(nw_key, dt)}
        except Exception as e:
            print("prosses data dict"+str(e)+" on kay: "+str(sub_key))
    return row


def proses_head_list(key, data_list):
    columns = []
    for subcolumn in data_list[0]:
        if data_list[0][subcolumn] is str:
            columns.append({
                'Header': subcolumn,
                'accessor': key+"_"+subcolumn
            })
        elif data_list[0][subcolumn] is int:
            columns.append({
                'Header': subcolumn,
                'accessor': key + "_" + subcolumn
            })
        elif data_list[0][subcolumn] is list:
            columns.append({
                'Header': subcolumn,
                'columns': proses_head_list(subcolumn, data_list[0][subcolumn])
            })
        elif data_list[0][subcolumn] is dict:
            columns.append({
                'Header': subcolumn,
                'columns': proses_head_dict(subcolumn, data_list[0][subcolumn])
            })
    return {
        'Header': key,
        'columns': columns
    }


def proses_head_dict(key, data):
    columns = []
    for subcolumn in data:
        # print(key+"_" + subcolumn)
        # print(data[column])
        if data[subcolumn] is str:
            columns.append({
                "Header": subcolumn,
                'accessor': key+"_"+subcolumn
            })
        elif data[subcolumn] is int:
            columns.append({
                'Header': subcolumn,
                'accessor': key + "_" + subcolumn
            })
        elif data[subcolumn] is list:
            columns.append({
                'Header': subcolumn,
                'columns': proses_head_list(subcolumn, data[subcolumn])
            })
        elif data[subcolumn] is dict:
            columns.append({
                'Header': subcolumn,
                'columns': proses_head_dict(subcolumn, data[subcolumn])
            })
    return {
        'Header': key,
        'columns': columns
    }
