from sqlwrapper import *
import datetime
from datetime import datetime,timedelta
from Fetch_Current_Datetime import *
def Sales_Closed(request):
   
   yesterday_date = datetime.strptime(application_datetime().strftime("%Y-%m-%d"),"%Y-%m-%d")-timedelta(days=1)
   yesterday = yesterday_date.strftime("%Y-%m-%d")
   print(yesterday_date.strftime("%Y-%m-%d"))
   dbput("INSERT INTO food_order_history(order_details_id, order_no, table_no, food_id, quantity, order_status_id, datetime)  \
          SELECT order_details_id, order_no, table_no, food_id, quantity, order_status_id, datetime FROM food_order where date(datetime)='"+str(yesterday)+"'")
   dbput("INSERT INTO history_order_comments(order_comments_id, order_no, order_comments, comments_time)  \
          SELECT * FROM order_comments where date(comments_time) = '"+str(yesterday)+"'")

   dbput("delete from food_order where  date(datetime)='"+str(yesterday)+"'")
   dbput("delete from order_comments where date(comments_time) = '"+str(yesterday)+"'")
   dbput("update users  set  todayorder_flag=1,fdorderwaiter_flag=1")
   return json.dumps({"Return": "Sales Closed","ReturnCode": "SC","Status": "Success","StatusCode": "200"},indent = 4)
