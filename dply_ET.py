#!/usr/bin/env python
# coding: utf-8



#import socket
import re
#import scrubadub as sb
from nltk.tokenize import word_tokenize
#from nltk import pos_tag
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import joblib
#from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
from flask import Flask, render_template, request

# Library for reading mail and writing to csv

#import email
from bs4 import BeautifulSoup
from imap_tools import MailBox, AND, A,Q
import numpy as np 
import pandas as pd 





#!pip install spacy


#def __init__(self):
#    self.socket = socket.socket()
#    self.connection, _ = self.socket.create_connection(('106.51.18.139', 5500))
#    self.streaming()

app = Flask(__name__)

@app.route("/emailtriage",methods = ["GET","POST"])
def emailtriage():
 
    # get list of email subjects from INBOX folder
    mailbox = MailBox('outlook.office365.com')
    #mailbox.login('payments@centelon.com', 'Zux11324', initial_folder='inbox')  # or mailbox.folder.set instead 3d arg
    mailbox.login('officialmailid', 'Password', initial_folder='inbox')  # or mailbox.folder.set instead 3d arg
    #User name: payments@centelon.com Password: Zux11324
    # afzal.mansury@centelon.com\payments@centelon.com
    for msg in mailbox.fetch(A(seen=False)):
        soup = BeautifulSoup(msg.html, features="html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        elements = soup.find_all("div", id="Signature")
    
        for element in elements:
            element.decompose()
    
        if len(soup.get_text())>0:
            text = soup.get_text()
        else:
            soup = BeautifulSoup(msg.text)
            text = soup.get_text()
        
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        subjects = msg.subject
        #print(subjects)
        
        
        match = re.search(r'((Re\:\sFW\:)|(Re\:)|(RE\:)|(FW\:)|(Fw\:)|(Fwd\:)(RE\:\sFW\:))', subjects)
        # If-statement after search() tests if it succeeded
        if match:
            #print('found',match.group(0)) ## 'found word:cat'
            #print(text)
            if match.group()=="RE:" or match.group()=="Re:" or match.group()=="FW:" or match.group=="Fw:"or match.group()=="Fwd:":
                
                try:
                    try:
                        pattern = re.compile(r'RE:|Re:|FW:|Fw:|Fwd:')
                        matches = pattern.finditer(text)
                        match_span_sub = []
                        for match in matches:
                            match_span_sub.append(match.span())
                        last_span_sub = match_span_sub[0] #[0]

                        text = text[last_span_sub:]
                    except:
                        text = text
                except:
                    print("no subject found")
                try:
                    match = re.search(r'Thanks & Regards,|From:|Thanks & regards,|Kindly regards,|Regards Poonam AR Team|Thanks & Regards|Signing off,|Regards|Best regards,|Kind regards,|Warm regards,|IMPORTANT: This e-mail|CONFIDENTIALITY AND PRIVACY NOTICE|CONFIDENTIALITY:|With kind regards,|Kind regards|THANKING YOU ALL|Yours sincerely &  Regards|Warm Regards,|THANKING YOU ALL', text)
                    result = text.index(match.group(0))
                    text = text[:result]
                except:
                    print(" ")
        else:
            #print(text)
            text_full = []
            for text in text.splitlines():
                if not text.startswith(("Subject:","Cc:","Sent:","From:","To:")): #"Subject:",
                    text_full.append(text)
                    
            text = " ".join(text_full)
            try:
                match = re.search(r'Thanks & Regards,|From:|Thanks & regards,|Kindly regards,|Regards Poonam AR Team|Thanks & Regards|Signing off,|Regards|Best regards,|Kind regards,|Warm regards,|IMPORTANT: This e-mail|CONFIDENTIALITY AND PRIVACY NOTICE|CONFIDENTIALITY:|With kind regards,|Kind regards|THANKING YOU ALL|Yours sincerely &  Regards|Warm Regards,|THANKING YOU ALL', text)
                result = text.index(match.group(0))
                text = text[:result]
            except:
                print("Not Required",text)

        #print("*"*40,"End of mail body","*"*40,text)
        
        
        model = joblib.load('ml_model_pkl/NB_CV.sav')
        count_vect = joblib.load('C:/Users/mansurya/Desktop/Email_triage/Final_ET_Project/transformer/count_vect_trans.sav')
        #new_desc = ["Here we can check for single mail"]
        labels = ["AR","NAR"]
        nb_count =  count_vect.transform([text])
        #nb_count =  tfidf_vect.transform(new_desc)
        #nb_count =  tfidf_vect_ngram.transform(new_desc)
        
        #nb_count =  tfidf_vect_ngram_chars.transform(new_desc)
        pred = model.predict(nb_count)
        pred = labels[pred[0]]
        print(pred)
        
        mailbox.seen(msg.uid, False)
        
        if pred   == 'NAR':
            mailbox.move(msg.uid,destination_folder="text_mail/NAR")
        else:
            mailbox.move(msg.uid,destination_folder="test_mail/AR")

    return 'executed successfully'



if __name__ == '__main__':
    app.run(port=5045)
    

