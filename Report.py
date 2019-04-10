from sqlwrapper import *
from collections import defaultdict

def Report_Service(request):
    d = request.json
    get_category_table_order,final_list = [],[]
    #get overall table orders report
    if d['type'] == 2:
        get_table_orders = json.loads(dbget("select table_no,count(table_no) from food_order_history\
	left join food_menu on food_menu.food_id = food_order_history.food_id\
	left join food_category on food_category.category_id = food_menu.item_category_id\
        where date(datetime) between '"+str(d['from_date'])+"' and '"+str(d['to_date'])+"' and  item_category_id != 7 group by table_no order by table_no"))
        
        for get_table_order in get_table_orders:
           
            table_category=json.loads(dbget("select food_order_history.food_id,food_order_history.table_no,food_menu.food_name,food_category.category,count(food_menu.food_id) from food_order_history \
                                                            left join food_menu on food_menu.food_id= food_order_history.food_id\
                                                            left join food_category on food_category.category_id = food_menu.item_category_id\
                                                            where table_no ='"+str(get_table_order['table_no'])+"' and  item_category_id != 7 group by food_order_history.food_id,food_order_history.table_no,\
                                                            food_category.category,food_menu.item_category_id,food_menu.food_name "))
            #res = list(filter(lambda i: i['id'] != 2, test_list)) 
            get_category_table_order.append({"table_no":get_table_order['table_no'],"items":table_category})
    for get_categorys in get_category_table_order:
        

            c = defaultdict(int)
            for d in get_categorys['items']:
                    c[d['category']] += d['count']
            final = [{'Category_name': category.title(), 'Count': count} for category, count in c.items()]
            get_categorys['category_reports']=final

    return json.dumps({"overall_table_orders":get_table_orders,"return":get_category_table_order},indent=2)
