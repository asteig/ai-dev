McSweeneys' Restaurant         Discworld room help        McSweeneys' Restaurant



Name

     Customer Service Counter.                                                  

Description

     Your job is to take orders from and serve meals to a queue of         
     customers.  You can have as many orders open at once as you like, but 
     customers will not hang around forever so you should manage your time 
     accordingly.  The job breaks down into a few basic tasks: Start taking
     an order, add the cost of the order to the till (subtract costs if    
     required), charge the customer and refund them their change, make the 
     drinks for orders using the imp-powered drinks machine and serve the  
     order, first getting the drinks from the machine and the dishes from  
     the chute.                                                            

     The number of orders you take and serve, along with the number of     
     mistakes you make and food you waste will determine how Mr O.L        
     Harribal judges your performance.                                     

/std/mission/global/mcsweeneys/doc/serving From 1 to 23 of 94 (24%) - return to continue, h for help.
 

Simple example

     Note that some of the output below has been shortened or omitted for       
     clarity.                                                                   
     Note furthermore that the syntax for the refund works using both possible  
     syntaxes.                                                                  
     > refund 25                                                                
     > refund 0.25                                                              
 
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
/std/mission/global/mcsweeneys/doc/serving From 24 to 46 of 94 (48%) - return to continue, h for help.
 

     1x McCola                                                                  
     > press cola button                                                        
     An imp drops an empty cup onto the recessed well under the McCola spigot.  
                                                                                
     ( Time passes, the McSlice Porker and the McCola are now prepared )        
                                                                                
     > get porker from chute                                                    
     > get cola from machine                                                    
     > serve 48                                                                 
     You get a new tray and place a McSlice Porker and a McCola on it.          
     You hand the tray to the man.                                              
                                                                                
Syntax

     take [next] order                                                          
     recall [current customer order]                                            
     list [all]                                                                 
     list <menu item>                                                           
     add <amount> [to] [total]                                                  
     subtract <amount> [from] [total]                                           
     sub <amount> [from] [total]                                                
     reset <cash register>                                                      
     charge [customer]                                                          
     refund <amount>                                                            
/std/mission/global/mcsweeneys/doc/serving From 47 to 69 of 94 (73%) - return to continue, h for help.
 

     press <button>                                                             
     look <orders|line>                                                         
     check [order] <order number>                                               
     check orders                                                               
     get <food(s)> from chute                                                   
     get <drink(s)> from machine                                                
     serve [order] <order number>                                               

Strategy

     As with any job, there are always certain strategies that will be more     
     effective than others.  There are also shortcuts that can be taken to help 
     speed up tasks, these can be identifed by experienced workers.  On         
     Discworld MUD there is the opportunity to make use of aliases to combine   
     multiple commands into one and shorten the length of commands.  McSweeneys 
     would encourage you to make use of such aliases to enhance your            
     productivity.  Without using such measures you will find it much harder to 
     achieve gold-star rating.  Having said that, the use of aliases should not 
     lead to any job being trivialised, if you find any aliases that have this  
     affect, please file a bug report.                                          
                                                                                
     Note that automated scripts and triggers are not permitted on Discworld MUD
     in any context, see help automation.                                       

/std/mission/global/mcsweeneys/doc/serving From 70 to 92 of 94 (97%) - return to continue, h for help.
 
syntax take
/std/mission/global/mcsweeneys/doc/serving From 70 to 92 of 94 (97%) - return to continue, h for help.
 

See also

     alias, unalias, alias tutorial                                        
syntax take
(Igame) Algar wisps: ah, I shan't bother then, thanks!
Forms of syntax available for the command "take":
take [next] order                          
take <object> from <object> {into|to} [my] Get something from a container and
     {left hand|right hand} [and] [my]     hold it in two particular hands.
     {left hand|right hand}
take <object> from <object> {into|to} [my] Get something from a container and
     empty {hand|hands}                    hold it in any free hand.
take at most <number> <thing(s)> from      Get a number of items from a
     <container(s)>                        container.
take <object> {into|to} [my] {left         Pick something up and hold it in two
     hand|right hand} [and] [my] {left     particular hands.
     hand|right hand}
take <object> from <object> {into|to} [my] Get something from a container and
     {hand|hands}                          hold it in any hand.
take <object> from <object> {into|to} [my] Get something from a container and
     {left hand|right hand}                hold it in a particular hand.
take <object> {into|to} [my] empty         Pick something up and hold it in any
     {hand|hands}                          free hand.
take at most <number> <thing(s)>           Pick up a number of items.
take <thing(s)> out of <container(s)>      Get something from a container and
                                           leave it on the floor or ground.
take <object> {into|to} [my] {hand|hands}  Pick something up and hold it in any
                                           hand.
Take syntax From 1 to 23 of 27 (85%) - return to continue, h for help.
 

take <object> {into|to} [my] {left         Pick something up and hold it in a
     hand|right hand}                      particular hand.
take <thing(s)> from <container(s)>        Get something from a container.
take <thing(s)>                            Pick something up.
syntax recall
Forms of syntax available for the command "recall":
recall [current customer order]             
Strange clanking noises emanate from the drinks machine.
syntax list
Forms of syntax available for the command "list":
list <menu item>                           
list [all]                                 
syntax add
Forms of syntax available for the command "add":
add <amount> [to] [total]                 
(Wizards) Library wisps: Is there anyone here who can act as a recruiter for the Faculty club?
syntax subtract
Forms of syntax available for the command "subtract":
subtract <amount> [from] [total]  