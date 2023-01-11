# Data-Co-Global-Supply-Chain-Analysis-and-Late-Delivery-Prediction

## Project Description
* This project is an analysis of the products sold by DataCo Global to consumers and corporates, and their supply chain statistics. 
* The dataset contains information about product details (name, description, price, etc), shipping details (estimated/real shipping time), late delivery risk, delivery status, and customer details. 
* The data covers products in the Clothing, Sports, and Electronic Supplies categories, and has 53 columns and 180520 rows. 
* Each row of the dataset refers to one purchase made by a customer along with that purchase's supply chain statistics.

## Notebook Description
The notebook is organized into the following sections:

### 1. Data Cleaning and Data Wrangling
This step is important for better readability of the data and making it ready for analysis.

### 2. Exploratory Data Analysis
The Exploratory Data Analysis section includes the following:

* Simple frequency plots showing distribution of orders vs various features
* EDA for Late Days - Delayed Deliveries
* Temporal Analysis
* Geographical Analysis

### 3. Building Classifiers
Different classifiers are built with appropriate feature selection to predict the late delivery risk which will help the company in making better decisions and improving its supply chain.


## Evaluation Metric
The evaluation metric for the classifier will be the `accuracy` of the model in predicting the late delivery risk.

