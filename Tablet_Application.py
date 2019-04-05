from sqlwrapper import *
import base64
def Display_Food_Menus(request):
    
    
       food_details,food_menu_details = [],[]
       GET_FOOD_MENUS = json.loads(dbget("select food_offers.*,offer_status.offer_status,offer_type.offer_type,food_category.*,food_status.status, food_menu.* from food_menu\
                                         left join food_category on food_category.category_id = food_menu.item_category_id \
                                         left join food_status on food_status.status_id = food_menu.food_status_id\
				         left join food_offers on food_offers.food_id = food_menu.food_id\
				         left join offer_status on offer_status.offer_status_id = food_offers.offer_status_id\
				         left join offer_type on offer_type.offer_type_id = food_offers.offer_type_id where food_menu.food_status_id = 1"))
       
       for food_menu in GET_FOOD_MENUS:
          if food_menu['category'] not in food_details:
             food_details.append(food_menu['category'])
             food_menu_details.append({"categry_name":food_menu['category'],"category_img":food_menu['image_url'],"item":[]})
       for food_menu in GET_FOOD_MENUS:
          for food_menu_detail in food_menu_details:
            
             if food_menu['category'] ==food_menu_detail['categry_name']:
                food_menu['item_images'] = [{"item_image":food_menu['food_id_url']}]
                food_menu_detail["item"].append(food_menu)
       return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":food_menu_details,"Status": "Success","StatusCode": "200"},indent = 4)
def Tablet_Login_And_Logout(request):
   d = request.json
   get_password = json.loads(dbget("select * from table_details where table_no = '"+str(d['table_no'])+"'"))
   print(get_password)
   
   str_to_bype = get_password[0]['table_password'].encode("utf-8")
   print("str_to_bype",str_to_bype,type(str_to_bype))

   output = (base64.b64decode(str_to_bype)).decode()
   print('output samae as input',output,type(output))
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
          
