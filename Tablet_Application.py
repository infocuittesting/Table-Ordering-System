from sqlwrapper import *
import base64
from collections import Counter
def Display_Food_Menus(request):
    
    
       food_details,food_menu_details = [],[]
       GET_FOOD_MENUS = json.loads(dbget("select food_type.*,food_category.*,food_status.status, food_menu.* from food_menu\
                                         left join food_category on food_category.category_id = food_menu.item_category_id \
                                         left join food_status on food_status.status_id = food_menu.food_status_id\
                                         left join food_type on food_type.food_type_id = food_menu.food_type_id where food_menu.food_status_id = 1 and food_category.category_id !=62 "))
       #get_best_sellers = json.loads(dbget(""))
       for food_menu in GET_FOOD_MENUS:
          if food_menu['category'] not in food_details:
             food_details.append(food_menu['category'])
             food_menu_details.append({"categry_name":food_menu['category'],"category_img":food_menu['image_url'],"items":[]})
       for food_menu in GET_FOOD_MENUS:
          for food_menu_detail in food_menu_details:
            
             if food_menu['category'] ==food_menu_detail['categry_name']:
                food_menu['item_images'] = [{"item_image":food_menu['food_id_url']}]
                food_menu_detail["items"].append(food_menu)
       get_best_sellers= json.loads(dbget("select food_category.category_id,food_category.category,food_category.image_url,food_menu.food_name,food_menu.price,food_menu.food_id_url,\
                                           food_type.food_type_id,food_type.food_type,food_status.status,\
                                           food_order_history.food_id,count(*) from food_order_history \
                                           left join food_menu on food_menu.food_id = food_order_history.food_id\
                                           left join food_category on food_category.category_id= food_menu.item_category_id\
                                           left join food_type on food_type.food_type_id = food_menu.food_type_id\
                                           left join food_status on food_status.status_id = food_menu.food_status_id\
                                           where food_menu.food_status_id = 1 and  food_category.category_id !=62 \
                                           group by food_order_history.food_id,food_category.category_id,food_menu.food_name,food_name,food_menu.price,food_menu.food_id_url,\
                                           food_category.category,\
                                           food_type.food_type_id,food_type.food_type,food_category.image_url,food_status.status\
                                           order by count desc"))
       k = [x['category'] for x in get_best_sellers]

       new_vals=[]

       for i in Counter(k):
           all_values = [x for x in get_best_sellers if x['category']==i]
           #all_values['']
           #print("all",all_values)
           new_vals.append(max(all_values, key=lambda x: x['count']))
       get_offers_menu = json.loads(dbget("select food_type.*,food_category.*,food_status.status, food_menu.* from food_menu \
                                         left join food_category on food_category.category_id = food_menu.item_category_id \
                                         left join food_status on food_status.status_id = food_menu.food_status_id \
                                         left join food_type on food_type.food_type_id = food_menu.food_type_id \
				         where food_menu.food_status_id = 1 and offer_value != 0"))
       
       final_get_offers_menu = [dict(item, item_images=[dict(item_image=item['food_id_url'])]) for item in get_offers_menu]
       final_get_best_sellers_menu = [dict(item, item_images=[dict(item_image=item['food_id_url'])]) for item in new_vals]
             
       specials = json.loads(dbget("select food_category.category_id,food_category.category,food_category.image_url,food_menu.*,today_special.today_special_status,\
                                   food_type.food_type_id,food_type.food_type,food_status.status\
                                   from public.food_menu\
                                  join today_special on food_menu.today_special_id = today_special.today_special_id \
                                  left join food_category on food_category.category_id= food_menu.item_category_id\
                                  left join food_type on food_type.food_type_id = food_menu.food_type_id\
                                  left join food_status on food_status.status_id = food_menu.food_status_id\
                                  where food_status_id=1 and item_category_id!=62 and food_menu.today_special_id=1"))

       today_specials = [dict(special, item_image=[dict(image_url=special['food_id_url'])]) for special in specials]
       final_food_menu = [{"Food_Category":food_menu_details,"Offers":final_get_offers_menu,
                          "Best_Sellers":final_get_best_sellers_menu,
                          "Today_Special":{"categry_name":"Today_Specials",
                                           "category_img":"https://s3.amazonaws.com/image-upload-rekognition/tosfoodimages/new_work_cadillacmagazine-624x406.png",
                                           "items":today_specials}}]

       return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":final_food_menu,"Status": "Success","StatusCode": "200"},indent = 4)
def Tablet_Login_And_Logout(request):
   d = request.json
   try:
          get_password = json.loads(dbget("select * from table_details where table_no = '"+str(d['table_no'])+"'"))
          print(get_password)
          
          str_to_bype = get_password[0]['table_password'].encode("utf-8")
          print("str_to_bype",str_to_bype,type(str_to_bype))

          output = (base64.b64decode(str_to_bype)).decode()
          print('output samae as input',output,type(output))
   except:
          return json.dumps({"Return":"Table Number Data Not Exist","ReturnCode":"TNDNE"})
   if d['login_status_id'] == 1:
       if output == d['password']:
           dbput("update table_details set login_status_id = '"+str(d['login_status_id'])+"'")
           return json.dumps({"Return": "Login Successfully","ReturnCode": "LS","Status": "Success","StatusCode": "200"},indent = 4)
       
       else:
           return json.dumps({"Return": "Login OR Password Incorrect","ReturnCode": "LOPI","Status": "Success","StatusCode": "200"},indent = 4)
       
   else:
      if output == d['password']:
           dbput("update table_details set login_status_id = '"+str(d['login_status_id'])+"'")
           return json.dumps({"Return": "LogOut Successfully","ReturnCode": "LOS","Status": "Success","StatusCode": "200"},indent = 4)
       
      else:
           return json.dumps({"Return": "Login OR Password Incorrect","ReturnCode": "LOPI","Status": "Success","StatusCode": "200"},indent = 4)
  #return json.dumps({"Return": "LogOut Successfully","ReturnCode": "LS","Status": "Success","StatusCode": "200"},indent = 4)
def Query_Extra_Item_Category(request):
       get_extra_item = json.loads(dbget("select food_type.*,food_category.*,food_status.status, food_menu.* from food_menu\
                                         left join food_category on food_category.category_id = food_menu.item_category_id \
                                         left join food_status on food_status.status_id = food_menu.food_status_id\
                                         left join food_type on food_type.food_type_id = food_menu.food_type_id where food_menu.food_status_id = 1 and food_category.category_id = 62"))
       
       return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":get_extra_item,"Status": "Success","StatusCode": "200"},indent = 4)  
