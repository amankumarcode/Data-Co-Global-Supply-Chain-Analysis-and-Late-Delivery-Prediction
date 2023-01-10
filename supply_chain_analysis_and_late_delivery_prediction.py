# -*- coding: utf-8 -*-
"""Supply Chain Analysis and Late Delivery Prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Il8v0CSminrgpnkA2qUBBWKNV-tDY0yq

# **Welcome to CIS545 Project, Spring 2022**
## **Group 95**

**Group Members:**
 
1.   Karne Chaithanya Sai 
2.   Aman Kumar 
**Pointers:**
*   We are using our own dataset for this project. This dataset contains the data about the products sold by DataCo Global to consumers and corporates majorly and their supply chain statistics.

*   Product details (name description, price etc), shipping details (estimated/real shipping time), late delivery risk, delivery status etc., and the customer details are included in the dataset.

*   It contains the statistical data of Clothing, Sports, and Electronic Supplies related products. The data has 53 columns and 180520 rows.

*  Each row of the dataset refers to one purchase made by the customer along with that purchase's supply chain statistics.

*  The dataset can be found [here](https://data.mendeley.com/datasets/8gx2fvg2k6/5). **The dataset needs to be uploaded on colab session storage for all of the code cells to run.**

*  The description file for this dataset can be found [here](https://drive.google.com/file/d/1YAlnk9-dFhkB-OOd-MyEKRrZZP8Xywcz/view?usp=sharing)

First it is important to load all the required libraries for our project implementation
"""

!pip install pandasql

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
import chardet
import pandasql as ps

"""We need to find the type of encoding used for our dataset. The following code gives the encoding of the dataset."""

with open("DataCoSupplyChainDataset.csv", 'rb') as rawdata:
    result = chardet.detect(rawdata.read(100000))
result

"""Let us now read our dataset into a dataframe called "df" with the above obtained encoding"""

df = pd.read_csv("DataCoSupplyChainDataset.csv", encoding="ISO-8859-1")

"""Let us look at the first 5 rows of the dataset to get an idea of how the dataset looks"""

df.head()

"""We will now generate the descriptive statistics of our dataset df"""

df.describe()

"""# **Data Cleaning and Data Wrangling**

It is very important first to clean our dataset and making it ready for analysis.

Here we will:

1.   Clean the 'Customer Country' column as it contains some encrypted country names. Ex: Change 'EE.UU.' to USA for better readabiliy.
2.  Clean the 'Order Country' column as it contains some encrypted country names. Ex: Change 'Estados Unidos' to USA for better readabiliy.
3.   Drop columns - 'Category Id', 'Customer Email', 'Customer Fname', 'Customer Id', 'Customer Lname', 'Customer Password', 'Department Id', 'Order Id', 'Order Item Cardprod Id', 'Order Item Id', 'Order Item Total', 'Order Profit Per Order', 'Product Card Id', 'Product Category Id', 'Product Description', 'Product Image' as these are not useful for our analysis and are redundant.

We can observe from the following heatmap that the the "Product Description" column is completely empty and thus can be dropped.
"""

plt.figure(figsize=(18,12))
plt.title("Heat Map of Null Values", fontdict={'fontsize': 18})
sns.heatmap(df.isnull(), cbar=True, cmap = "RdYlBu")
plt.xlabel("Feature")
plt.ylabel("Number of data points/orders")

"""We plot the correlation map to get the redundant columns. The redundant column have perfect correlation with another column. And following columns have correlation of 1 between each other:

1.   Order Profit Per Order and Benefit Per Order.
2.   Order Item Total and Sales per customer.
3.   Category Id and Product Category Id
4.   Order Customer Id and Customer Id
5.   Order Id and Order Item Id


"""

plt.figure(figsize=(30,15))
correlation_map = df.corr()
map=sns.heatmap(df[correlation_map.index].corr(),annot=True,cmap="YlGnBu")

# Cleaning the 'Customer Country' and Order Country columns

df['Customer Country'] = df['Customer Country'].apply(lambda x: x.replace('EE. UU.', 'USA') if x == 'EE. UU.' else x)
df['Order Country'] = df['Order Country'].apply(lambda x: x.replace('Estados Unidos', 'USA') if x == 'Estados Unidos' else x)

# Dropping the unwanted columns

df.drop(columns=['Category Id', 'Customer Email', 'Customer Fname', 'Customer Id', 'Customer Lname', 'Customer Password', 'Department Id', 'Order Id', 'Order Item Cardprod Id', 
                 'Order Item Id', 'Order Item Total', 'Order Profit Per Order', 'Product Card Id', 'Product Category Id', 'Product Description', 'Product Image'], inplace=True)

# Looking at the shape of the final df after removing 16 columns and cleaning the 'Customer Country' column

df.shape

df.columns

df.head(1)

"""# **3. Exploratory Data Analysis**

### **3.1 Simple frequency plots showing distribution of orders vs various features**

1.  A bar chart showing the Type of Transcations vs Number of Orders
2.  A bar chart showing the Delivery Status vs Number of Orders
3.  A bar chart showing the Product Category Name vs Number of Orders
4.  A bar chart showing the Order Status vs Number of Orders
"""

# A bar chart showing the Type of Transcations vs Number of Orders

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(22,14))

ax[0,0].bar(list(df['Type'].value_counts().index), df['Type'].value_counts(), color = "orange")
ax[0,0].set_xlabel("Transaction Type")
ax[0,0].set_ylabel("Number of Orders")
ax[0,0].set_title("Transaction Type vs Number of orders")

# A bar chart showing the Delivery Status vs Number of Orders

ax[0,1].bar(list(df['Delivery Status'].value_counts().index), df['Delivery Status'].value_counts(), color = "orange")
ax[0,1].set_xlabel("Delivery Status")
ax[0,1].set_ylabel("Number of Orders")
ax[0,1].set_title("Delivery Status vs Number of orders")

# A bar chart showing the Category Name vs Number of Orders

ax[1,0].bar(list(df['Category Name'].value_counts().index), df['Category Name'].value_counts(), color = "orange")
ax[1,0].set_xticklabels(labels = list(df['Category Name'].value_counts().index),rotation=90)
ax[1,0].set_xlabel("Category Name")
ax[1,0].set_ylabel("Number of Orders")
ax[1,0].set_title("Category Name vs Number of orders")

# A bar chart showing the Order Status vs Number of Orders

ax[1,1].bar(list(df['Order Status'].value_counts().index), df['Order Status'].value_counts(), color = "orange")
ax[1,1].set_xticklabels(labels = list(df['Order Status'].value_counts().index),rotation=45)
ax[1,1].set_xlabel("Order Status")
ax[1,1].set_ylabel("Number of Orders")
ax[1,1].set_title("Order Status vs Number of orders")

"""###**Insights from 3.1**

1.  We can see that most of the orders placed were made using debit card transactions. 
2.  Majority of the deliveries are late deliveries, but complete. 
3.  The top 5 product categires bought were Cleats, Mens Footwear, Women's Apparel, Indoor/Outdoor Games and Fishing

### **3.2 EDA for Late Days - Delayed Deliveries**

### **3.2.1 Which product categories are getting delivered late the most?**

We first need to consider only late delivery data here and perform our analysis on that
"""

from IPython.core.pylabtools import figsize
# Subsetting only late delivery data

late_df = df[df['Late_delivery_risk'] == 1]

# Plotting late deliveries for product categories

fig, ax = plt.subplots(figsize = (10,10))
ax.bar(list(late_df['Category Name'].value_counts().index), late_df['Category Name'].value_counts())
ax.set_xticklabels(labels = list(late_df['Category Name'].value_counts().index), rotation = 90)
plt.show()

"""### **3.2.2 Which destination countries are getting the most late deliveries?**

Now the orders are being placed from two countries which are USA and Puerto Rico. We will try to find which destination countries are receiving the products late the most from both USA and Puerto Rico.

*  Lets use pandasql for this


"""

late_df.head(1)

# Subsetting data of late deliveries from USA to various countries round the world

late_df_usa = late_df[late_df['Customer Country'] == 'USA']
late_df_usa.rename(columns = {'Order Country':'Order_Country'}, inplace = True)

# Subsetting data of late deliveries from Puerto Rico to various countries round the world

late_df_puertorico = late_df[late_df['Customer Country'] == 'Puerto Rico']
late_df_puertorico.rename(columns = {'Order Country':'Order_Country'}, inplace = True)

query1 = """SELECT Order_Country, COUNT(*) AS Orders
            FROM late_df_usa
            GROUP BY Order_Country
            ORDER BY Orders DESC
            LIMIT 5"""

late_df_usa_final = ps.sqldf(query1)

query2 = """SELECT Order_Country, COUNT(*) AS Orders
            FROM late_df_puertorico
            GROUP BY Order_Country
            ORDER BY Orders DESC
            LIMIT 5"""

late_df_puertorico_final = ps.sqldf(query2)

# Plotting late days

fig, ax = plt.subplots(nrows=1, ncols=2, figsize = (12,6))

ax[0].bar(late_df_usa_final['Order_Country'], late_df_usa_final['Orders'], color = "red") 
ax[1].bar(late_df_puertorico_final['Order_Country'], late_df_puertorico_final['Orders'], color = "red") 
ax[0].set_xlabel("Destination Country")
ax[0].set_ylabel("Number of late deliveries")
ax[1].set_xlabel("Destination Country")
ax[1].set_ylabel("Number of late deliveries")

"""### **Insights From 3.2.2**

When orders are placed from both USA and Puerto Rico, the destination countries excluding USA which receive delayed deliveries are France, Mexico, Alemenia and Australia

### **3.2.3**

Delivery statistics by shipping mode

Lets understand how the delivery time varied according to the Shipping Mode selected by the customers.
"""

# Plot showing deliveries made based on shipping mode

df.rename(columns = {'Shipping Mode':'Shipping_Mode'}, inplace = True)
late_df.rename(columns = {'Shipping Mode':'Shipping_Mode'}, inplace = True)

query1 = """SELECT Shipping_Mode, COUNT(*) as Total_Deliveries
            FROM df
            GROUP BY Shipping_Mode"""

total_deliveries_sm = ps.sqldf(query1)

query2 = """SELECT Shipping_Mode, COUNT(*) as Late_Deliveries
            FROM late_df
            GROUP BY Shipping_Mode"""

late_deliveries_sm = ps.sqldf(query2)

query3 = """SELECT total_deliveries_sm.Shipping_Mode, total_deliveries_sm.Total_Deliveries, late_deliveries_sm.Late_Deliveries
            FROM total_deliveries_sm
            JOIN late_deliveries_sm
            ON total_deliveries_sm.Shipping_Mode = late_deliveries_sm.Shipping_Mode"""

final_sm = ps.sqldf(query3)
final_sm['LD_%'] = final_sm['Late_Deliveries']/final_sm['Total_Deliveries']*100


fig, ax = plt.subplots(1, 2, figsize = (15,7.5))

sns.countplot(x = df['Shipping_Mode'], hue = df['Delivery Status'], data = df, ax=ax[0])
sns.barplot(final_sm['Shipping_Mode'], final_sm['LD_%'], ax=ax[1])
ax[0].set_xlabel("Shipping Mode")
ax[0].set_ylabel("Number of deliveries")
ax[1].set_xlabel("Shipping Mode")
ax[1].set_ylabel("% of Late Deliveries")
plt.show()

"""### **Insights from 3.2.3**

1.   Standard Class Shipping Mode has the lowest % of late deliveries of about ~40%, and First Class Shipping Mode had the highest % of late deliveries of about ~95%.
2.   First Class Shipping Mode has no deliveries that were shipped in advance or shipped on time. All the deliveries were either late or cancelled.
3.  For Same Day Delivery Shipping Mode, there were more number of deliveries that were shipped on time than those that were shipped late. For Same Day Delivery, the supply chain tried harder to deliver on time.

### **3.3 Temporal Analysis**

It is very important especially in supply chain to understand how the orders are being place based on time.
*  There is a date column in our dataset called order date (DateOrders) which tells us the date on which the order was placed.
*  Let us plot the frequency of orders placed every year, every month, every hour of day and every day of week.
"""

# Let us convert the column 'order date (DateOrders)' to a datetime object, a new column called 'date' to make it useful for analysis

df['date'] = df['order date (DateOrders)'].apply(lambda x: dt.datetime.strptime(x, "%m/%d/%Y %H:%M"))

# Let us now extract day, month, year, hour and day name from the date created above

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['hour'] = df['date'].dt.hour
df['weekday'] = df['date'].dt.day_name()

# Let us plot the distribution of orders placed by Year, Month, Hour and Day Name

fig, ax = plt.subplots(nrows=2, ncols=2, figsize = (14,12))

ax[0, 0].bar(list(df['year'].value_counts().index), df['year'].value_counts(), color = "blue")

ax[0, 1].bar(list(df['month'].value_counts().index), df['month'].value_counts(), color = "blue") 

ax[1, 0].bar(list(df['hour'].value_counts().index), df['hour'].value_counts(), color = "blue") 

ax[1, 1].bar(list(df['weekday'].value_counts().index), df['weekday'].value_counts(), color = "blue")

"""### **3.4 Geographical Analysis**

The following map displays destination countries that have given the company most profit.
"""

geo_map = df.groupby(['Order Country'])['Benefit per order'].sum().reset_index(name='Total_Profit')
geo_map = geo_map.sort_values(by= 'Total_Profit', ascending= False)
geo_map.head()

import plotly.express as px

fig = px.choropleth(geo_map ,  locationmode='country names', locations='Order Country',
                    color='Total_Profit', 
                    hover_name='Order Country')

fig.show()

"""# **4. Building Classifiers**

Let us build a classifier to predict the late delivery risk, given some of the chosen features as inputs for the model.

First let us build a **Naive Bayes** model to predict the late delivery risk.

Let us the choose the columns that we will use to build our model here.

**Predictor Columns:**

1.   Type
2.   Days For Shipment (Scheduled)
3.   Sales Per Customer (processed below)
4.   Market
5.   Order Item Quantity
6.   Order Status
7.   Shipping Mode

**Prediction Column**

1.   Late Delivery Risk
"""

#We will look at the our label Late Delivery Risk using histogram
#sns.histplot(df["Late_delivery_risk"], fill=True) 
plt.xlabel("Labels")
plt.ylabel("Count")
df["Late_delivery_risk"].value_counts().plot(kind = 'bar')

"""We can see that the target variable is fairly balanced. 1 - Late Delivery, 0 - Delivery on time."""

# Let us look at the distribution of the 'Sales per customer' column using a histogram

fig, ax = plt.subplots()
ax.hist(df['Sales per customer'], bins = 10)

df['Sales per customer'].describe()

"""From the histogram let us divide the values in the 'Sales per customer' column into three groups

1.  7.4 dollars - 201 dollars as (Less than 201 dollars)
2.  201 - 394 as (201 dollars - 394 dollars)
3.   More than 394 dollars as (Greater than 394 dollars)
"""

# Create a function to convert each value in the 'Sales per customer' column to the corresponding group

def group(x):
  if int(x)<= 201:
    return 'Less than $201'
  elif int(x) >201 and int(x) <=394:
    return '$201 - $394'
  else:
    return 'Greater than $394'

# Convert each value in the 'Sales per customer' column to the corresponding group

df['Sales_per_customer_refined'] = df['Sales per customer'].apply(lambda x: group(x))

"""Let us now create a subset of the main dataframe df to create a new dataframe df_model which we will use for our modelling purposes.

Let us subset the columns mentioned above which we will use for this modelling.
"""

df_model = df[['Type', 'Days for shipment (scheduled)', 'Sales_per_customer_refined', 'Market', 'Order Item Quantity', 'Order Status', 'Shipping_Mode', 'Late_delivery_risk']]

"""Let us look at the dataset that we will be usning for our modeling"""

df_model.tail()

"""**Ordinal Encoding** of the 'Sales_per_customer_refined' column."""

from sklearn.preprocessing import OrdinalEncoder

ord_enc = OrdinalEncoder(categories=[['Less than $201', '$201 - $394', 'Greater than $394']])
df_model['Sales_per_customer_refined'] = ord_enc.fit_transform(df_model[['Sales_per_customer_refined']])
# ordinal_encoded_df = pd.DataFrame(b)
# ordinal_encoded_df
df_model['Sales_per_customer_refined']

"""**OneHotEncoding of the other columns**"""

from sklearn.preprocessing import OneHotEncoder

enc = OneHotEncoder()
a = enc.fit_transform(df_model[['Type', 'Days for shipment (scheduled)', 'Market', 'Order Item Quantity', 'Order Status', 'Shipping_Mode']]).toarray()
encoded_df = pd.DataFrame(a)
encoded_df

"""Combining both the ordinal encoded and onehotencoded dataframes to form the final_model_data dataframe which we will use for our analysis."""

final_model_data = pd.concat([encoded_df, df_model[['Sales_per_customer_refined']]], axis=1, join='inner')
final = pd.concat([final_model_data, df_model[['Late_delivery_risk']]], axis=1, join='inner')
final

"""Lets now split our dataset into train and test splits"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(final.drop(columns = 'Late_delivery_risk'), final['Late_delivery_risk'], test_size = 0.3, random_state = 42)

"""Now, we train and fit two models.

1.   Categorical Naive Bayes
2.   Gaussian Naive Bayes


"""

from sklearn.naive_bayes import CategoricalNB
from sklearn.naive_bayes import GaussianNB

# Declaring both the models
cnb = CategoricalNB()
gnb = GaussianNB()

# Fitting both the models on the training dataset
cnb.fit(X_train, y_train)
gnb.fit(X_train, y_train)

# Predicting on X_test

pred_cnb = cnb.predict(X_test)
pred_gnb = gnb.predict(X_test)

pred_cnb

pred_gnb

"""Let us now find out the **Accuracies** of our models"""

from sklearn.metrics import accuracy_score

cnb_accuracy = accuracy_score(y_test, pred_cnb)
cnb_accuracy

gnb_accuracy = accuracy_score(y_test, pred_gnb)
gnb_accuracy

"""We can see that the categorical Naive Bayes is more accurate with 70% accuracy.

**This is because our data which we used for this modeling is a categorical dataset. So Categorical Naive Bayes should give higher accuracy, which is what we obtained**

Let us find out the **Recall, Precision and F1 scores** of the Categorical Naive Bayes model
"""

from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

recall = recall_score(y_test, pred_cnb)
precision = precision_score(y_test, pred_cnb)
f1_score = f1_score(y_test, pred_cnb)

print('the recall score is {}'.format(recall))
print('the precision score is {}'.format(precision))
print('the f1 score score is {}'.format(f1_score))

"""**High Precision score here tells that the False Positives are less, meaning that the model is not predicting orders as Late deliveries if they are actually not late deliveries. This is a very good thing especially in the supply chain space. We dont want to predict orders that are on time as late deliveries, which is exactly what our model is doing**

Let us also print the **Classification Report** for the Categorical Naive Bayes Model.
"""

from sklearn.metrics import classification_report

print(classification_report(y_test, pred_cnb))

"""Let us also plot the **Confusion Matrix** for the Categorical Naive Bayes Model"""

from sklearn.metrics import confusion_matrix

conf_matr = confusion_matrix(y_test, pred_cnb)
fig, ax = plt.subplots()
ax = sns.heatmap(conf_matr, annot=True, cmap="Blues")

"""**Now let's try some sophisticated models like a Random Forest. The list of models that we are going to try next:**

1.   Logistic Regression
2.   Random Forest

We will use Logistic Regression as a baseline classifier.

Lets look at our cleaned dataset.
"""

print(df.shape)
df.head(3)

"""We will extract numeric and categorical columns and select the one's that we require for training."""

numeric_df = df.select_dtypes(include=[np.number])
categorical_df = df.select_dtypes(exclude=[np.number])
numeric_df.head(2)

categorical_df.head(2)

"""After glancing over all the numeric and categorical features we remove the features that are irrelevant or are almost perfectly correlated to the other features and thus we boil down to following features for our classification model:
 

1.   Market
2.   Order Country
3.   Customer Segment
4.   Type
5.   Shipping_Mode
6.   Benefit per order (Basically Profit Per Order)
7.   Latitude
8.   Longitude
9.   Days for shipment (scheduled)
10.  Order Status
11.  Order Item Quantity


"""

cat_columns = ['Order Country', 'Customer Segment', 'Type','Shipping_Mode','Market','Order Status']
num_columns = ['Benefit per order','Latitude','Longitude','Days for shipment (scheduled)','Order Item Quantity']
df_cat = df[cat_columns]
df_num = df[num_columns]
target_col = df[['Late_delivery_risk']]

df_cat.head(1)

df_num.head(1)

"""We will use a Label encoder for categorical variable, due to purposes of using feature selection using Random Forest. Though, a one hot encoder will perform equivalently well on this dataset."""

from sklearn.preprocessing import LabelEncoder
LE = LabelEncoder()
def LE_features(sdf):
    sdf=LE.fit_transform(sdf)
    return sdf

df_cat = df_cat.apply(LE_features)
# df_cat = pd.get_dummies(df_cat)
# df_cat.head(1)

training_dataset = pd.concat([df_num,df_cat, target_col], axis=1, join='inner') 
training_dataset.head(1)

"""We shuffle our dataset."""

#Shuffle our dataset
training_dataset = training_dataset.sample(frac=1)
training_dataset.head(1)

training_dataset_final = training_dataset
train_X, test_X, train_y, test_y = train_test_split(training_dataset_final.drop(columns = 'Late_delivery_risk'), training_dataset_final['Late_delivery_risk'], test_size = 0.2, random_state = 42)

"""**Logistic Regression**"""

#Accuracy Score of Test data
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression().fit(train_X, train_y)
clf.score(test_X, test_y)

pred_lr = clf.predict(test_X) 
recall = recall_score(test_y, pred_lr)
precision = precision_score(test_y, pred_lr)

print('the recall score is {}'.format(recall))
print('the precision score is {}'.format(precision))
print(classification_report(test_y, pred_lr))

"""**Random Forest**"""

#Accuracy Score of Test Data
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(train_X, train_y)
rf.score(test_X,test_y)

pred_rf = rf.predict(test_X) 
recall = recall_score(test_y, pred_rf)
precision = precision_score(test_y, pred_rf)

print('the recall score is {}'.format(recall))
print('the precision score is {}'.format(precision))
print(classification_report(test_y, pred_rf))

feature_scores = pd.Series(rf.feature_importances_, index=train_X.columns).sort_values(ascending=False)
feature_scores

"""Feature Scores Visualization using Random Forest. Latitude and Longitude are the best features to predict late delivery."""

sorted = rf.feature_importances_.argsort()
plt.figure(figsize=(8,8))
plt.barh(training_dataset.columns[sorted], rf.feature_importances_[sorted])
plt.xlabel("Feature Importance using Random Forest")

"""Now referring the above graph, we will again perform feature selection for our model. In this case we will remove the features with feature importance score of less than 5%. Therefore we will remove features "Customer Segment","Type","Order Item Quantity","Market" and train our model."""

#Accuracy score of test data
rf2 = RandomForestClassifier()
rf2.fit(train_X.drop(columns = ["Customer Segment","Type","Order Item Quantity","Market"]), train_y)
rf2.score(test_X.drop(columns = ["Customer Segment","Type","Order Item Quantity","Market"]),test_y)

pred_rf2 = rf2.predict(test_X.drop(columns = ["Customer Segment","Type","Order Item Quantity","Market"])) 
recall = recall_score(test_y, pred_rf2)
precision = precision_score(test_y, pred_rf2)

print('the recall score is {}'.format(recall))
print('the precision score is {}'.format(precision))
print(classification_report(test_y, pred_rf2))

"""# Conclusion

We tried multiple models from Gaussian Naive Bayes to Random Forest. Some insights we obtained are as follows:

1.   Categorical Naive Bayes outperformed Gaussian Naive Bayes as there is lot of categorical data in our dataset.
2.   Random Forest classifier performed the best among all classifier with F1 score of 0.85. Thus showing us that bagging works great on this dataset.
3.   We could discard some of the features by visualizing feature importance thus improving our model and reducing computation.

# Challenges



1.   Since there are too many rows and features,especially when we one hot encode the categorical columns; hyperparameter tuning of the model becomes time consuming.
2.   On analysis we found that the dataset is perfectly balanced on many features thus it becomes a challenging task to derive interesting insights via visualization. 
3.   Choosing right set of features is a tricky task. For our case we selected final features based on feature importance scores but there other techniques like SHAP feature selection that can be used but due to time constraints we didn't delve in that direction.

# Future Work
Some interesting ideas that we can work on in future:

1.   Analyzing and predicting the "suspected fraud" label in the order status column can help the company plan better.
2.   Customer Segmentation and Audience Analysis using additional datasets like census data.
3.   Some more visualizations like top routes can be plotted using a georgraphical map.

![th.jpg](data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAoHBwkHBgoJCAkLCwoMDxkQDw4ODx4WFxIZJCAmJSMgIyIoLTkwKCo2KyIjMkQyNjs9QEBAJjBGS0U+Sjk/QD3/2wBDAQsLCw8NDx0QEB09KSMpPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT3/wAARCACmAKcDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwCyTzSE/lQeKglkP3cU7CGzfMcjNLG2KZnntUqtnpj8qYhxOab16UvPWlPygYpDFGQaYxOacrHrTWdt3pTQh23IB5obPY03cTjmlP1oAtJazfZPPLr5Y/h3c/lUEuMZJ4qwLNBZeebhN2P9X3qCQ5THrWUHe5pJWsQEr/dpAoYdCPxpNq5xv59KaykE4wa1MywkZC45x9aNuDjNRI7nsQadvIIzmkxoXBBxmhsY5NDtyOaQYORQgZXYsGyvSpo5S687s+9RSkxHgnFIkhI7/nVCLikjr/Oiq0cmMgnP1opWC5Ybcc5xVVy2496keVicAmowp3c55oAVVJqwq4HWowhU5DVIAccnNACnsKU0zJzSj1zSGKOBSEck0pY+tN39R8v50xB1IpkpwPenZxj0PeiQDjJFAFiG0hay+0fak8zH+q700n5c9faltUtRbuXL+b22jj8ab14rON7u5crWQ3eg9jTSykdacY17io2gz0BFaEEijpx+OaRx7VGBIg4zgU9Se9DBCkbgPWkx7U4HnFJkdKQyKbAXkbvaoVbHUBfoKst0700N2Zc0xESYJOeT70VPx2GKKYFZR83WpVxu6mog43YAqQFh/DQInG3FIWpFckcqKM57YqWUL1IFOx2qNSetK0uOhoQAykDgEmmbCT90/lThKcdRThL7imIt6ZukuUtmVXjcliHGQAByauwXjreTQWNk0KIw3O8e1XH+ye+M96i0+8j0+yabYJZZD0PG0D+neoLnxC0NjPcyIPlBKIMsCe27HOKyk9bGkVoaV/dW5eKO+CYc8Mo5H41jsAJSEZfvEAbhk1DZ3Ufia3tnlQQu7CZUWQnBU9Cf1xUUdlbRT+YI8uvQkk4pK99Bu1tSd5Mdjn2pomz2YUjSKezf981HvB7MPwrZGRPuBz0pvbiojkcgnP0p43daAHdDS55FMIajkUhkhFQyDHKtipATjmo5sFKaERea5/8A10VXJwetFMRa+UN24pQ3QDFVgrg/MBViI9Mj9KBjyTxjFLg5OcU4su3OKReWHHAqRkirheahPpx1qRpMdhUDu+M4FNADEAdqBKOpFRbmJ+6Ku2FuJN80inZGOPQt2/z9KG7K4kruwk3mJvVgQhH8XIx3/XtWDewXAUeXctsfkoR1962bq+Xay52qD82TkE1kyu9wysf9WTtBBrkudFizopeKdZS4PlDIIPHpWqnejQdKSVWEuBI3GRyAfUVYubSWymMUy8kZDDow9q1g9DOZX3DPUZpjOBySKeYVznB59KiMIY9G4rYzYGRW+7yaVckdKYIVHAJFPGFGBQCEIJNDZxTiSSDimscikMMZHIpvlKRg/wA6eDx7UADNNAVzFg9eKKmaHJ+U/rRTERKvqf1qVVFP2+mKaVPPSlcdgO0nHYU5SAMcZNREZI6U4r7CkArYboRio2PsaaY8HgkCm7W6B6YhSQK0UUtp4AcxRKm52zyxPtWd5bjvV6ZmfSLe2WQLJJu4B+ZsZOKip8JUNzJ3KztHvU4OUIXGR6gGs37ROL9Y0iea4PzIB8zEDknHYdqr60Z7D7OHk3OwYcDoMjjPrUmj3xgiMin55Gw+084HbPpznFYWsjW+p0Nhc3sE+5oGgY5OxxjmummI1bTAwyJ4MkDHX1Fc1/ao2CG7k2j+FpG5UEZwSevSrula0krOykBcgKRwSPUg1SdhPUglLHG1tpqq0cwyfM3evNb+pWiNE13FjAxvUfzrGM8PcHPtXQncyasVgZBnOaelwvQqc+9K8sZ+6WpqsCep/OmSW1KuvSkKio4yc9aex9+KllC7RilCjn1pgNOJxg0AMIx/GRRT9oaincLDcVG7YGPWpGYHPPApm0MakBi8c9TQTnsc1JgEcEU5UA7/AI1QiLHHQ4qNnAPfFTvwOGH41EVU9TTAbuBP/wBapYJFhmSV0DCPLDjp9KAEHGeaRmUD1FJ6gjC1pxfwerRknIGOvaqfhrEc86SqNoAcZPAOcf1q7HpE4luZJp/Mz/qVC4wMnIPvjH61nrILC5LPuAKkEj/CudprRmqaZseKrRWns7hSGjeMjg9GB/TqKNLvVhKq6gY6NWZNrUN5aRRwksA5J45/GomudhyG4Az/AJNIex6Ja3onsZVOcFCOnXisktFzlOar+HdQ3HY7LtAyRn+tXruLybuRIgHQH5Sa1psiZSkaHPyqD+NRh06bSPoakm3nO5AMelRhFxySOa1MyZGGeP51YByKrJGn/PQ5+lWU2YwCaTGgA+anEcfSgqOueKBzj1FSMRWIzRSMp6iimBBktS7sVIMZzRkYPFMCPOaRiPfNTB8dVoMox90ZoEViQcDmgdfarAcHIKinKwz0H1pgQBeM0jA9uM1byPQUjAHtmkBFbxK0yKWwOp/AZrlNbnjWQllwMkE+9devypK2AQI26GuI1wB8jOSTnFY1Hdlx2M+IpG/yttUnqBRdMkpSPDPvPSlstLurt8W8Ej/7WMAfieKuXGi3OmtbvORukXJCnO3n7ufX/Gp21GbujnyIwrbVyADs6Ct65m+ZZNn31Ga5eF2Aj4AHcV0ke6S2hPovrVU9wlsIXDDtn6UwwuxyNopzIeCd2frUL5BON3/fVbmY8wS/3h+VOSOQZyRTF8wHHGD6mplUnqV/OgByqyr1oGfXmnhSO9KRSGM3UUdaKQEe0k9cGk6DluKaScnFBY+ppiEODxmjj1HNIcnj+tAUk9f1pgSKB65pw5IGTimpGQOTUoGOKQCnjjNIcY5pC2DSbs0DHKwBxgYPBz6Vyuu6f9i1EoZFkQ8o46MK6ViWOFzn0A61j6whvdTtrSPLsAI9oHIPVv61jNFRL+jkjT4QqBQAcD2zT9WiSbTSzqpeKRdvOOvFWIIFhITG0KMBTVTU5Y/MSMkZUh/x7U5aRHHcykt55blIlhOzdgtnH5V0agKqqOgGBUMcsL2qeWmdgxnHU9yKerBh0Ip011FLsOb7vXpTTIoyT/KhmA/hNRGUY6D8RWpA8yqfT8qPM5+9wPQVD5qk9Fx9KTzfm4x+VAFgSN13ZHalDsc/NVdpugJbH0pyypjGT+VAE5PviimB0I6mikMaSpbtTWbHTGKjLAdufpTg/HA496YhQ5HO2pUbI5UCoUJYZPSnSTxWyB554YUJwDLIEBPpyaAJ9+O1O3DuKqJqFk7qiX1mztjaouEJJPoM0jalZK5R76yV1OCpuEyD6YzSAt5z2phB/wAKilv7OCRo5r20ikXgo9wikfUE5FOlvbSFEeW7tY1kGULzqoYeoyefwpDHwzNbyiZjgR/NmsvQbvZrM2ozRCUoGVMnGCT1H4fzp2pTW95p7LDqlrArOAJxMjDI5x1/StHTbLRorS3iOuWQdxuw08e5ie+M96xqqO8tjSF+m5NLerdXDSldhbtnNUNT0uHU/JLTSwvGchoyBn2PHNX7/wDsvTfvanZiUY/dvMitg98E5qqby3kt/PWeEwr1lEilB+OcVUHGUfdJkmnqSLGqAKowo4A9KlAAFU47+znO2G9tZWAJISdScDqeD096VNSsShf7fZ7AcE/aEwD271oIsPKig5JwKrNOvI5p8t1ZxQLNJd26QyfcdpVw/wBDnn8KikmtTbi4F3aCAnaJTKu0n0znGaZI0sjEHDGpFkj6kEEVTe5smRiupWOB6Tp/jSxbZ1LwTRSoON0cgYZ+opiL5aIgEDmm5GRtBx61WUMmOcevNSB8kjzAB6ZoAsqCe360VEsmB94kUUDI2GTxTgnFOVBkmlwex/SgQLuUYrU8KQx3XjbT47mKOVBa3J2uoYf8suxrNAOM1p+FJooPG9g0siRqLW55dgo/5ZetJjRf8Q6IdJ+HviiWezhjma7nuIWCqT5bSqUOR047VsaJoent4O0zRpbSD7VdaSSzGNc52KGOcZ6yVi67qR1D4eeKIZL1Jpm1CeGEPMCQnnqFA56AV1L6rolv4rsYPOX7WLGVY5BMvlpGGTKnnqSFxx/Cako4/wACiSP4Wm/t9Lgv9QN0+I5IQ5bMwDe/AJPtit/TtB0q1+I2qxwWFqscmn28rIIl2hzJICQMYGQozjr1rEW/Gh/DbXY9OvkguINRuEhaORd4U3GAR/wE/rTvAEsdr4t1V7u9d5ZbOFnlup9zu3mSDqT6ADA4HFADtQNraDwhrmqaPa2N/c3n2S6iWEINkisPmB54IRuenPrTfE3h+DR9CvNPgtoXudc1dmXaq7liJ8x8e22Mj/gVcVf3M+raBNqGo3l1e3H2eUxtNKWWLnOUHRfurz14613vi/V4U8SaLJG8VyUsrg4RwdrFohnj2yPzqZNpPl3GrX1IvD0a6f4c8XahPZW0t3ZyyTKs8QYZW2jYA98fjUXizRLKTxP4Pezsre3Oo3Cm6SKMBZVTZINwHBxgjPXBxVjQ501nw94wtfPtre4vpZIYxNKFALW0agnvjPtV3ULqxl8ceFLdL+1kbToLmWbbKvy/u1Rc88ZJOPpTjeyvuDtfQzfira2cvga9ubC2hjfT7sJIyRhT8y7D0/66iujvfC1tN4j0DUYbO38u2WWKdREuCrx/KSMdmH/j1Yev3Ojar4I8Y21hJsdJ5mmEswPmzIqOWQZPynaAB6g8Vvx+JbePxfFprXcHkS6cJ0bzVwHV8EdepDD/AL5piOU0WGDRtF8ba/Ba28moWmoXqQPKm4RojZCqOwyxJAxmp79dAv8A4n+GZtMfT7lrhLr7Wtu6OrFYvkLAcZ+Zhk84HtUOiPFrmheNtCtLm3F/dajetAjyAb0dsBx6rkEZGelNex8N6H8UPDlvosdpbyQpc/bTG3CkxfIGOcA8McdcH3oAl1dpf+Fo6FZXOi21tpyXMq28wjX/AEjMHzZHsT6Vk659nh8Ya6saLGguI1CouAMQR9vrmr/iOzvl+IWlammr2VxBJf8A+iwyXLbYAITuBAyADt6gdSPWsi9Z38Q6207W7yNeliYXLpzHGQAfYcfUGmhMa8sY/u/980zzFH3Sg9flpcR/xKoxRtjPQLVCAzDHGP8AvmigBOwFFMQ4AjpQMnBFFFSMdtPrUU1rDc4W4himUHIEiBgPzoooAYNJsCQfsFp/34X/AAoXSdP27fsFptJ5HkL/AIUUUDHx6XYI6uljaKynKsIVBH0OKdc2VtdMpubaGYrwDJGGx+YoopAKY0WMRhFEeNuwDjHpj0qKGztrUM1vbQQk4BMcYUkfgKKKAIp9PtLp2ea1gkfH3niVj+ZFINIsxCENrbtGDuCGJcZ9cYoooAhOnWbSqPsVrheB+5Xj9KmTTbHaU+w2m0nOPJXGfy96KKGBPJp9pNAkUlrbtFH9xDGML9BjimNp1qYBB9mg8kHIj8tdufXGMZoooArnRLHB22lsM/8ATFf8Klgs4bVNgzFFnhYVA5+lFFMCZI4SrZln+Vdx4HqB/Wo9lvkZefp6DrRRTELH5HO55vYADpRRRQB//9k=)
"""
