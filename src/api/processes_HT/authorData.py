from io import StringIO
import csv
import re


def formatData_to_json_author_table(authorsData):
    json_author_table = {
        'comments': [],
        'columns': [],
        'data': []
    }
    file = StringIO(""+authorsData)
    reader = csv.reader(file, delimiter=',')
    author_data = []
    # search comments
    for row in reader:
        if re.search("^#", row[0]):
            json_author_table['comments'].append("".join(row))
        else:
            author_data.append(row)
    columns = []
    for index in range(len(author_data)):
        row = author_data[index]
        if index == 0:
            cc = 0
            for cell in row:
                columns.append(""+str(cc)+"_"+cell.replace(" ", "_").casefold())
                json_author_table['columns'].append({
                    'Header': ""+cell,
                    'accessor': ""+str(cc)+"_"+cell.replace(" ", "_").casefold()
                })
                cc += 1
        else:
            data = {}
            for i in range(len(row)):
                data[columns[i]] = row[i]
            json_author_table['data'].append(data)
    return json_author_table
