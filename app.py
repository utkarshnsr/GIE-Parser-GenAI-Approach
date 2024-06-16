import streamlit as st
import PIL.Image
from PIL import Image
import google.generativeai as genai
import ast
import io
import pandas as pd
import os
from dotenv import load_dotenv


def configureGemini():
   load_dotenv()
   GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
   genai.configure(api_key=GOOGLE_API_KEY)


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

    return the list only (NO OTHER WORDS). Here is an example:

    [(1,2, "red"), (3,4, "black")]
    """
  model = genai.GenerativeModel('gemini-1.5-flash')
  img = Image.open(io.BytesIO(imgPath))
  response = model.generate_content([prompt, img])
  return response.text


def getCSVFile(df):
   csv = df.to_csv(index=False).encode('utf-8')
   return csv
   
   

def uploadGraphImage():
    st.subheader("File Uploader")
    graphFile = st.file_uploader("Please upload your graph",type=['png', 'jpg'])

    if graphFile:
       bytes_data = graphFile.getvalue()
       st.subheader("Graph Image View")
       leftColumn, centerColumn,rightColumn = st.columns(3)
       with centerColumn:
          st.image(bytes_data)
       graphType = identifyGraphType(bytes_data)
       st.write(f"The graph you uploaded is a {graphType}. We will now extract the coordinate points for your graph.")
       st.subheader("Graph Coordinates View")
       coordinates = extractGraphCoordinates(bytes_data)
       coordinates = eval(coordinates)
       coordinatesDf = pd.DataFrame(coordinates, columns=['x_axis', 'y_axis', 'coordinate point color'])
       st.write("Below is the dataframe which contains all the coordinate points for the points in the graph.")
       leftColumn, centerColumn,rightColumn = st.columns(3)
       with centerColumn:
          st.dataframe(coordinatesDf)
       csv = getCSVFile(coordinatesDf)
       graphFileName = graphFile.name.split(':')[0]
       csvFileName = graphFileName + "extractedPoints.csv"
       st.download_button("Download Data Points (CSV)", csv, csvFileName)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Graph Ingestion Engine</h1>", unsafe_allow_html=True)
    st.write("This is the Graph Ingestion Engine (GIE) application built using Generative AI approach. Please upload an image of the graph you wish to parse. **Note:** the system currently accepts line graphs and scatter plots.")
    #configuring the Gemini Flash model
    configureGemini()
    #the method below is called to upload graph images to the app
    uploadGraphImage()