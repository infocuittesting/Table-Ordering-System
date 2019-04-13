from sqlwrapper import *
from Fetch_Current_Datetime import *
from collections import defaultdict
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
    try:

        dbput("update food_order set order_status_id = '"+str(d['order_status_id'])+"' where order_details_id = '"+str(d['order_details_id'])+"'")
        return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)
    except:
        return json.dumps({"Return":"Wrong Value Error","ReturnCode":"WVE"})
def Update_Order_Status(request):
    
    
   d = request.json
   
   s = {'order_status_id' : 6}
   gensql('update','food_order',s,d)
   return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)

   
def Update_ReadyforPayment_Status(request):
    
   
    d = request.json
    try:
        e={"table_no":d['table_no']}
        s = {'table_status_id' : 3,'payment_type_id':d['payment_type_id']}
        
        gensql('update','table_details',s,e)
        get_order_no = json.loads(dbget("select order_no from food_order where order_status_id != 7 and table_no = '"+str(d['table_no'])+"' "))
        dbput("update order_timings set bill_request_time = '"+str(application_datetime())+"' where order_no = '"+str(get_order_no[0]['order_no'])+"'")
        
        return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)
    except:
        
     return json.dumps({"Return":"Wrong Value Error","ReturnCode":"WVE"})
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

   
   #print(total_amount)
   c = defaultdict(int)
   for d in get_orders:
    #print(c)
    c[d['food_name']] += (d['price']*d['quantity'])
    #c[d['food_name']] += d['quantity']
   #print(c)
   finals = [{'food_name': food_name, 'total_price': price} for food_name, price in c.items()]

   #print(finals)

   z = defaultdict(int)
   for s in get_orders:
     z[s['food_name']] += s['quantity']
   finals_value = [{'Names': food_name, 'quantity': quantity} for food_name, quantity in z.items()]
   for final in finals:
    for finals_va in finals_value:
        if final['food_name'] == finals_va['Names']:
            final['quantity'] = finals_va['quantity']
   

   #finals = [ dict(final,price = x['price'])    for x in get_orders  for final in finals if final['food_name'] == x['food_name'] ]
   if len(get_orders) != 0 :
    sub_total = sum([x['total_price'] for x in finals])
    offer_value = sum([x['offer_value']*x['quantity'] for x in get_orders])
    food_menu_details = {"table_no":d['table_no'],"order_no":get_orders[0]['order_no'],
                         "items":finals,'grand_total':"{0:.2f}".format((sub_total+((sub_total*12)/100)-offer_value)),
                         "GST_Amount":"{0:.2f}".format((sub_total*12)/100),"total_items":len(finals),"sub_total":sub_total,"total_offers":offer_value}

   else:
    food_menu_details = {"table_no":d['table_no'],"order_no":0,
                         "items":get_orders,'total_amount':0,"total_items":0,"sub_total":0,"total_offers":0,"GST_Amount":0,"grand_total":0}

   return(json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS",
                      "Returnvalue":food_menu_details,"Status": "Success","StatusCode": "200"},indent = 4))  
def Update_Notification_Status(request):
    d = request.json
    #values = ','.join("'{0}'".format(x) for x in d['order_details_id'])
    values = ', '.join(map(str, d['order_details_id']))
    print(values)
    if d['notification_status_id'] == 2:
        
        dbput("update food_order set notification_status_id='"+str(d['notification_status_id'])+"',\
              notification_time='"+str(application_datetime().strftime("%Y-%m-%d %H:%M:%S"))+"' where order_details_id in ("+values+")")
    else:
      dbput("update food_order set notification_status_id='"+str(d['notification_status_id'])+"' where order_details_id in ("+values+")")
    return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)
def Query_Notification_Food_Items(request):
    notify_time,final_results,table_no = [],[],[]
    get_notifications = json.loads(dbget("select notification_status,notification_time, food_order.*,food_menu.food_name from food_order\
	left join food_menu on food_menu.food_id =food_order.food_id \
	left join notification_status on notification_status.notification_status_id = food_order.notification_status_id\
	where order_status_id =6 and food_order.notification_status_id  =2\
	order by food_order.notification_time"))
    for get_notification in get_notifications:
          if get_notification['notification_time'] not in notify_time:
             notify_time.append(get_notification['notification_time'])
             final_results.append({"notification_time":get_notification['notification_time'],"table_records":[]})
     
    for get_notification in get_notifications:
        for final_result in final_results:
         if get_notification['notification_time'] == final_result['notification_time']:
           if not any(d['table_no'] == get_notification['table_no'] for d in final_result['table_records']):
             final_result['table_records'].append({"table_no":get_notification['table_no'],"items":[]})
             
    for get_notification in get_notifications:
       for final_result in final_results:

               if get_notification['notification_time'] == final_result['notification_time']:
                 for d in final_result['table_records']:
                  if   d['table_no'] == get_notification['table_no']:
                      d['items'].append(get_notification)
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":final_results,"Status": "Success","StatusCode": "200"},indent = 4)
