from sqlwrapper import *
from collections import defaultdict
from Fetch_Current_Datetime import *
def Report_Service(request):
    d = request.json
    get_category_table_order,final_list,get_category_orders = [],[],[]
    if d['type'] == 1:
        
        d = request.json
        get_category_orders = []
        get_categories_report = json.loads(dbget("SELECT food_name,food_category.category,count(*)\
                                     FROM public.food_order_history join food_menu on\
                                     food_order_history.food_id  = food_menu.food_id\
                                      join food_category on food_menu.item_category_id = food_category.category_id\
                                         where food_category.category_id!=7 and datetime between '"+d['from_date']+"' and '"+d['to_date']+"'\
                                      group by food_menu.food_name,food_category.category"))
        
        c = defaultdict(int)
        for d in get_categories_report:
                        c[d['category']] += d['count']
        finals = [{'category': category.title(), 'Count': count,"food_items_reports":[]} for category, count in c.items()]
        
        for get_category in get_categories_report:
            for final in finals:
                
                if final['category'] == get_category['category'].title():
                    final['food_items_reports'].append({"food_name":get_category['food_name'],"Count":get_category['count']})

            
        return json.dumps({"Return":"Category","Return_Category":finals},indent=2)
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
                                                                where date(datetime) between '"+str(d['from_date'])+"' and '"+str(d['to_date'])+"' and table_no ='"+str(get_table_order['table_no'])+"' and  item_category_id != 7 group by food_order_history.food_id,food_order_history.table_no,\
                                                                food_category.category,food_menu.item_category_id,food_menu.food_name "))
                #res = list(filter(lambda i: i['id'] != 2, test_list)) 
                get_category_table_order.append({"table_no":"Table"+" "+str(get_table_order['table_no']),"Count":get_table_order['count'],"items":table_category})
            for get_categorys in get_category_table_order:
            

                c = defaultdict(int)
                for d in get_categorys['items']:
                        c[d['category']] += d['count']
                final = [{'Category_name': category.title(), 'Count': count} for category, count in c.items()]
                get_categorys['category_reports']=final
                get_categorys.pop('items')
                    
            
            return json.dumps({"Return":"Table","Return_Table":get_category_table_order},indent=2)
    if d['type'] == 3:
        get_amount = json.loads(dbget("select sum(grand_total) as amount,date(order_time) from history_order_timings group by date(order_time) order by date(order_time)"))
        return json.dumps({"Return":"linear","dataProvider":get_amount},indent=2)
def Categories_Basis_Report(request):
    d = request.json
    get_category_orders = []
    get_categories_report = json.loads(dbget("SELECT food_name,food_category.category,count(*)\
                                 FROM public.food_order_history join food_menu on\
                                 food_order_history.food_id  = food_menu.food_id\
                                  join food_category on food_menu.item_category_id = food_category.category_id\
                                     where food_category.category_id!=7 and datetime between '"+d['from_date']+"' and '"+d['to_date']+"'\
                                  group by food_menu.food_name,food_category.category"))
    
    c = defaultdict(int)
    for d in get_categories_report:
                    c[d['category']] += d['count']
    finals = [{'category': category.title(), 'Count': count,"food_items_reports":[]} for category, count in c.items()]
    
    for get_category in get_categories_report:
        for final in finals:
            
            if final['category'] == get_category['category'].title():
                final['food_items_reports'].append({"food_name":get_category['food_name'],"Count":get_category['count']})
       
    return json.dumps({"Return":finals},indent=2)
def Insert_Feedback(request):
    d= request.json
    e = {"order_no":d['order_no']}
    d = {k:v for k,v in d.items() if k not in ('order_no')}
    d.update({'feedback_time':application_datetime(),"q1":d['q1'].title(),
              "q2":d['q2'].title(),
              "q3":d['q3'].title(),
              "q4":d['q4'].title(),
              "q5":d['q5'].title()})
    
    gensql('update','feedback',d,e)
    return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
