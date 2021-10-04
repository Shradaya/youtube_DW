import connectdb
import csv
import sql
import query
import psycopg2
from googletrans import Translator


def extract_videos_data(filepath, country_name, con, cur, translator):
    source_name  = filepath.split("/")[-1]
    values = []
    archive_list = []
    
    archive_sql_query = sql.query(query.extract_raw_videos_archive_data_query)
    sql_query = sql.query(query.extract_raw_videos_data_query)
    
    csv_file = open(filepath,'rt', encoding='ISO-8859-1')
    csv_reader = csv.reader((l.replace('\0', '') for l in csv_file))
    i = 0
    for row in csv_reader:
        try:
            if i==0:
                i+=1
                continue
            if len(row) == 16:
                temp = prepare_row(country_name, row, translator)
                values.append(temp)
        except:
            pass
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
    
    #con.commit()

def prepare_row(country_name, row, translator):
    temp = []
    if country_name == 'Japan'  or country_name == 'Korea' or country_name == 'Russia':
        for data in row:
            translated = translator.translate(data)
            temp.append(translated.text)
        temp.append(country_name)
        print(temp)
    else:
        temp = row[:]
        temp.append(country_name)
    
    return temp


def extract_video_data_table(con, cur):
    delete_sql = "DELETE FROM videos;"
    cur.execute(delete_sql)
    #con.commit()

    sql_query = sql.query(query.extract_video_data_from_raw_query)
    cur.execute(sql_query)
    #con.commit()
    print("Video table has been extracted")

def load_dim_channel_data_table(con, cur):
    delete_sql = "DELETE FROM dim_channel;"
    cur.execute(delete_sql)
    #con.commit()

    sql_query = sql.query(query.load_dim_channel_query)
    cur.execute(sql_query)
    #con.commit()
    print("Dimension channel loading has been completed.")

def load_dim_country_data_table(con, cur):
    delete_sql = "DELETE FROM dim_country;"
    cur.execute(delete_sql)
    #con.commit()

    sql_query = sql.query(query.load_dim_country_query)
    cur.execute(sql_query)
    #con.commit()
    print("Dimenstion country loading has been completed.")

def load_dim_publish_date_data_table(con, cur):
    delete_sql = "DELETE FROM dim_publish_date;"
    cur.execute(delete_sql)
    #con.commit()

    sql_query = sql.query(query.load_dim_publish_date_query)
    cur.execute(sql_query)
    #con.commit()
    print("Dimenstion publish date loading has been completed.")

def load_dim_trending_date_data_table(con, cur):
    delete_sql = "DELETE FROM dim_trending_date;"
    cur.execute(delete_sql)
    #con.commit()

    sql_query = sql.query(query.load_dim_trending_date_query)
    cur.execute(sql_query)
    #con.commit()
    print("Dimenstion trending date loading has been completed.")

def load_dim_videos_data_table(con, cur):
    delete_sql = "DELETE FROM dim_videos"
    cur.execute(delete_sql)
    #con.commit()

    sql_query = sql.query(query.load_dim_videos_query)
    cur.execute(sql_query)
    #con.commit()
    print("Dimenstion videos loading has been completed.")

def load_fact_video_trend_data_table(con, cur):
    delete_sql = "DELETE FROM fact_video_trend;"
    cur.execute(delete_sql)
    #con.commit()

    sql_query = sql.query(query.load_fact_video_trend_query)
    cur.execute(sql_query)
    #con.commit()
    print("Fact table video trend has been completed.")

def main():
    con = connectdb.connect(psycopg2)
    cur = con.cursor()
    translator = Translator()
    
    delete_sql = "DELETE FROM raw_videos;"
    cur.execute(delete_sql)
    #con.commit()
    
    """extract_videos_data('../../data/CAvideos.csv', 'Canada', con, cur, translator)
    extract_videos_data('../../data/DEvideos.csv', 'Germany', con, cur, translator)
    extract_videos_data('../../data/FRvideos.csv', 'France', con, cur, translator)
    extract_videos_data('../../data/GBvideos.csv', 'Great Britian', con, cur, translator)
    extract_videos_data('../../data/INvideos.csv', 'India', con, cur, translator)"""
    #extract_videos_data('../../data/JPvideos.csv', 'Japan', con, cur, translator)
    #extract_videos_data('../../data/KRvideos.csv', 'Korea', con, cur, translator)
    #extract_videos_data('../../data/MXvideos.csv', 'Mexico', con, cur, translator)
    #extract_videos_data('../../data/RUvideos.csv', 'Russia', con, cur, translator)
    #extract_videos_data('../../data/USvideos.csv', 'United States', con, cur, translator)
    extract_videos_data('../../data/korea.csv', 'Korea', con, cur, translator)
    
    #extract_video_data_table(con, cur)
    
    """load_dim_channel_data_table(con, cur)
    load_dim_country_data_table(con, cur)
    load_dim_publish_date_data_table(con, cur)
    load_dim_trending_date_data_table(con, cur)
    load_dim_videos_data_table(con, cur)
    load_fact_video_trend_data_table(con, cur)"""
    con.close()


if __name__ == '__main__':
    main()  