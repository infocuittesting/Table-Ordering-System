from sqlwrapper import *
import requests
import re
import string
def Add_food_menu(request):
   if request.method =="POST":
       s = {}
       d = request.json
       #print("input data",d)
       #print("image",d['image_url'])
       food_id_url = d['food_id_url']
       img = d['image_url']
      # print("img",img,type(img),len(img))
       
       d['food_name'] = re.sub("'","''",d['food_name'])
       d['food_name'] = string.capwords(d['food_name'])
       get_name = json.loads(dbget("select count(*) from food_menu where food_name = '"+str(d['food_name'])+"'"))
       if get_name[0]['count'] == 0:
                           
          d['food_id'] = json.loads(dbget("select uuid_generate_v4() as order_no"))[0]['order_no']
          #Base 64 to Image
          if len(food_id_url) != 0:
             
             r = requests.post("https://cktab4aq0h.execute-api.us-east-1.amazonaws.com/tosimageupload",json={"base64":food_id_url})
             data = r.json()
             d['food_id_url'] = data['body']['url']
          d = {k:v for k,v in d.items() if v != ''  if v is not None if k  not in ('image_url')}
          if d['item_category_id'].isdigit():
              try:
                 gensql('insert','food_menu',d)
                 dbput("update users set fdmenu_flag=1")
                 return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
              except:
                 return json.dumps({"Return":"Duplicate Key Error or Value Error","ReturnCode":"DKEOV"},indent=2)
          
          else:
           
                 if len(img) != 0:
                 
                    get_url = requests.post("https://cktab4aq0h.execute-api.us-east-1.amazonaws.com/tosimageupload",json={"base64":img})
                    datas = get_url.json()
                    s['image_url'] = datas['body']['url']
                    s['category'] = d['item_category_id'].upper()
               
                
                 s['category'] = d['item_category_id'].upper()
                 try:
                  gensql('insert','food_category',s)
                 except:
                    return json.dumps({"Return":"category Duplicate Key Error or Value Error","ReturnCode":"DKEOV"},indent=2)
          
                 d['item_category_id'] = (json.loads(dbget("select * from food_category where category = '"+str(s['category'])+"'")))[0]['category_id']
                 #print(d)
                 try:
                  d = {k:v for k,v in d.items() if v != ''  if v is not None if k  not in ('image_url')}
                  gensql('insert','food_menu',d)
                  dbput("update table_details set disp_fm_flag=1;"
                        "update users set fdmenu_flag=1")
                 except:
                   
                   return json.dumps({"Return":"food name Duplicate Key Error or Value Error","ReturnCode":"DKEOV"},indent=2)
          
          return json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent = 4)
       else:
            
          return json.dumps({"Return":"Food Item Already Exist","ReturnCode":"FIAE","Status": "Success","StatusCode": "200"})
   elif request.method =="GET":
       #food_details,food_menu_details = [],[]
       GET_FOOD_MENUS = json.loads(dbget("select today_special.*,food_type.*,food_category.*,food_status.status, food_menu.* from food_menu\
                                         left join food_category on food_category.category_id = food_menu.item_category_id \
                                         left join food_status on food_status.status_id = food_menu.food_status_id\
                                         left join food_type on food_type.food_type_id = food_menu.food_type_id\
                                         left join today_special on today_special.today_special_id = food_menu.today_special_id"))

       return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":GET_FOOD_MENUS,"Status": "Success","StatusCode": "200"},indent = 4)

def select_item_category(request):
   
    get_category = json.loads(dbget("select * from food_category"))
    return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":get_category,"Status": "Success","StatusCode": "200"},indent = 4)
   
      

def Update_Food_Menus(request):
   d = request.json
   z,e={"category":d['category']},{}
   food_id =d['food_id_url']
   image_url = d['image_url']
   if len(food_id) != 0:
          print("if part working")
          r = requests.post("https://cktab4aq0h.execute-api.us-east-1.amazonaws.com/tosimageupload",json={"base64":food_id})
          data = r.json()
          d['food_id_url'] = data['body']['url']
          s = {k:v for k,v in d.items() if k in ('food_id')}
          d = {k:v for k,v in d.items() if v is not None if v != '' if k not in ('food_id','image_url','category')}
          d['food_name'] = re.sub("'","''",d['food_name'])
          d['food_name'] = string.capwords(d['food_name'])
         
         # try:
          gensql('update','food_menu',d,s)

         # except:
          #  return json.dumps({"Return":"Duplicate Key Error or Value Error","ReturnCode":"DKEOV"},indent=2)
   else:
      s = {k:v for k,v in d.items() if k in ('food_id')}
      d = {k:v for k,v in d.items() if v is not None if v != '' if k not in ('food_id','image_url','category')}
      d['food_name'] = re.sub("'","''",d['food_name'])
      d['food_name'] = string.capwords(d['food_name'])
      
      gensql('update','food_menu',d,s)

       
   if len(image_url) != 0:
              get_url = requests.post("https://cktab4aq0h.execute-api.us-east-1.amazonaws.com/tosimageupload",json={"base64":image_url})
              datas = get_url.json()
	      #z,e = {},{}
              z['image_url'] = datas['body']['url']
              e['category_id'] = d['item_category_id']
              #try:
              gensql('update','food_category',z,e)

              #except:
                # return json.dumps({"Return":"Wrong Category Id value Error","ReturnCode":"WCVE"},indent=2)
   else:
      
              e['category_id'] = d['item_category_id']
              
              gensql('update','food_category',z,e)
   dbput("update table_details set disp_fm_flag=1")
   dbput("update users set fdmenu_flag=1")
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

      dbput("update users set fdmenu_flag=1")
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
   dbput("update users set fdmenu_flag=1")
   return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent = 4)
   
def Select_Food_Offers(request):

  get_food_offers = json.loads(dbget(" select food_category.category,food_menu.food_name,food_menu.price,food_menu.item_category_id,offer_type.offer_type,offer_status.offer_status,food_offers.* from food_offers\
			 left join offer_type on offer_type.offer_type_id = food_offers.offer_type_id\
			 left join offer_status on offer_status.offer_status_id = food_offers.offer_status_id\
			left join food_menu on food_menu.food_id = food_offers.food_id\
			 left join food_category on food_category.category_id = food_menu.item_category_id"))
  return json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":get_food_offers,
                     "Status": "Success","StatusCode": "200"},indent = 4)

def Update_FoodMenu_Flag(request):
   d = request.json
   dbput("update table_details set disp_fm_flag=0 where table_no='"+str(d['table_no'])+"'")
   return json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS",
                      "Status": "Success","StatusCode": "200"},indent = 4)   
  
