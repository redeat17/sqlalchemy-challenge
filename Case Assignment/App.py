#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
import json
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,inspect, func


# In[ ]:





# # Part 1 - Prepare SQLAlchemy 

# In[3]:


# Python SQL toolkit and Object Relational Mapper
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
inspector = inspect(engine)
#database_path = "../Resources/hawaii.sqlite"


# In[4]:


measurement_df = pd.read_sql('SELECT * FROM measurement', engine)
measurement_df.head()


# In[5]:


station_df = pd.read_sql('SELECT * FROM STATION', engine)
station_df.head()


# # Part 2 - Exploratory Climate Analysis
# #1.Design a query to retrieve the last 12 months of precipitation data and plot the results

# In[9]:


# Calculate the date 1 year ago from the last date point in the database
lastyear_df = pd.read_sql('SELECT * FROM measurement WHERE date between "2016-08-23" and "2017-08-23"' , engine)
lastyear_df


# In[10]:


# Perform a query to retrieve the data and precipitation scores, # Save the query results as a Pandas DataFrame and set the index to the date column

# Sort the dataframe by date
lastyear_prcp = lastyear_df[["date", "prcp"]].set_index('date').sort_values("date", ascending=False)
lastyear_prcp.head()


# In[11]:


# Use Pandas Plotting with Matplotlib to plot the data
# Set plot and plot the chart
plt.figure(figsize=(15, 10))
plt.plot(lastyear_prcp.index, lastyear_prcp['prcp'])

# Add legned 
plt.legend(['precipitation'], loc="upper right",fontsize=15)
# set x location
xloc = ['2016-08-23', '2016-10-01', '2016-11-09', '2016-12-19', '2017-01-28', '2017-03-09', '2017-04-18','2017-05-31','2017-07-10'] 

# Assign xticks
plt.xticks(xloc, rotation='vertical',fontsize=15)
# Set Labels & Title
plt.xlabel('Date', fontsize=15)
plt.ylabel("Inches",fontsize=15)
plt.title(f"Precipitation (inches)in Honolulu, Hawaii",fontsize=20, fontweight = 'bold')
plt.yticks(size=15)

# Asign xlim and ylim
plt.xlim(0,370)
plt.ylim(-0.4,7)


# Save Figure
plt.savefig("Images/Precipitation_Plot.png", bbox_inches = 'tight')
# Show plot
plt.show()


# In[13]:


# Use Pandas to calculate the summary statistics for the precipitation data
# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
active_df = pd.read_sql('SELECT count (*), station FROM measurement GROUP BY station ORDER BY count(*) desc', engine)
active_df


# In[16]:


measurement_df["station"].value_counts()


# In[17]:


max_temp = pd.read_sql('SELECT max(tobs) FROM measurement WHERE station  = "USC00519281"', engine)
max_temp


# In[18]:


min_temp = pd.read_sql('SELECT min(tobs) FROM measurement WHERE station  = "USC00519281"', engine)
min_temp


# In[19]:


avg_temp = pd.read_sql('SELECT avg(tobs) FROM measurement WHERE station  = "USC00519281"', engine)
avg_temp


# In[20]:


# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station?


# In[21]:


# Choose the station with the highest number of temperature observations.
Highesttemp = pd.read_sql('SELECT max(tobs),station FROM measurement', engine)
Highesttemp


# In[22]:


# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
lastyear_tobs = pd.read_sql('SELECT tobs FROM measurement WHERE station  = "USC00519281" and date between "2016-08-23" and "2017-08-23"', engine)
lastyear_tobs.head()


# In[23]:


#plt.figure(figsize=(12, 8))
#plt.hist(lastyear_tobs, color='red', bins=12)
#plt.grid()
lastyear_tobs.hist()
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.title("Temperature in Hawaii")
plt.show()


# ## Part 3 - Data Analysis Assignment

# In[ ]:





# In[24]:


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
  
    # your code here
    return pd.read_sql('SELECT min(tobs),avg(tobs),max(tobs) FROM measurement WHERE date between "2012-02-28" and "2012-03-05"', engine)
    #return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        #filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))


# In[29]:


# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
   
    df= pd.read_sql('SELECT min(tobs),avg(tobs),max(tobs) FROM measurement WHERE date between "2016-08-23" and "2017-08-23"', engine)
    return df
# function usage example
print(df)


# In[30]:


# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)
tmax = df["max(tobs)"]
tmin = df["min(tobs)"]
peak_to_peak = tmax - tmin # This will be our error line
tavg = df["avg(tobs)"] # This will be the height of our graph 

# Plot
fig, ax = plt.subplots(figsize = (5, 10)) # Create figure & axis objects 
ax.bar(x = 1, height = tavg, yerr = peak_to_peak/2, width = 0.4,color = 'r', alpha = 0.5) # Plotting
ax.set_xticks([0]) 
plt.yticks(size=14)
plt.ylabel("Temp F")
plt.title("Trip Avg Temp")
plt.show()


# In[31]:


# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation
rainfall_df = pd.read_sql('select  s.name, m.station, m.prcp, s.elevation, s.latitude, s.longitude from (Select station, ROUND(sum(prcp),2) prcp  from measurement where date between "2016-08-23" and "2017-08-23" group by station) m join station s on m.station=s.station order by m.prcp desc' , engine)
rainfall_df


# In[32]:


# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A DataFrame containing the daily normals, tmin, tavg, and tmax
    
    """
    
    # your code here
    return pd.read_sql('SELECT min(tobs),avg(tobs),max(tobs) FROM measurement WHERE date like "%01-01"', engine)
daily_normals("01-01")


# In[34]:


# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`
# Set the start and end date of the trip
# Use the start and end date to create a range of dates
# Stip off the year and save a list of %m-%d strings
# Loop through the list of %m-%d strings and calculate the normals for each date

start_date = dt.datetime(2018,1,1)
end_date = dt.datetime(2018,1,7) 
date_list = pd.date_range(start_date, end_date).tolist()
date_list
dates=[]
for date in date_list:
    dates.append (dt.datetime.strftime(date, '%m-%d')) 
normals=[]
for date in dates:
    normals.append(daily_normals(date))
print("My Vacation Date: Jan 01 through Jan 07")
for normal in normals:
    print(normal)


# In[35]:


# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index
normal_temp=[]
for normal in normals:
    normal_temp.append(np.ravel(normal))
travel_df = pd.DataFrame(normal_temp, columns=['min(tobs)', 'avg(tobs)', 'max(tobs)'])
travel_df.index=[str(date.strftime('%Y-%m-%d')) for date in date_list]
travel_df


# In[ ]:





# In[37]:


# Plot the daily normals as an area plot with `stacked=False`
ax = travel_df.plot.area(stacked=False, rot=30)
plt.yticks(size=14)
plt.ylabel("Temp (F)")
plt.title("Trip Avg Temp per Day")
plt.show()


# In[ ]:




