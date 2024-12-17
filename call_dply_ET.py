#from dply_ET import emailtriage
#emailtriage()
#try:
#    emailtriage()
#xcept:
#    print("no mail")

import requests
from datetime import datetime
url_test_img = 'http://127.0.0.1:5045/emailtriage'

requests.post(url_test_img)
print("ok",datetime.now())



#C:/Users/mansurya/Desktop/Email_triage/Final_ET_Project/dply_ET.py
# get url and image, img type
#url_test_img = 'http://127.0.0.1:5001/mask_image'

#response = requests.post(url_test_img)