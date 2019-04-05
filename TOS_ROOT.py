from flask import Flask,request
from flask_cors import CORS


TOS = Flask(__name__) #here i set environment varible for flask framework web application
CORS(TOS)
#-----------------------Configuration-------------------
from food_menus import *
from Place_Order import *
from Billing_Application import *
from Tablet_Application import *
from Sales_Closed import *
#below i set path for web application

@TOS.route("/",methods=['GET','POST'])
def mos_index():
    return "Hello TOS Manager"

@TOS.route("/<string:name>",methods=['GET','POST'])
def pass_param(name):
    return (name)

#----------------CONFIGURATION---------------------
@TOS.route("/Add_Food_Menu_Items",methods=['POST','GET'])
def food_menu_card():
    return Add_food_menu(request)

@TOS.route("/Edit_Food_Menu_Items",methods=['POST'])
def edit_items():
    return Update_Food_Menus(request)
@TOS.route("/Select_Item_Category",methods=['GET','POST'])
def getcategory():
    return select_item_category(request)

@TOS.route("/Display_Disable_Food_Item",methods=['GET'])
def getdisableitems():
    return Display_Disable_Food_Item(request)

@TOS.route("/Add_Food_Offers",methods=['POST'])
def addoffers():
    return Add_Food_Offers(request)
@TOS.route("/Update_Food_Offers",methods=['POST'])
def updateoffers():
    return Update_Food_Offers(request)
@TOS.route("/Select_Food_Offers",methods=['POST','GET'])
def selectoffers():
    return Select_Food_Offers(request)
#-------------PLACE ORDER-------------------------------------------
@TOS.route("/Choose_Food_Order",methods=['POST'])
def placeorder():
    return Place_Order(request)
@TOS.route("/Query_today_food_orders",methods=['POST','GET'])
def todayorders():
    return Query_today_food_orders(request)

@TOS.route("/Query_food_orders",methods=['POST'])
def getorders():
    return Query_food_orders(request)

#----------------Billing-----------------------------------------------
@TOS.route("/Query_Table_Status",methods=['GET'])
def tablestatus():
    return Query_Table_Status(request)
@TOS.route("/Update_Order_Status",methods=['POST'])
def ordercompleted():
    return Update_Order_Status(request)
@TOS.route("/Update_ReadyforPayment_Status",methods=['POST'])
def tablepaymentstatus():
    return Update_ReadyforPayment_Status(request)
@TOS.route("/Update_Table_Available_Status",methods=['POST'])
def tableavailablestatus():
    return Update_Table_Available_Status(request)
@TOS.route("/Get_Order_Item_Table",methods=['POST'])
def billing_order_item():
    return Get_Order_Item_Table(request)
@TOS.route("/Update_Food_Order_Status_Item",methods=['POST'])
def updatefooditem():
    return Update_Food_Order_Status_Item(request)
@TOS.route("/Update_Category_Food_Menus",methods=['POST'])
def editcategoryfoodmenus():
    return Update_Category_Food_Menus(request)
#----------------TABLET----------------------------------------------------
@TOS.route("/Display_Food_Menus",methods=['GET','POST'])
def activefoodmenus():
    return Display_Food_Menus(request)
@TOS.route("/Tablet_Login_And_Logout",methods=['POST'])
def loginlogout():
    return Tablet_Login_And_Logout(request)
#------------sales closed-------------
@TOS.route("/Sales_Closed",methods=['GET'])
def salesclosed():
    return Sales_Closed(request)

	
if __name__ == "__main__":
    TOS.run(host ='192.168.99.1',port =5000)#run web application
