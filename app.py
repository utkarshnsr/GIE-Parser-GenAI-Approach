import streamlit as st
import PIL.Image
from PIL import Image
import google.generativeai as genai
import ast
import io
import pandas as pd
import os
from dotenv import load_dotenv



def identifyGraphType(imgPath):
  prompt = """
    For the graph image that is uploaded, I want you to do the following: 

    1) first identify what type of graph it is (line, bar, pie, etc)

    Just return the answer as a string. Here is an example:

    if the graph is a bar graph then return bar graph
    if the graph is a scatter plot then return scatter plot
    if the graph is a pie chart then return pie chart
    if the graph is a line graph then return line graph
    """
  load_dotenv()
  API_KEY = os.environ.get("GOOGLE_API_KEY")
  genai.configure(api_key=API_KEY)
  model = genai.GenerativeModel('gemini-1.5-flash')
  img = Image.open(io.BytesIO(imgPath))
  response = model.generate_content([prompt, img])
  return response.text


def extractGraphCoordinates(imgPath):
  prompt = """
    For the graph image that is uploaded, I want you to do the following: 

    1) for each point on the graph, get its x and y coordinates and its color
    2) put the information for each point into a list


    if the graph is a pie chart, then do the following:

    1) for each sector get the name of the vector and the percentage it takes up in the graph
    2) put the information for each sector into a list

    return the list ONLY. NO OTHER WORDS. Here is an example:

    [(1,2, "red"), (3,4, "black")]
    """
  genai.configure(api_key="AIzaSyDbzF8OtYGXkd_Sezc-imqJduuW8ROkys4")
  model = genai.GenerativeModel('gemini-1.5-flash')
  img = Image.open(io.BytesIO(imgPath))
  response = model.generate_content([prompt, img])
  return response.text

#sample comment
file = st.file_uploader("Please upload your graph")

if file:
    bytes_data = file.getvalue()
    st.image(bytes_data)
    st.write(f'filename: {file.name}')
    graphType = identifyGraphType(bytes_data)
    st.write(f'type: {graphType}')
    coordinates = extractGraphCoordinates(bytes_data)
    coordinates = eval(coordinates)
    df = pd.DataFrame(coordinates, columns=['x_axis', 'y_axis', 'coordinate point color'])
    csv = df.to_csv(index=False).encode('utf-8')
    st.dataframe(df)
    csvFileName = file.name + "extractedPoints.csv"
    st.download_button("Download Data Points", csv, csvFileName)


    