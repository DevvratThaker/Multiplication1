# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:48:19 2021

@author: administrator
"""


# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 16:25:35 2021

@author: administrator
"""


from flask import Flask, request

from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import requests
from flask import jsonify
import re
import json
import pickle as p
 
# create the Flask app
rel = pickle.load(open("relativity.pkl", 'rb'))
app = Flask(__name__)
 
# GET requests will be blocked
@app.route('/json-example', methods=['POST'])
def json_example():
  request_data = request.get_json()
  
  channel = request_data['channel']
  segment = request_data['segment']
  vehage = request_data['vehage']
  addon = request_data['addon']
  fuel = request_data['fuel']
  make = request_data['make']
  district = request_data['district']
  ncb = request_data['ncb']
  creditscore = request_data['creditscore']
  gender = request_data['gender']
  polholdersage = request_data['polholdersage']
  breakin = request_data['breakin']

  
  df2 = pd.DataFrame([vehage])
  df2.columns = ['vehage']
  df2['vehage'] = pd.to_numeric(df2['vehage'])
  bins = [0, 1, 3, 5, 7, 10, 100]
  df2['range'] = pd.cut(df2['vehage'], bins)
  agegroup = df2.iloc[0,1]
  agegroup = re.sub("[^0-9]", "", "%s"%agegroup)
  
  df3 = pd.DataFrame([polholdersage])
  df3.columns = ['polholdersage']
  df3['polholdersage'] = pd.to_numeric(df3['polholdersage'])
  bins = [0, 18, 25, 30, 35, 40, 50, 60, 65, 150]
  df3['range'] = pd.cut(df3['polholdersage'], bins)
  custagegroup = df3.iloc[0,1]
  custagegroup = re.sub("[^0-9]", "", "%s"%custagegroup)
  
  df4 = pd.DataFrame([creditscore])
  df4.columns = ['creditscore']
  df4['creditscore'] = pd.to_numeric(df4['creditscore'])
  bins = [0, 700, 750, 800, 900]
  df4['range'] = pd.cut(df4['creditscore'], bins)
  creditscoregroup = df4.iloc[0,1]
  creditscoregroup = re.sub("[^0-9]", "", "%s"%creditscoregroup)
  
  
  
  interaction = agegroup + addon
  
  
  data = {channel,segment,interaction,custagegroup,fuel,make,district,ncb,creditscoregroup,gender,breakin}
  {'factors': ['channel', 'segment', 'interaction', 'custagegroup', 'fuel', 'make', 'district', 'ncb', 'creditscoregroup', 'gender', 'breakin']}
  df = pd.DataFrame(data)
  df = df.rename(columns={0: "factors"})
  channelrel = pd.merge(df,rel,on='factors')
  channelrel = channelrel[['factorsrel']]
  rate = channelrel['factorsrel'].product(axis=0)
  finalrate = (1.35*rate)
  
  return jsonify(
            glmrate = format(finalrate)
            )
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
        
    


  

         
