'''
Your job is to keep the section clean and tidy, the cupboard contains 
everything you'll need.  There are a number of tables in your section,
and most will be occupied when you start your shift.  When a group has
finished their meal they will get up and leave the section, you must  
work out which table they've vacated and then clean the table ready   
for new customers.                                                    

The number of customers that choose to sit down and eat in your       
section will help to determine how well Mr O.L. Harribal judges your  
performance.  He will also take into consideration any complaints     
about your conduct and the number of customers that decide they'd     
rather sit elsewhere.                                                 

clear [trays] [from] <table>                                               
dip <mop> {in|into} <bucket>                                               
empty <bin>                                                                
empty <tray> {in|into} <bin>                                               
fill <bucket> from <tap>                                                   
fit <bag> {in|into} <bin>                                                  
get <thing> from cupboard                                                  
mop floor                                                                  
put <rubbish> in <bin>                                                     
put <empty tray> {in|into} cupboard                                        
rinse <cloth>                                                              
sweep [rubbish] [from] under <table>                                       
wet <cloth>                                                                
wipe <table>  
'''
class McCleaning:
	
	def __init__(self):
		# get all supplies
		print('get bucket,mop,broom,cloth,1st bag from cupboard')
		
		# get cloth and mop ready
		print('fill bucket from tap')
		print('dip mop into bucket')
		print('wet cloth')
		
		# put bag in bin...
		print('fit bag into bin')
		
	def get_(self, data):
		print('got some stuff!!!'.upper())
	
	def look_(self, data):
		print('looking at stuff!!!'.upper())
		# what did I look at?
	
	def wet_(self, data):
		print('i just wet some stuff!'.upper())
		
	def wipe_(self, data):
		print('rinse cloth')