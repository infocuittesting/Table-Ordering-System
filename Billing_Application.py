from sqlwrapper import *
from Fetch_Current_Datetime import *
def Query_Table_Status(request):
    get_table_details = json.loads(dbget("select login_status.login_status,payment_type.*,table_status.table_status, table_details.* from table_details\
	left join table_status on table_status.table_status_id = table_details.table_status_id\
	left join login_status on login_status.login_status_id = table_details.login_status_id\
	left join payment_type on payment_type.payment_type_id = table_details.payment_type_id order by table_no"))
    available_count = len(list(filter(lambda i: i['table_status'] == 'AVAILABLE', get_table_details)))
    unavailable_count =len(list(filter(lambda i: i['table_status'] == 'UN AVAILABLE', get_table_details)))
    payment_count = len(list(filter(lambda i: i['payment_type'] != 'NOPE', get_table_details)))
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS",
                       "Available_count":available_count,"unavailable_count":unavailable_count,"payment_count":payment_count,"Returnvalue":get_table_details,"Status": "Success","StatusCode": "200"},indent = 4)

def Update_Food_Order_Status_Item(request):
    d = request.json

    dbput("update food_order set order_status_id = '"+str(d['order_status_id'])+"' where order_details_id = '"+str(d['order_details_id'])+"'")
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

def Update_Order_Status(request):
    
    
   d = request.json
   
   s = {'order_status_id' : 6}
   gensql('update','food_order',s,d)
   return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

   
def Update_ReadyforPayment_Status(request):
    
   
    d = request.json
    e={"table_no":d['table_no']}
    s = {'table_status_id' : 3,'payment_type_id':d['payment_type_id']}
    
    gensql('update','table_details',s,e)
    dbput("update order_timings set bill_request_time = '"+str(application_datetime())+"' where order_no = '"+str(d['order_no'])+"'")
    
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)


def Update_Table_Available_Status(request):
    
   d = request.json
   s = {'table_status_id' : 1,'payment_type_id':3}
   z = {'table_no':d['table_no']}
   gensql('update','table_details',s,z)

   e = {'order_status_id':7}
   gensql('update','food_order',e,d)
   dbput("update order_timings set close_time = '"+str(application_datetime())+"' where order_no = '"+str(d['order_no'])+"'")
    
   return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

def Get_Order_Item_Table(request):
    
   d = request.json

   get_orders=json.loads(dbget("select food_type.*, \
   order_status.order_status_desc,food_menu.food_name,food_menu.offer_value,food_menu.price, \
   food_category.category, food_order.* from food_order\
    left join food_menu on food_menu.food_id = food_order.food_id \
    left join food_category on food_category.category_id =food_menu.item_category_id \
    left join order_status on order_status.order_status_id = food_order.order_status_id \
    left join food_type on food_type.food_type_id = food_menu.food_type_id \
    where food_order.table_no = '"+str(d['table_no'])+"' and food_order.order_status_id != 7 \
    and food_menu.item_category_id!=7 order by datetime"))

   total_amount = json.loads(dbget("select sum((food_menu.price*quantity)-(food_menu.offer_value*food_order.quantity)) as total from food_order \
                                   left join food_menu on food_menu.food_id = food_order.food_id \
                                   and food_order.order_status_id != 7 \
                                   and food_menu.item_category_id!=7 \
                                   where food_order.table_no =  '"+str(d['table_no'])+"'"))
   print(total_amount)
   if len(get_orders) != 0 :
    food_menu_details = {"table_no":d['table_no'],"order_no":get_orders[0]['order_no'],
                         "items":get_orders,'total_amount':"{0:.2f}".format(total_amount[0]['total'])}

   else:
    food_menu_details = {"table_no":d['table_no'],"order_no":0,
                         "items":get_orders,'total_amount':0}

   return(json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS",
                      "Returnvalue":food_menu_details,"Status": "Success","StatusCode": "200"},indent = 4))  
def Update_Category_Food_Menus(request):
    
  d = request.json
  dbput("update food_menu set food_status_id = '"+str(d['food_status_id'])+"' where item_category_id = '"+str(d['item_category_id'])+"'")
  return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)


def Send_Alert_to_waiter_food_items_closed(request):
    d = request.json
    return json.dumps({"Table_no":d['table_no'],"Description": "Food Items Completed","Status": "Success","StatusCode": "200"},indent = 4)

