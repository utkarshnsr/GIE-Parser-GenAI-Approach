# GIE-Parser-GenAI-Approach

This is a Generative AI based approach for the Graph Ingestion Engine project. Overall, the goal of the project is to build a system that can:

- Reverse engineer data-points from graph
- Create aural representations of the data

By building this application we are trying to address the problem of making online graph more accessible. The application is meant for individuals such as scientists, teachers, and webmasters interested in improving the accessibility of their graphs. 

Lately, I have been working on this sample prototype using Streamlit framework for the frontend and free tier version of the Google’s Gemini 1.5 flash model for parsing the information in the inputted graphs. 

## Project Setup 

Below are the things that need to be done to run this prototype application locally. 

- Install all the required Python libraries using the requirements.txt file <br /> <br />
  `pip install -r requirements.txt`

- Create a `.env` file in the folder locally to store your [Gemini API KEY](https://ai.google.dev/gemini-api/docs/api-key). Inside the file put the following: <br /> <br />
`GOOGLE_API_KEY = "YOUR API KEY"`

- Run the `Streamlit` application <br /> <br /> 
`streamlit run app.py`


