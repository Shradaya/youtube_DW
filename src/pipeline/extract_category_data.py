import connectdb
import json
import sql
import query
import psycopg2

def extract_category_data(filepath, country_name, con, cur):
    source_name  = filepath.split("/")[-1]
    values = []
    archive_list = []
        
    archive_sql_query = sql.query(query.extract_raw_category_archive_data_query)
    sql_query = sql.query(query.extract_raw_category_data_query)
    
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
    for i in values:
        a = i[:]
        a[-1] = source_name
        archive_list.append(a)

    for row in values:
        cur.execute(sql_query, row)
    for row in archive_list:
        cur.execute(archive_sql_query, row)
    con.commit()

def extract_category_data_table(con, cur):
    delete_sql = "DELETE FROM category;"
    cur.execute(delete_sql)
    con.commit()

    sql_query = sql.query(query.extract_category_data_from_raw_query)
    cur.execute(sql_query)
    con.commit()


def main():
    con = connectdb.connect(psycopg2)
    cur = con.cursor()
    
    delete_sql = "DELETE FROM raw_category;"
    cur.execute(delete_sql)
    con.commit()
    

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
    con.close()

if __name__ == '__main__':
    main()  