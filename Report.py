from sqlwrapper import *

def Report_Service(request):
    d = request.json
    #get overall table orders report
    if d['type'] == 2:
        get_table_orders = json.loads(dbget("select table_no,count(table_no) from food_order_history\
	left join food_menu on food_menu.food_id = food_order_history.food_id\
	left join food_category on food_category.category_id = food_menu.item_category_id\
        where date(datetime) between '"+str(d['from_date'])+"' and '"+str(d['to_date'])+"' and  item_category_id != 7 group by table_no order by table_no"))
        
        
    return"asda"
