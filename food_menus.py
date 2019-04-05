from sqlwrapper import *
def Add_food_menu(request):
   if request.method =="POST":
       s = {}
       d = request.json
       
       d['food_name'] = d['food_name'].title()
       
       d['food_id'] = json.loads(dbget("select uuid_generate_v4() as order_no"))[0]['order_no']
       if d['item_category_id'].isdigit():
           
           gensql('insert','food_menu',d)
       
       else:
           s['category'] = d['item_category_id'].upper()
           
           gensql('insert','food_category',s)
           d['item_category_id'] = (json.loads(dbget("select * from food_category where category = '"+str(s['category'])+"'")))[0]['category_id']
           print(d)
           
           gensql('insert','food_menu',d)
       
       
       return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
   elif request.method =="GET":
       food_details,food_menu_details = [],[]
       GET_FOOD_MENUS = json.loads(dbget("select food_offers.*,offer_status.offer_status,offer_type.offer_type,food_category.*,food_status.status, food_menu.* from food_menu\
                                         left join food_category on food_category.category_id = food_menu.item_category_id \
                                         left join food_status on food_status.status_id = food_menu.food_status_id\
				         left join food_offers on food_offers.food_id = food_menu.food_id\
				         left join offer_status on offer_status.offer_status_id = food_offers.offer_status_id\
				         left join offer_type on offer_type.offer_type_id = food_offers.offer_type_id"))
       
       for food_menu in GET_FOOD_MENUS:
          if food_menu['category'] not in food_details:
             food_details.append(food_menu['category'])
             food_menu_details.append({"categry_name":food_menu['category'],"category_img":food_menu['image_url'],"category_id":food_menu['category_id'],"item":[]})
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
   
   s = {k:v for k,v in d.items() if k in ('food_id')}
   d = {k:v for k,v in d.items() if v is not None if k not in ('food_id')}
   d['food_name'] = d['food_name'].title()
   update_item = gensql('update','food_menu',d,s)
   return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)
   

def Display_Disable_Food_Item(request):
   get_disable_item = json.loads(dbget("select food_status.status, food_category.category,food_menu.* from food_menu  \
                                        left join food_status on food_status.status_id = food_menu.food_status_id\
                                        left join food_category on food_category.category_id = food_menu.item_category_id where food_status_id = '2'"))
   return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":get_disable_item,"Status": "Success","StatusCode": "200"},indent = 4)

def Add_Food_Offers(request):
   
      d = request.json
      dish_id ,list1= '',[]
      if d['food_id'] is None:
         get_offers = json.loads(dbget("select * from food_menu where item_category_id = '"+str(d['category_id'])+"'"))
         print("sucess")
         for get_offer in get_offers:
             list1.append(tuple((get_offer['food_id'],d['offer_value'],d['offer_type_id'],d['offer_status_id'])))
             if len(dish_id) == 0:
                dish_id = "'"+str(get_offer['food_id'])+"'"
             else:
                dish_id += ","+"'"+str(get_offer['food_id'])+"'"
         #print(dish_id)
         #print(list1)
         dbput("delete from food_offers where food_id in ("+str(dish_id)+")")
         values = ', '.join(map(str, list1))
         dbput("INSERT INTO  food_offers (food_id, offer_value, offer_type_id, offer_status_id)VALUES {}".format(values))
         
    
      else:
         print("fada")
         d = {k:v for k,v in d.items() if v is not None if k not in ('category_id')}
         gensql('insert','food_offers',d)
      '''
      getcount  = json.loads(dbget("select count(*) from food_offers where food_id = '"+str(d['food_id'])+"'"))
      
      if getcount[0]['count'] != 0:
         a = {k:v for k,v in d.items() if v is not None if k not in ('food_id')}
         b = {k:v for k,v in d.items() if k in ('food_id')}
         gensql('update','food_offers',a,b)
         
      else:
         print("its OFFER INSERT inside")
         d = {k:v for k,v in d.items() if v is not None}
         gensql('insert','food_offers',d)
      '''
      return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
def Update_Food_Offers(request):
   d = request.json
   dish_id ,list1= '',[]
   if d['food_id'] is None:
         get_offers = json.loads(dbget("select * from food_menu where item_category_id = '"+str(d['category_id'])+"'"))
         print("sucess")
         for get_offer in get_offers:
             list1.append(tuple((get_offer['food_id'],d['offer_value'],d['offer_type_id'],d['offer_status_id'])))
             if len(dish_id) == 0:
                dish_id = "'"+str(get_offer['food_id'])+"'"
             else:
                dish_id += ","+"'"+str(get_offer['food_id'])+"'"
         #print(dish_id)
         #print(list1)
         dbput("delete from food_offers where food_id in ("+str(dish_id)+")")
         values = ', '.join(map(str, list1))
         dbput("INSERT INTO  food_offers (food_id, offer_value, offer_type_id, offer_status_id)VALUES {}".format(values))
         
    
   else:
         print("fada")
         a = {k:v for k,v in d.items() if v is not None if k not in ('food_id','category_id')}
         b = {k:v for k,v in d.items() if k in ('food_id')}
         gensql('update','food_offers',a,b)
   return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)
   
def Select_Food_Offers(request):

  get_food_offers = json.loads(dbget(" select food_category.category,food_menu.food_name,food_menu.price,food_menu.item_category_id,offer_type.offer_type,offer_status.offer_status,food_offers.* from food_offers\
			 left join offer_type on offer_type.offer_type_id = food_offers.offer_type_id\
			 left join offer_status on offer_status.offer_status_id = food_offers.offer_status_id\
			left join food_menu on food_menu.food_id = food_offers.food_id\
			 left join food_category on food_category.category_id = food_menu.item_category_id"))
  return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":get_food_offers,"Status": "Success","StatusCode": "200"},indent = 4)
