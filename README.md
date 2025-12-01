# RE-Final-Project-DS2022

Case–study clarity; data/arch diagrams; tradeoffs; limita-
tions; next steps.

1) Executive Summary
Problem: There are many people that are not familiar with coding, however, need to work with data for their job or are interested in understanding a particular data set. 
Solution: In my web app, I allow users to upload their CSV files, store it in a gallery, and see a summary of some information about the data including shape, column names, number of nulls, and number of duplicates. These functions are for users that are not familiar with cleaning data coding and wish to understand how clean their data is. From the summary page, the user can identify quickly if they need to look further into the code if there is an abnormally high number of nulls or duplicates. 

2) System Overview
Course Concept(s): I used Azure's blob storage containers, taught in Case 7, to store the user's uploaded CSV files. These files are stored in the gallery on the gallery page, and are accessed in the summary page when generating a summary of the data. 
Architecture Diagram: Include a PNG in /assets and embed it here.
Data/Models/Services: For my testdata, I used a data set from Kaggle called "Messy-dataset" by user eyowhite (permalink: https://github.com/eyowhite/Messy-dataset/blob/feded56bde2cc1bd72455fc8842866ac3a67090a/messy_HR_data.csv). 

3) How to Run (Local)
I chose to use Docker:
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY assets .
ENV AZURE_STORAGE_CONNECTION_STRING='PASTE-CONNECTION-STRING-FROM-ENV'
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]

4) Design Decisions

Why this concept? Alternatives considered and why not chosen.
Tradeoffs: Performance, cost, complexity, maintainability.
Security/Privacy: Secrets mgmt, input validation, PII handling.
Ops: Logs/metrics, scaling considerations, known limitations.

5) Results & Evaluation
Screenshots or sample outputs (place assets in /assets).
Brief performance notes or resource footprint (if relevant).
Validation/tests performed and outcomes.

6) What’s Next
I would like to extend my summary page to include other cleaning coding functions so that the user further understands their dataset. For the null values, I would like to add a function that prints the dataframe fragment of the rows that contain the null values. I would also like to incorporate an AI model that based on the summary information can determine why there may be null values or duplicates (e.g. during a particular time period there is a lack of data in particular columns). 