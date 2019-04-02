from sqlwrapper import  *
from Fetch_Current_Datetime import *

def Place_Order(request):
    
    d = request.json
    print(d)
    items = d['items']

    orders = json.loads(dbget("select order_no from food_order where table_no="+str(d['table_no'])+" and order_status_id!=7"))
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
    food_details ,food_order_details= [],[]
    get_orders=json.loads(dbget("select order_status.order_status_desc,food_menu.food_name,food_category.category, food_order.* from food_order\
	left join food_menu on food_menu.food_id = food_order.food_id \
	left join food_category on food_category.category_id =food_menu.item_category_id \
	left join order_status on order_status.order_status_id = food_order.order_status_id order by datetime"))
    for get_order in get_orders:
          if get_order['table_no'] not in food_details:
             food_details.append(get_order['table_no'])
             food_order_details.append({"tableno":get_order['table_no'],"category_list":[]})
          else:
              
                for food_order_detail in food_order_details:
                    if get_order['table_no'] ==food_order_detail['tableno']:
                      food_order_detail["category_list"].append({""+get_order['category']+"":[]})
    
    return json.dumps({"Returnvalue":food_order_details},indent=2)
