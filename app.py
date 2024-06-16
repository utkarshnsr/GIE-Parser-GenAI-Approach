import streamlit as st
import PIL.Image
from PIL import Image
import google.generativeai as genai
import ast
import io
import pandas as pd
import os
from dotenv import load_dotenv
import re


def configureGemini():
   load_dotenv()
   GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
   genai.configure(api_key=GOOGLE_API_KEY)


def identifyGraphType(imgPath):
  prompt = """
    For the graph image that is uploaded, I want you to do the following: 

    1) first identify what type of graph it is (line, bar, pie, etc)

    Just return the answer as a string. Here is an example:

    if the graph is a bar graph then return Bar Graph
    if the graph is a scatter plot then return Scatter Plot
    if the graph is a pie chart then return Pie Chart
    if the graph is a line graph then return Line Graph
    if the image is not a graph then return "notagraph" string
    """
  model = genai.GenerativeModel('gemini-1.5-flash')
  img = Image.open(io.BytesIO(imgPath))
  response = model.generate_content([prompt, img])
  formattedResponse = re.sub(r'[^a-zA-Z0-9]', '', str(response.text))
  return formattedResponse


def extractScatterPlotPoints(imgBytesData):
  prompt = """
    For the scatter plot graph image that is uploaded, I want you to do the following: 

    1) for each point on the graph, get its x coordinate, y coordinate, and the point color (only the name NOT the rgb or hexcode value)
    2) put the information for each point into a list

    return the list only (NO OTHER WORDS). Here is an example:

    [(1,2, "red"), (3,4, "black")] 
    """
  model = genai.GenerativeModel('gemini-1.5-flash')
  img = Image.open(io.BytesIO(imgBytesData))
  response = model.generate_content([prompt, img])
  return response.text


def extractLineGraphPoints(imgBytesData):
   prompt = """
    For the line graph image that is uploaded, I want you to do the following: 

    1) for each important points on the graph, get the x coordinate, y coordinate, and the point color (only the name NOT the rgb or hexcode value)
    2) put the information for each point into a list

    return the list only (NO OTHER WORDS). Here is an example:

    [(1,2, "red"), (3,4, "black")] 
    """
   model = genai.GenerativeModel('gemini-1.5-flash')
   img = Image.open(io.BytesIO(imgBytesData))
   response = model.generate_content([prompt, img])
   return response.text

def extractBarGraphPoints(imgBytesData):
   prompt = """
    For the bar graph image that is uploaded, I want you to do the following: 

    1) for each bar get the x value, y value, and the bar color (only the name NOT the rgb or hexcode value)
    2) put the information for each bar into a list

    return the list only (NO OTHER WORDS). Here is an example:

    [("golf",6, "red"), ("tennis",14, "yellow")] 
    """
   model = genai.GenerativeModel('gemini-1.5-flash')
   img = Image.open(io.BytesIO(imgBytesData))
   response = model.generate_content([prompt, img])
   return response.text

def extractPieChartPoints(imgBytesData):
   prompt = """
    For the pie chart image that is uploaded, I want you to do the following: 

    1) for each pie in the pie chart get the name of the category, the percentage the category takes up, and the color of the pie (only the name NOT the rgb or hexcode value)
    2) ensure that all the percentages for the pies combined add to up 100%
    3) put the information for each bar into a list
    
    return the list only (NO OTHER WORDS). Here is an example:

    [("language",30, "red"), ("math",40, "yellow")] 
    """
   model = genai.GenerativeModel('gemini-1.5-flash')
   img = Image.open(io.BytesIO(imgBytesData))
   response = model.generate_content([prompt, img])
   return response.text

def getCSVFile(df):
   csv = df.to_csv(index=False).encode('utf-8')
   return csv

def parseAppropriateGraph(graphType, imgBytesData):
   if (graphType == "BarGraph"):
      st.write(f"The graph you uploaded is a bar graph. We will now extract the coordinate points for your graph.")
      st.subheader(f"Coordinates View of Your Bar Graph")
      coordinates = extractBarGraphPoints(imgBytesData)
      coordinates = eval(coordinates)
      coordinatesDf = pd.DataFrame(coordinates, columns=['bar name', 'y_axis value', 'bar point color'])
      return coordinatesDf
   elif (graphType == "ScatterPlot"):
      st.write(f"The graph you uploaded is a scatter plot. We will now extract the coordinate points for your graph.")
      st.subheader(f"Coordinates View of Your Scatter Plot")
      coordinates = extractScatterPlotPoints(imgBytesData)
      coordinates = eval(coordinates)
      coordinatesDf = pd.DataFrame(coordinates, columns=['x_axis', 'y_axis', 'coordinate point color'])
      return coordinatesDf
   elif (graphType == "PieChart"):
      st.write(f"The graph you uploaded is a pie chart. We will now extract the coordinate points for your graph.")
      st.subheader(f"Coordinates View of Your Pie Chart")
      coordinates = extractPieChartPoints(imgBytesData)
      coordinates = eval(coordinates)
      coordinatesDf = pd.DataFrame(coordinates, columns=['category name', 'percentage', 'category color'])
      return coordinatesDf
   elif (graphType == "LineGraph"):
      st.write(f"The graph you uploaded is a line graph. We will now extract the coordinate points for your graph.")
      st.subheader(f"Coordinates View of Your Line Graph")
      coordinates = extractLineGraphPoints(imgBytesData)
      coordinates = eval(coordinates)
      coordinatesDf = pd.DataFrame(coordinates, columns=['x_axis', 'y_axis', 'coordinate point color'])
      return coordinatesDf
   else:
      st.warning("The image you inputted is not a supported graph type.")
      return None
      

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
       graphType = str(graphType)
       coordinatesDf = parseAppropriateGraph(graphType, bytes_data)
       if coordinatesDf is not None:
            st.write("Below is the dataframe which contains all the coordinate points for the points in the graph.")
            leftColumn, centerColumn,rightColumn = st.columns(3)
            with centerColumn:
                st.dataframe(coordinatesDf)
            csv = getCSVFile(coordinatesDf)
            graphFileName = graphFile.name.split('.')[0]
            csvFileName = graphFileName + "extractedPoints.csv"
            st.download_button("Download Data Points (CSV)", csv, csvFileName)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Graph Ingestion Engine (GIE)</h1>", unsafe_allow_html=True)
    st.write("This is the GIE application built using Generative AI approach. Please upload an image of the graph you wish to parse. **Note:** The system accepts the following graph types:")
    st.image("images/acceptedGraphTypes.png",width=700)
    #configuring the Gemini Flash model
    configureGemini()
    #the method below is called to upload graph images to the app
    uploadGraphImage()