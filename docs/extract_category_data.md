## Script to extract category data into the data base
The script for this task can be found [here.](https://github.com/Shradaya)


## 1. Imported necessary libraries:
```
import connectdb
import json
import sql
import query
import psycopg2
```
Here `sql`, `query`, `connectdb` is the module made in pipeline directory which I have explained in 
documentation.md file. 


## 2. `main` function

The main function is what executes the program in sequence. It has connection and cursor definition. It calls functions in required sequence to get the correct outcome.

* Function definition
```
def main():
    ....
```

* Connection and cursor definition
```
    con = connectdb.connect(psycopg2)
    cur = con.cursor()
```

* Deleting the data available in the raw_category table before inserting new data into it.
```
    delete_sql = "DELETE FROM raw_category;"
    cur.execute(delete_sql)
    con.commit()
```


* calling function in a sequence. The functions called in main are defined below. After function call is completed the connection is closed. Here the extract_category_data has been called multiple times in order to read different files one after the other.
```    
    extract_category_data('../../data/CA_category_id.json', 'Canada', con, cur)
    extract_category_data('../../data/DE_category_id.json', 'Denmark', con, cur)
    extract_category_data('../../data/FR_category_id.json', 'France', con, cur)
    extract_category_data('../../data/GB_category_id.json', 'Great Britian', con, cur)
    extract_category_data('../../data/IN_category_id.json', 'India', con, cur)
    extract_category_data('../../data/JP_category_id.json', 'Japan',con, cur)
    extract_category_data('../../data/KR_category_id.json', 'Korea', con, cur)
    extract_category_data('../../data/MX_category_id.json', 'Mexico',con, cur)
    extract_category_data('../../data/RU_category_id.json', 'Russia', con, cur)
    extract_category_data('../../data/US_category_id.json', 'United States', con, cur)
    
    extract_category_data_table(con, cur)

    load_dim_category_data_table(con, cur)
    con.close()
```    

## 3. `extract_category_data` function

The extract_category_data function is reads the data from json file and stores it in raw tables. The function has four arguments. The arguments are filepath, country_name, connection and cursor.

* Function definition
```
extract_category_data(filepath, country_name, con, cur):
    ....
```

* Getting the source file name and creating lists to covey the data up to the database.
```
    source_name  = filepath.split("/")[-1]
    values = []
    archive_list = []

```
    
* Loading the predefined queries
```
    archive_sql_query = sql.query(query.extract_raw_category_archive_data_query)
    sql_query = sql.query(query.extract_raw_category_data_query)
```   

* Reading each parameter and storing the values in the standard raw table conveyer list.
```
    with open(filepath) as json_data:
        data = json.load(json_data)
        for i in range(len(data['items'])):
            values.append([data['items'][i]['kind'],
                        data['items'][i]['etag'],
                        data['items'][i]['id'],
                        data['items'][i]['snippet']['channelId'],
                        data['items'][i]['snippet']['title'],
                        data['items'][i]['snippet']['assignable'],
                        country_name])
```

* loading the archive data conveyer list by adding the source file name.
```
    for i in values:
        a = i[:]
        a[-1] = source_name
        archive_list.append(a)
```

* Executing the sql queries with their respective data and  commiting the changes.
```
    for row in values:
        cur.execute(sql_query, row)
    for row in archive_list:
        cur.execute(archive_sql_query, row)
    con.commit()
```

## 4. `extract_category_data_table` function

This function is used to insert data into the category table by cleaning the data from the raw_category table.

* Function Definition
```
def extract_category_data_table(con, cur):
    ....
```

* Deleting file that exists before insertion
```    
    delete_sql = "DELETE FROM category;"
    cur.execute(delete_sql)
    con.commit()
```

* Loading the sql query to insert data into the category table 
```
    sql_query = sql.query(query.extract_category_data_from_raw_query)
```

* Executing query and commiting the changes
```
    cur.execute(sql_query)
    con.commit()
```

## 5. `load_dim_category_data_table` function

This function is used to insert data into the dim_category from the standard category table.

* Function Definition
```
def load_dim_category_data_table(con, cur):
    ....
```

* Deleting file that exists before insertion
```    
    delete_sql = "DELETE FROM dim_category;"
    cur.execute(delete_sql)
    con.commit()
```

* Loading the sql query to insert data into the dim_category table 
```
    sql_query = sql.query(query.load_dim_category_query)
```

* Executing query and commiting the changes
```
    cur.execute(sql_query)
    con.commit()
```


## 6. Program executor

When the program is executed this statement directs the execution to the main function.

```
if __name__ == '__main__':
    main()
```