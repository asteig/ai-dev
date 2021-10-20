# standard libraries
import json
import re


# my stuff
from utils import *

# TASK GLOBALS
# keep track of everyone in line; indexed by order #
CUSTOMER_QUEUE = {}

'''
McSweeneys' Restaurant: Customer Service Counter

Your job is to take orders from and serve meals to a queue of         
customers.  You can have as many orders open at once as you like, but 
customers will not hang around forever so you should manage your time 
accordingly.  The job breaks down into a few basic tasks: Start taking
an order, add the cost of the order to the till (subtract costs if    
required), charge the customer and refund them their change, make the 
drinks for orders using the imp-powered drinks machine and serve the  
order, first getting the drinks from the machine and the dishes from  
the chute.


Simple example
	> take order                                                               
	The man says: A McSlice Porker and a McCola please.                        
	> list porker                                                              
	McSlice Porker ............................... $2.98                       
	> add 2.98                                                                 
	> list cola                                                                
	McCola ....................................... $2.77                       
	> add 2.77                                                                 
	> charge customer                                                          
	You say: The total comes to five dollars and seventy-five pence.           
	The man hands you six dollars which you place in the register.             
	> refund 25                                                                
	You clip order #48 onto the line.                                          
	> check 48                                                                 
	1x McSlice Porker                                                          
	1x McCola                                                               
	> press cola button                                                        
	An imp drops an empty cup onto the recessed well under the McCola spigot.  
																																						
	( Time passes, the McSlice Porker and the McCola are now prepared )        
																																						
	> get porker from chute                                                    
	> get cola from machine                                                    
	> serve 48                                                                 
	You get a new tray and place a McSlice Porker and a McCola on it.          
	You hand the tray to the man.   
'''


menu_txt = '''You read the menu:

Appetisers
		Boiled McRice                       A$1.40
		Fried McRice                        A$1.40
		Boiled McNoodles                    A$2
		Fried McNoodles                     A$2.12

Main Courses
		McKlatchian Kebab                   A$2.45
		McRib and McNoodles                 A$2.50
		McChopsuey and McNoodles            A$2.67
		McPrawn balls and McNoodles         A$2.67
		McCrunchy bits in orange sauce with McNoodles A$2.67
		McChowmein and McNoodles            A$2.75
		McSlice Porker                      A$3
		McCrispy Duck and McNoodles         A$3.25
		McDwarven Ratburger                 A$3.25
		McMorpork BigDibbler                A$4.37

Soft Drinks
		McCola                              A$2.67
		Strawberry McWobbler                A$3
		McJasmin Tea                        A$3
		McWater                             A$10
'''

ACTIVATE = 'Mr. O.L. Harribal says: Put yer uniform on and we can get started.'

''' take order
The queue moves forward as a pretentious old fellow and a sensitive schoolgirl approach the counter.
take order
They stare up at the sign and begin choosing what they'd like to order.
You haven't finished taking the current customers' order yet.
The sensitive schoolgirl lets the pretentious old fellow know what she'd like.
The pretentious old fellow says: We think we'd like a McRib, McChopsuey, two Boiled McRice and two McColas, if it's not too much trouble.
The pretentious old fellow asks: Think you can handle that?  How much will that be?

We think we'd like a McRib, McChopsuey, two Boiled McRice and two McColas, if it's not too much trouble.

==============
The thin mature gentleman says: We want McCrunchy bits in orange sauce, McChopsuey, a McKlatchian Kebab, Fried McNoodles, a McCola and a Strawberry McWobbler, and that's all.  Nothing else.

list McCrunchy
list McChopsuey
list McKlatchian
list McNoodles
list McCola
list McWobbler
'''

# hold all the tasks and logic to manage the counter
class McCounter:
	
	ROOM_ID = 'd2265a457a2d8adec9d30100fa6302e8477f045e'
	
	# keep track of all the orders
	ORDERS = {}
	
	drinks = ['McCola', 'McWobbler', 'McJasmin', 'McWater']
	
	menu = {}
	
	def __init__(self):
		pass

	# parse the menu and create a lookup table for prisces
	def list_(self, data):
		colorNote('parse the menu.....')
		print('DATA!!!!')
		print(data)

		# for item in data['items']:
		# 	name = item['item']
			
		# 	# handle combo items
		# 	if ' and ' in name or ' with ' in name:
		# 		name = name.replace(' with ', ' and ')
		# 		item1, item2 = name.split(' and ')
		# 		self.menu[item1] = {
		# 			'name': item1, 
		# 			'combo': item2,
		# 			'price': item['price']
		# 		}
		# 	else:
		# 		self.menu[name] = {
		# 			'name': name, 
		# 			'price': item['price'],
		# 		}
		
		# print('MENU COMBOS:')
		# [print(self.menu[i]) for i in self.menu if 'combo' in self.menu[i]]
	
	# handles 'take' command's response...
	# runs whenever a 'take' command is completed...
	def take_(self, data):
		# keep track of the total order price as items are added
		print('TAKE DATA:')
		print(data)

	# handles 'charge' command's response
	def charge_(self, data):
		order = data['order']['txt']
'''
#### test out 'take'
order1 = 'We want McCrunchy bits in orange sauce, McChopsuey, a McKlatchian Kebab, Fried McNoodles, a McCola and a Strawberry McWobbler, and that\'s all.  Nothing else.'
order2 = 'We think we\'d like a McRib, McChopsuey, two Boiled McRice and two McColas, if it\'s not too much trouble.'

# SET MENU
full_menu = {'items': [{'item': 'Boiled McRice', 'price': '1.40'}, {'item': 'Fried McRice', 'price': '1.40'}, {'item': 'Boiled McNoodles', 'price': '2'}, {'item': 'Fried McNoodles', 'price': '2.12'}, {'item': 'McKlatchian Kebab', 'price': '2.45'}, {'item': 'McRib and McNoodles', 'price': '2.50'}, {'item': 'McChopsuey and McNoodles', 'price': '2.67'}, {'item': 'McPrawn balls and McNoodles', 'price': '2.67'}, {'item': 'McCrunchy bits in orange sauce with McNoodles', 'price': '2.67'}, {'item': 'McChowmein and McNoodles', 'price': '2.75'}, {'item': 'McSlice Porker', 'price': '3'}, {'item': 'McCrispy Duck and McNoodles', 'price': '3.25'}, {'item': 'McDwarven Ratburger', 'price': '3.25'}, {'item': 'McMorpork BigDibbler', 'price': '4.37'}, {'item': 'McCola', 'price': '2.67'}, {'item': 'Strawberry McWobbler', 'price': '3'}, {'item': 'McJasmin Tea', 'price': '3'}, {'item': 'McWater', 'price': '10'}], 'action': 'list'}


m = McCounter()
m.list_(full_menu)

print('ORDER #1')
print(order1)
m.take_({'order': {'txt': order1}})

print()
print()
print()
print()
print()

print('ORDER #2')
print(order2)
m.take_({'order': {'txt': order2}})
'''