
from sqlwrapper import  *
from Fetch_Current_Datetime import *
import time
def Place_Order(request):
    
    d = request.json
    #print(d)
    z = {k:v for k,v in d.items() if v != '' if k in ('cus_name','cus_mobile')}
    d = {k:v for k,v in d.items()if k not in ('cus_name','cus_mobile')}
    items_value = d['items']
    list1,list2 = [],[]
    check_item = ""
    if len(items_value) == 0:
        return json.dumps({"Return":"No Items Selected","Returncode":"NIS"},indent=2)
    else:
        for item_va in items_value:
            if len(check_item) ==0:
               check_item = "'"+item_va['food_id']+"'"
               list2.append(check_item)
             
            else:
                check_item +=","+ "'"+item_va['food_id']+"'"
                list2.append(check_item)
             
        get_table_status = json.loads(dbget("select table_status_id from table_details where table_no="+str(d['table_no'])+""))
        if get_table_status[0]['table_status_id'] != 3:
            
            get_item_status = json.loads(dbget("select count(*) from food_menu where food_id in ("+str(check_item)+") and food_status_id = 1"))
            if get_item_status[0]['count'] == len(list2):
                orders = json.loads(dbget("select order_no from food_order where table_no="+str(d['table_no'])+" and order_status_id !=7"))
                print(orders)
                
                order_no = json.loads(dbget("select uuid_generate_v4() as order_no"))[0]['order_no'] if len(orders) == 0 else orders[0]['order_no']
                print(order_no)
                
                for item in items_value:
                    list1.append(tuple((order_no,d['table_no'],item['food_id'],item['quantity'],item['order_status_id'],str(application_datetime().strftime("%Y-%m-%d %H:%M:%S")),3)))
                    #item.update({'order_no':order_no,'notification_status_id':3,'datetime':application_datetime(),'table_no':d['table_no']})
                    #get_items = json.loads(dbget("select food_status_id,food_name from food_menu where food_id = '"+str(item['food_id'])+"' "))
                    #if get_items[0]['food_status_id'] == 1:
                     #  gensql('insert','food_order',item)
                    #else:
                     #   unavailable_item.append({"food_name":get_items[0]['food_name'],"food_id":item['food_id']})
                values = ', '.join(map(str, list1))
                dbput("INSERT INTO  food_order (order_no, table_no, food_id, quantity, order_status_id, datetime, notification_status_id)VALUES {}".format(values))
                       
                try:
                    maintain_time = {"order_no":order_no,"order_time":application_datetime(),"table_no":str(d['table_no'])}
                    gensql('insert','order_timings',maintain_time)
                    z.update({"order_no":order_no,"table_no":str(d['table_no'])})
                    gensql('insert','feedback',z)
                except:
                    pass
                
                if len(d['comments'])!=0:
                    order_comments = {'order_no':order_no,'order_comments':d['comments'],'comments_time':application_datetime()}
                   
                    gensql('insert','order_comments',order_comments)
                else:
                    pass
                dbput("update table_details set table_status_id = '2' where table_no = "+str(d['table_no'])+"")
                
                return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
            else:
              return json.dumps({"Return": "Items Not Avialble","ReturnCode": "INA","Status": "Success","StatusCode": "200"},indent = 4)
        else:
           return json.dumps({"Return": "Coudn't Place Order","ReturnCode": "CNPO","Status": "Success","StatusCode": "200"},indent = 4)
     
def Query_today_food_orders(request):
   st_time = time.time()
   today_orders = json.loads(dbget("select food_menu.food_name,food_category.*, food_order.*,\
                                  order_status.order_status_desc,notification_status.* from food_order\
                                   left join food_menu on food_menu.food_id = food_order.food_id\
                                   left join food_category on food_category.category_id =food_menu.item_category_id\
                                   left join order_status on order_status.order_status_id = \
                                   food_order.order_status_id join notification_status on\
                                   food_order.notification_status_id = notification_status.notification_status_id \
                                   where food_order.order_status_id!=7 and food_menu.item_category_id!=7 \
                                   order by datetime"))
   #print(today_orders)
   tables = list(set(order['table_no'] for order in today_orders))
   print("tables", tables)
   total_orders = []
   for table in tables:
       all_category = []
       all_table_orders = [order for order in today_orders if order['table_no'] == table]
       category_type = list(set([table_order['category'] for table_order in all_table_orders]))
       for category in category_type:
           all_category.append({'category':category,'items':[tab_order for tab_order in all_table_orders if tab_order['category']==category]})
       order_no = all_table_orders[0]['order_no']
       comments = json.loads(dbget("select * from public.order_comments where order_no='"+order_no+"' order by comments_time "))
       total_orders.append({'table_no':table,'order_no':order_no,'all_items':all_category,'commenst':comments})
   order_status_count = json.loads(dbget("select count(*) as order_status_count from food_order where order_status_id=5 \
                                         group by order_status_id"))
   
   order_count1 = order_status_count[0]['order_status_count'] if len(order_status_count) != 0 else 0
   ed_time = time.time()
   full_time = ed_time - st_time
   print("Time Taken", full_time)
   return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":total_orders,
                      "order_status_count":order_count1},indent=2)


def Query_food_orders_waiter(request):
   st_time = time.time()
   today_orders = json.loads(dbget("select food_menu.food_name,food_category.*, food_order.*,\
                                  order_status.order_status_desc,notification_status.* from food_order\
                                   left join food_menu on food_menu.food_id = food_order.food_id\
                                   left join food_category on food_category.category_id =food_menu.item_category_id\
                                   left join order_status on order_status.order_status_id = \
                                   food_order.order_status_id join notification_status on\
                                   food_order.notification_status_id = notification_status.notification_status_id \
                                   where food_order.order_status_id!=7 \
                                   order by datetime"))
   # print(today_orders)
   tables = list(set(order['table_no'] for order in today_orders))
   print("tables", tables)
   total_orders = []
   for table in tables:
       all_category = []
       all_table_orders = [order for order in today_orders if order['table_no'] == table]
       category_type = list(set([table_order['category'] for table_order in all_table_orders]))
       for category in category_type:
           all_category.append({'category': category, 'items': [tab_order for tab_order in all_table_orders if
                                                                tab_order['category'] == category]})
       order_no = all_table_orders[0]['order_no']
       comments = json.loads(
           dbget("select * from public.order_comments where order_no='" + order_no + "' order by comments_time "))
       total_orders.append({'table_no': table, 'order_no': order_no, 'all_items': all_category, 'commenst': comments})
   order_status_count = json.loads(dbget("select count(*) as order_status_count from food_order where order_status_id=5 \
                                        group by order_status_id"))

   order_count1 = order_status_count[0]['order_status_count'] if len(order_status_count) != 0 else 0
   ed_time = time.time()
   full_time = ed_time - st_time
   print("Time Taken", full_time)
   return json.dumps({"Return": "Record Retrived Successfully", "ReturnCode": "RRS", "Returnvalue": total_orders,
                      "order_status_count": order_count1}, indent=2)
