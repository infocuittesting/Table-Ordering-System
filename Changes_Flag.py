from sqlwrapper import *
import json

def Get_FoodMenu_Flag(reqeust):
    d = reqeust.json
    return json.dumps({"Return": "Record Retrived Successfully", "ReturnCode": "RRS",
                       "Changes_Flage": json.loads(dbget("select disp_fm_flag as d from table_details \
                                        where table_no='"+str(d['table_no'])+"'"))[0]['d'],
                       "Status": "Success", "StatusCode": "200"}, indent=4)

def Get_TableStatus_Flag(reqeust):

    return json.dumps({"Return": "Record Retrived Successfully", "ReturnCode": "RRS",
                       "Changes_Flage": json.loads(dbget("select tablestatus_flag as d "
                                                         "from resturants"))[0]['d'],
                       "Status": "Success", "StatusCode": "200"}, indent=4)

def Update_TableStatus_Flag(reqeust):
    dbput("update resturants set tablestatus_flag=1")
    return json.dumps(
        {"Return": "Record Updated Successfully", "ReturnCode": "RUS", "Status": "Success",
         "StatusCode": "200"},indent=4)

def Get_Allkot_Flag(reqeust):
    d = reqeust.json
    return json.dumps({"Return": "Record Retrived Successfully", "ReturnCode": "RRS",
                       "Changes_Flage": json.loads(dbget("select * from users where \
                        user_name='"+d['user_name']+"'")),
                       "Status": "Success", "StatusCode": "200"}, indent=4)

def Update_Allkot_Flag(reqeust):
    d = reqeust.json
    j = {k:v for k,v in d.items() if k in ('user_name')}
    i = {k:v for k,v in d.items() if k not in ('user_name') if v != ""}
    gensql('update','users',i,j)
    return json.dumps(
        {"Return": "Record Updated Successfully", "ReturnCode": "RUS", "Status": "Success",
         "StatusCode": "200"},indent=4)
