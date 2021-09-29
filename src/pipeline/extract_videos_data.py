import connectdb
import csv
import sql
import query
import psycopg2

def extract_videos_data(filepath, country_name, con, cur):
    source_name  = filepath.split("/")[-1]
    values = []
    archive_list = []
    
    archive_sql_query = sql.query(query.extract_raw_videos_archive_data_query)
    sql_query = sql.query(query.extract_raw_videos_data_query)
    
    csv_file = open(filepath,'rt', encoding='ISO-8859-1')
    csv_reader = csv.reader(csv_file)
    i = 0
    for row in csv_reader:
        if i==0:
            i+=1
            continue
        row.append(country_name)
        values.append(row)
    csv_file.close()
        
    for i in values:
        a = i[:]
        a[-1] = (source_name)
        archive_list.append(a)

    for row in values:
        cur.execute(sql_query, row)
    print("Standard Raw Table Populated for" + ' ' + country_name)
    for row in archive_list:
        cur.execute(archive_sql_query, row)
    print("Archive Raw Table Populated" + ' ' + country_name)
    
    con.commit()

def extract_video_data_table(con, cur):
    delete_sql = "DELETE FROM videos;"
    cur.execute(delete_sql)
    con.commit()

    sql_query = sql.query(query.extract_video_data_from_raw_query)
    cur.execute(sql_query)
    con.commit()



def main():
    con = connectdb.connect(psycopg2)
    cur = con.cursor()

    delete_sql = "DELETE FROM raw_videos;"
    cur.execute(delete_sql)
    con.commit()
    
    extract_videos_data('../../data/CAvideos.csv', 'Canada', con, cur)
    extract_videos_data('../../data/DEvideos.csv', 'Denmark', con, cur)
    extract_videos_data('../../data/FRvideos.csv', 'France', con, cur)
    extract_videos_data('../../data/GBvideos.csv', 'Great Britian', con, cur)
    extract_videos_data('../../data/INvideos.csv', 'India', con, cur)
    extract_videos_data('../../data/JPvideos.csv', 'Japan', con, cur)
    extract_videos_data('../../data/KRvideos.csv', 'Korea', con, cur)
    extract_videos_data('../../data/MXvideos.csv', 'Mexico', con, cur)
    extract_videos_data('../../data/RUvideos.csv', 'Russia', con, cur)
    extract_videos_data('../../data/USvideos.csv', 'United States', con, cur)

    extract_video_data_table(con, cur)
    con.close()


if __name__ == '__main__':
    main()  