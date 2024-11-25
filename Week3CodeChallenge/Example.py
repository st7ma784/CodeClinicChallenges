import json
import os
import random
import time
######USED TO CREATE DATA FILES! DO NOT EDIT THIS FUNCTION######
def populate_data_files(dir='.', num_files=3):
    for filenumber in range(1, num_files+1):
        filename = f"{dir}/table{filenumber}.json"            
        ids=[range(1, 100)]
        mask=[range(1, 100)].shuffle()>50
        ids=[i for i,id in enumerate(ids) if mask[i]]
        value1=[random.randint(1, 100) for i in len(ids)]
        value2=[random.randint(1, 100) for i in len(ids)]
        value3=[random.randint(1, 100) for i in len(ids)]
        dict_data={"id":ids, "value1":value1, "value2":value2, "value3":value3}
        with open(filename, 'w') as f:
            json.dump(dict_data, f)
##############################################################


# Function to sum tables on a primary key
def sum_tables_on_key(tables, primary_key):
    combined_data = {}

    for table in tables:
        #make sure we list all the primary keys
        for entry in table[primary_key]:
            if entry not in combined_data[primary_key]:
                combined_data[primary_key].append(entry)
        for column in table:
            #make sure we list all the columns
            if column != primary_key:
                if column not in combined_data:
                    combined_data[column] = []
        
    for table in tables:
        for i,key in enumerate(table[primary_key]):
            for column in combined_data:
                #if column is primary key, skip
                if column == primary_key:
                    continue
                #if column is in table, add value to combined data
                if column in table:
                    value=table[column][i]
                    column_name=column
                    combined_data_index=key
                    #find the row in combined data
                    row_index=combined_data[primary_key].index(combined_data_index)
                    # if the row index exists, add the value to the row        
                    if row_index:
                        combined_data[column_name][row_index] += value
                    #if the row index does not exist, create a new row
                    else:
                        #add an entry to ALL columns
                        for column in combined_data:
                            if column == primary_key:
                                combined_data[column].append(combined_data_index)
                            else:
                                combined_data[column].append(0)
                        row_index=len(combined_data[primary_key])-1
                    #add the value to the column
                    combined_data[column_name][row_index] += value

    return combined_data

# Example usage
json_files = os.listdir('.')
#read tables from json files
tables=[]
for i in range(len(json_files)):
    with open(json_files[i], 'r') as f:
        tables.append(json.load(f))
#sum tables on primary key
#begin timer here
timer_start = time.time()
primary_key = 'id'
result = sum_tables_on_key(json_files, primary_key)
#end timer here
timer_end = time.time()
#calculate time taken
time_taken = timer_end - timer_start
#output time taken
print(time_taken)

        