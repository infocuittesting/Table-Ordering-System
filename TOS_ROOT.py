from flask import Flask,request
from flask_cors import CORS
TOS = Flask(__name__) #here i set environment varible for flask framework web application
CORS(TOS)
#-----------------------Configuration-------------------
from food_menus import *
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
if __name__ == "__main__":
    TOS.run(host ='192.168.99.1',port =5000)#run web application
