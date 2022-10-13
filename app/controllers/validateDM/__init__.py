import sys, os
from .geneDatamart import geneDatamart

datamartSchemaSelect={
    "geneDatamart": geneDatamart
}

class validateDM:
    
    def __init__(self,datamart_name,data):
        self.schema = datamartSchemaSelect[datamart_name]
        self.data = data
    
    def get_validateData(self):
        validateData = {}
        try:
            validateData = self.check(self.schema,self.data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        return validateData
    
    def check(self,schema_obj,data_obj):
        validateData = {}
        try:
            for key in schema_obj:
                if key in data_obj:
                    if schema_obj[key] == type(data_obj[key]):
                        validateData[key] = data_obj[key]
                    elif data_obj[key] == None:
                        validateData[key] = self.completeSchema(schema_obj[key])  
                    elif type(schema_obj[key]) == list:
                        if len(data_obj[key]) == 0:
                            validateData[key] = self.completeSchema(schema_obj[key])                            
                        sObj = schema_obj[key][0]
                        validateData[key] = []
                        for item in data_obj[key]:
                            if sObj == type(item):
                                validateData[key].append(item)
                            else:
                                validateData[key].append(self.check(sObj,item))
                    elif type(schema_obj[key]) == dict:
                        validateData[key] = self.check(schema_obj[key],data_obj[key])
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, fname, exc_tb.tb_lineno)
        return validateData
    
    def completeSchema(self,schema):
        value = None
        if type(schema) == list:
            value = []
            if len(schema) > 0:
                if type(schema[0]) == dict or type(schema[0]) == list:
                    value.append(self.completeSchema(schema[0]))
        elif type(schema) == dict:
            if len(schema) == 0:
                value = {}
            else:
                value = {}
                for key in schema:
                    value[key] = self.completeSchema(schema[key])
        return value
                