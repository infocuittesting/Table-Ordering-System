
from sqlwrapper import  *
from Fetch_Current_Datetime import *
import time
def Place_Order(request):
    
    d = request.json
    print(d)
    items = d['items']

    orders = json.loads(dbget("select order_no from food_order where table_no="+str(d['table_no'])+" and order_status_id !=7"))
    print(orders)
    
    order_no = json.loads(dbget("select uuid_generate_v4() as order_no"))[0]['order_no'] if len(orders) == 0 else orders[0]['order_no']
    print(order_no)
    
    for item in items:
        item.update({'order_no':order_no,'datetime':application_datetime(),'table_no':d['table_no']})
        gensql('insert','food_order',item)
    order_comments = {'order_no':order_no,'order_comments':d['comments'],'comments_time':item['datetime']}    
    gensql('insert','order_comments',order_comments)
    dbput("update table_details set table_status_id = '2' where table_no = "+str(d['table_no'])+"")
    return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)


def Query_today_food_orders(request):
   st_time = time.time()
   today_orders = json.loads(dbget("select food_menu.food_name,food_category.*, food_order.*,\
                                   order_status.order_status_desc from food_order\
                                    left join food_menu on food_menu.food_id = food_order.food_id\
                                    left join food_category on food_category.category_id =food_menu.item_category_id\
                                    left join order_status on order_status.order_status_id = \
                                    food_order.order_status_id where food_order.order_status_id!=7 \
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
       total_orders.append({'table_no':table,'order_no':order_no,'all_items':all_category})
   ed_time = time.time()
   full_time = ed_time - st_time
   print("Time Taken", full_time)
   return json.dumps({"Returnvalue":total_orders},indent=2)

def Query_food_orders(request):
    print("daw")
    food_order_details,food_details,categories,list1 = [],{},[],[]
    get_orders=json.loads(dbget("select order_status.order_status_desc,food_menu.food_name,food_menu.price,food_category.category, food_order.* from food_order\
	left join food_menu on food_menu.food_id = food_order.food_id \
	left join food_category on food_category.category_id =food_menu.item_category_id \
	left join order_status on order_status.order_status_id = food_order.order_status_id order by datetime"))
    for get_order in get_orders:
          value = str(get_order['table_no'])
          print(value)
          if value not in food_details.keys():
            
                 food_details[""+str(get_order['table_no'])+""] =[]
                 food_order_details.append({"tableno":get_order['table_no'],"category_list":[]})
          else:
              pass
          
          food_details[""+str(get_order['table_no'])+""].append(get_order['category'])
              
    print(food_details)
                
                     # if get_order['category'] == category['category_name']:
    return json.dumps({"Returnvalue":food_order_details},indent=2)
