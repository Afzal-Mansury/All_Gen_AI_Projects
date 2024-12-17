# Schedule Library imported 

import schedule 
import time 

from dply_ET import emailtriage


# Functions setup 
def schedule_ET(): 
    emailtriage()
    # Task scheduling 
    # After every 10mins geeks() is called. 
    
#schedule.every(1).minutes.do(schedule_ET) 
schedule.every(1).minutes.do(schedule_ET)
# Loop so that the scheduling task 
# keeps on running all time. 
while True: 

	# Checks whether a scheduled task 
	# is pending to run or not 
	#schedule.run_pending() 
	time.sleep(1) 
