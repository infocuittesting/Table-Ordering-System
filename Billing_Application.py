from sqlwrapper import *

def Query_Table_Status(request):
    get_table_details = json.loads(dbget("select login_status.login_status,table_status.table_status, table_details.* from table_details\
	left join table_status on table_status.table_status_id = table_details.table_status_id\
	left join login_status on login_status.login_status_id = table_details.login_status_id "))
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":get_table_details,"Status": "Success","StatusCode": "200"},indent = 4)

def Update_Food_Order_Status_Item(request):
    d = request.json
    s = {'order_status_id' : 6}
    gensql('update','food_order',s,d)
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

def Update_Order_Status(request):
    
    
   d = request.json
   
   s = {'order_status_id' : 6}
   gensql('update','food_order',s,d)
   return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

   
def Update_ReadyforPayment_Status(request):
    
   
    d = request.json
    s = {'table_status_id' : 3}
    gensql('update','table_details',s,d)
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)


def Update_Table_Available_Status(request):
    
   d = request.json
   s = {'table_status_id' : 1}
   z = {'table_no':d['table_no']}
   gensql('update','table_details',s,z)

   e = {'order_status_id':7}
   gensql('update','food_order',e,d)
   
   return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

def Get_Order_Item_Table(request):
    d = request.json
    food_menu_details,food_details = [],[]
    get_orders=json.loads(dbget("select food_offers.*,offer_type.offer_type,offer_status.offer_status,order_status.order_status_desc,food_menu.food_name,food_menu.price,food_category.category, food_order.* from food_order\
	left join food_menu on food_menu.food_id = food_order.food_id \
	left join food_category on food_category.category_id =food_menu.item_category_id \
	left join order_status on order_status.order_status_id = food_order.order_status_id \
	left join food_offers on food_offers.food_id = food_order.food_id \
	left join offer_type on offer_type.offer_type_id = food_offers.offer_type_id \
	left join offer_status on offer_status.offer_status_id = food_offers.offer_status_id where food_order.table_no = '"+str(d['table_no'])+"' and food_order.order_status_id != 7  order by datetime"))
    
    if len(get_orders) != 0 :
     food_menu_details.append({"table_no":d['table_no'],"order_no":get_orders[0]['order_no'],"items":[]})
    else:
        pass
    for get_order in get_orders:
        for food_menu_detail in food_menu_details:
            
             if get_order['table_no'] ==food_menu_detail['table_no']:
                
                food_menu_detail["items"].append(get_order)
             food_menu_detail['total_amount'] = sum(item['price'] for item in food_menu_detail['items'])
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":food_menu_details,"Status": "Success","StatusCode": "200"},indent = 4)

    
