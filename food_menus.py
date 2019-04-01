from sqlwrapper import *
def Add_food_menu(request):
   if request.method =="POST":
       s = {}
       d = request.json
       d['food_id'] = (json.loads(dbget("select * from count_id")))[0]['food_id']
       d['food_name'] = d['food_name'].title()
       if d['item_category_id'].isdigit():
           
           gensql('insert','food_menu',d)
       
       else:
           s['category'] = d['item_category_id'].upper()
           
           gensql('insert','food_category',s)
           d['item_category_id'] = (json.loads(dbget("select * from food_category where category = '"+str(s['category'])+"'")))[0]['category_id']
           print(d)
           
           gensql('insert','food_menu',d)
       
       dbput("update count_id set food_id = food_id + '1'")
       return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
   elif request.method =="GET":
       food_details,food_menu_details = [],[]
       GET_FOOD_MENUS = json.loads(dbget("select food_offers.*,offer_status.offer_status,offer_type.offer_type,food_category.category,food_status.status, food_menu.* from food_menu\
                                         left join food_category on food_category.category_id = food_menu.item_category_id \
                                         left join food_status on food_status.status_id = food_menu.food_status_id\
				         left join food_offers on food_offers.food_id = food_menu.food_id\
				         left join offer_status on offer_status.offer_status_id = food_offers.offer_status_id\
				         left join offer_type on offer_type.offer_type_id = food_offers.offer_type_id"))
       
       for food_menu in GET_FOOD_MENUS:
          if food_menu['category'] not in food_details:
             food_details.append(food_menu['category'])
             food_menu_details.append({"categry_name":food_menu['category'],"item":[]})
       for food_menu in GET_FOOD_MENUS:
          for food_menu_detail in food_menu_details:
            
             if food_menu['category'] ==food_menu_detail['categry_name']:
                food_menu_detail["item"].append(food_menu)
       return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":food_menu_details,"Status": "Success","StatusCode": "200"},indent = 4)

def select_item_category(request):
    get_category = json.loads(dbget("select * from food_category"))
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":get_category,"Status": "Success","StatusCode": "200"},indent = 4)

def Update_Food_Menus(request):
   d = request.json
   #food_id = {k:v for k,v in d.items() if k in ('food_id')}
   #food = d['food']
   #offer = d['offer']
   #food_items = {k:v for k,v in food.items() if v!=None}
   #gensql('update','food_menu',food_items,food_id)
   if d['offer_value'] is None and d['offer_type_id'] is None and d['offer_status_id'] is None:
      
            s = {k:v for k,v in d.items() if k in ('food_id')}
            d = {k:v for k,v in d.items() if k not in ('offer_value','offer_type_id','offer_status_id','food_id')}
            
            print(s)
            d['food_name'] = d['food_name'].title()
            update_item = gensql('update','food_menu',d,s)
            print(update_item)
            return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)
   else:
      print("its came inside")
      getcount  = json.loads(dbget("select count(*) from food_offers where food_id = '"+str(d['food_id'])+"'"))
      s = {k:v for k,v in d.items() if k in ('food_id')}
      Z = {k:v for k,v in d.items() if k not in ('offer_value','offer_type_id','offer_status_id','food_id')}
            
      print(s)
      Z['food_name'] = Z['food_name'].title()
      update_item = gensql('update','food_menu',Z,s)
      if getcount[0]['count'] != 0:
         a = {k:v for k,v in d.items() if k in ('offer_value','offer_type_id','offer_status_id')}
         b = {k:v for k,v in d.items() if k in ('food_id')}
         gensql('update','food_offers',a,b)
         return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)
         #return json.dumps({"Return": "Food Offer Updated Successfully","ReturnCode": "FOUS","Status": "Success","StatusCode": "200"},indent = 4)
      else:
         print("its OFFER INSERT inside")
         d = {k:v for k,v in d.items() if k in ('offer_value','offer_type_id','offer_status_id','food_id')}
         gensql('insert','food_offers',d)
         return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)
         #return json.dumps({"Return": "Food Offer Inserted Successfully","ReturnCode": "FOIS","Status": "Success","StatusCode": "200"},indent = 4)
         

