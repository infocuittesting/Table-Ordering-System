from sqlwrapper import *
def Sales_Closed(request):

   dbput("INSERT INTO food_order_history(order_details_id, order_no, table_no, food_id, quantity, order_status_id, datetime)  \
          SELECT order_details_id, order_no, table_no, food_id, quantity, order_status_id, datetime FROM food_order")
   dbput("INSERT INTO history_order_comments(order_comments_id, order_no, order_comments, comments_time)  \
          SELECT * FROM order_comments")
   dbput("INSERT INTO history_order_timings(order_no, order_time, bill_request_time, close_time)  \
          SELECT * FROM order_timings")
   dbput("delete from food_order")
   dbput("delete from order_comments")
   dbput("delete from order_timings")
   return json.dumps({"Return": "Sales Closed","ReturnCode": "SC","Status": "Success","StatusCode": "200"},indent = 4)
