'''This python file is created to build an user end of the Model that we have built. So that any user could use it in a
 quite less compliated way.'''

 # library calls
import json
import streamlit as st
import pandas as pd
import numpy as np 
import json 
import pickle

# calling the column names of the X data as the user is going to insert the specifications that are not supported by our model
# the model accepts the location as dummy variables but that is not quite easy to understand by the user so we are gonna ask use 
# to insert the location names directly. and we are gonna tranform then in the model supported form. which is why the column names are
# required
 
# calling and processing the columns  
with open('model/columns.json','r') as f:
    columns_json=json.load(f)

column_names=list(columns_json['columns'])

# function to convert the user inserted data into a model supported version ans also this function shows the out put of the data
def predict_price(sqft,bath,balcony,bhk,location,columnNames):
    x=np.zeros(len(columnNames))
    x[0]=sqft
    x[1]=bath
    x[2]=balcony
    x[3]=bhk
    
    location_index=np.where(columnNames==location)[0]
    if location_index>=0:
        x[location_index]=1

    with open('model/Bengaluru_realestate_price_model.pkl','rb') as f:
        lin_model=pickle.load(f)
    with col2:
        st.write(f'Estimated Price: Rs. {round(lin_model.predict([x])[0],2)} Lakh')

# extracting location names from the column names so that they can be inserted into to location selection list in the ui
locations_name=list(columns_json['columns'])[4:]

# building the ui using streamlit package

# background
st.markdown(f"""
         <style>
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1525015471056-0f7e78652361?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE0fHx8ZW58MHx8fHw%3D&w=1000&q=80");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """, unsafe_allow_html=True)

# title and subtitle
st.write('''
## Bengaluru Real-Estate Price Prediction App
This app estimates the price of the house based on the total area, bhk,balconies, location 
''')
# setting layout
col1, col2=st.columns(2)

# input layout
with col1:
    st.write('#### Choose your Specifications:')
    total_sqft=st.slider('Area(Square ft):',200,5000,1000)
    bhk=st.radio("BHK",[1,2,3,4,5],1,horizontal=True)
    balconies=st.radio("Bealconies",[1,2,3,4,5],1,horizontal=True)
    bathrooms=st.radio("Bathrooms",[1,2,3,4,5],1,horizontal=True)
    locations=str(st.selectbox("Locations",locations_name))

input={
    "Area(Sqft)":total_sqft,
    "BHK":bhk,
    "Balconies":balconies,
    "Bathrooms":bathrooms,
    "Locations":locations,
}
inputs_df=pd.DataFrame(input,index=[0])

# default output layout (a  line will be added when the model is called)
with col2:
    st.write('#### Estimated price:')
    st.write('Selected Choices:')
    st.write(inputs_df)
    st.button('Estimate',on_click=predict_price,args=(total_sqft,bathrooms,balconies,bhk,locations,column_names))
