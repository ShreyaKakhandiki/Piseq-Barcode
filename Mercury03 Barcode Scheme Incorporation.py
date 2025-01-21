#!/usr/bin/env python
# coding: utf-8

# # code to generate the correct format of csv from the original (testing)

# In[8]:


import pandas as pd
import os
import math


# In[33]:


# read in an example csv file for initial testing

coordinates = pd.read_csv("/u/home/s/shreyaka/project-cluo/piseq/_latest1/_coordinates.csv")

print(coordinates)


# In[9]:


# determine number of subgroups, and number of images per subgroup 

# ian, if your mercury code already stores this information, don't worry about this section, you can just start with a dataframe that contains all of the subgroup information 


latest_path = "/u/home/s/shreyaka/project-cluo/piseq/_latest1" 

# Count the number of "Subgroup" directories in latest_path
subgroup_count = sum(
    1 for entry in filter(lambda x: x.startswith("Subgroup"), os.listdir(latest_path))
    if os.path.isdir(os.path.join(latest_path, entry))
)


# Create a DataFrame to store subgroup metadata, with columns for Subgroup, Subgroup_dim, x, and y
subgroup_df = pd.DataFrame({
    "Subgroup": range(1, subgroup_count + 1),
    "Path": [os.path.join(latest_path, f"Subgroup {i}") for i in range(1, subgroup_count + 1)],
    "Subgroup_dim": [None] * subgroup_count,
    "x": [None] * subgroup_count,
    "y": [None] * subgroup_count
}) 

# calculate subgroup dimensions and add to metadata

for idx, row in subgroup_df.iterrows():
    subgroup_path = row["Path"]
    if os.path.isdir(subgroup_path):
        num_files = sum(1 for _ in os.listdir(subgroup_path) if _.endswith('.tif') and os.path.isfile(os.path.join(subgroup_path, _)))
        #num_files = sum(1 for _ in os.listdir(subgroup_path) if os.path.isfile(os.path.join(subgroup_path, _)))
        print("the number of files is " + str(num_files))
        subgroup_df.at[idx, "Subgroup_dim"] = math.sqrt(num_files)
        
print(subgroup_df)


# In[34]:


# add mask name to coordinates dataframe 

current_group = 1

current_image = 1

for index, row in coordinates.iterrows(): 
    
    #if the image dimension exceeds the current group's size, move to the next subgroup
    
    group_size = (subgroup_df.loc[subgroup_df['Subgroup'] == current_group, 'Subgroup_dim'].iloc[0])**2
    
    if current_image > group_size :
        current_group += 1
        current_image = 1
    
    #add the mask name to the row in coordinates 
    
    mask_name = "subgroup " + str(current_group) + "\sample" + str(current_image) + ".png"
   # print(mask_name)
    coordinates.at[index,'mask'] = mask_name
    
    #increment image number
    
    current_image += 1 

print(coordinates)


# In[38]:


# add new rows for fluidics and wait time 

coordinates['type'] = 'laser'

# Create empty list for new rows
new_rows = []

# Iterate over each row in the original DataFrame
for _, row in coordinates.iterrows():
    
    # Append the original row (converted to a dictionary to avoid index issues)
    new_rows.append(row.to_dict())
    
    # Append the 'fluidics' row (only 'type' column is set, others remain empty)
    new_rows.append({'type': 'fluidics'})
    
    # Append the 'wait' row
    new_rows.append({'type': 'wait'})

# Convert list of dictionaries to a new DataFrame
expanded_coordinates = pd.DataFrame(new_rows)

# Fill NaN values with empty strings
expanded_coordinates = expanded_df.fillna('')

# Reset index for clean numbering
expanded_coordinates.reset_index(drop=True, inplace=True)

print(expanded_coordinates)


# In[41]:


# add missing information to fluidics and wait rows

# information for fluidics rows, values can be changed from these defaults
# port number will be updated 

expanded_coordinates.loc[expanded_coordinates['type'] == 'fluidics', ['flowPort','flowRate','volume']] = [1,500,250]


# add information for wait rows

expanded_coordinates.loc[expanded_coordinates['type'] == 'wait', ['waitTime']] = [1000]


# expanded_coordinates contains all the information that lab view needs, you can save it to a new csv file or overwrite the coordinates.csv file

# expanded_coordinates.to_csv('data.csv', index=False)

print(expanded_coordinates)


# 

# In[ ]:





# In[ ]:





# In[ ]:





# # incorporate bit-system scheme generation into csv modification
