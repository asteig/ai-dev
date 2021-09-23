'''
Your job is to cook the meals for every order while keeping waste to a
minimum.  Orders will be clipped to the line periodically when taken  
from customers.  Customers have limited patience and will abandon     
their orders if you take too long.  Each order will contain a number  
of meals and also some drinks, the drinks are not your responsibility,
only the food items.                                                  
                                                                     
Every meal has a single ingredient and is cooked in or on one of the  
four appliances, a deep fat fryer, hot griddle, flame grill or in a   
water vat.  Most ingredients can be fetched from the pantry.  There   
are two special cases however, fried noodles and rice, for which the  
ingredients are obtained by cooking boiled noodles or rice first.     
                                                                     
All the appliances are operated with the get and put commands.  Some  
meals may require further preparation once cooked, others can be      
packaged up straight away, ready for passing to the customer services 
staff.                                                                
                                                                     
The manager is very keen on both food hygiene and on keeping wastage  
in the kitchen low, he will take these factors into consideration     
along with how well you served food up for the customer orders when   
judging your performance.                                             

Syntax
check orders                                                               
check [order] <order number>                                               
fetch <ingredients> from pantry                                            
put <ingredient> {on|in|into} <appliance>                                  
check appliances                                                           
check <appliance>                                                          
get <food> from <appliance>                                                
prepare <food>                                                             
get <meal> from <prep surface>                                             
put <meal> {on|in|into} <chutes>                                           
put <waste> in <bin> 
'''

class McKitchen:
	
	def __init__(self):
		pass
		
	def check_(self, data):
		pass
		
	def fetch_(self, data):
		pass
	
	def get_(self, data):
		pass
	
	def prepare_(self, data):
		pass
	
	def put_(self, data):
		pass
