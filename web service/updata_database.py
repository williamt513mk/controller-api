#首先，從database.ini文件中讀取數據庫連接參數。
#接下來，通過調用該connect()函數來創建一個新的數據庫連接。
#然後，創建一個新的cursor並執行一條SQL語句來獲取PostgreSQL數據庫版本。
#之後，通過調用fetchone()游標對象的方法來讀取結果集   。
#最後，通過調用和對象的close()方法關閉與數據庫服務器的通信。cursorconnection
#如果發生錯誤，該connect()函數會引發  DatabaseError異常。要查看它的工作原理，我們可以更改database.ini文件中的連接參數。

#使用模塊的connect()功能psycopg2
import psycopg2
#以下config()函數讀取database.ini文件並返回連接參數
from configparser import ConfigParser

#channel_name = input('channel_name=')

#以下config()函數讀取database.ini文件並返回連接參數
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db
 
def connect(channel_name,value=1):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        print('update realtime_web_service table:')
        #PG SQL 語法
        #clear all to 0
        SQL = 'UPDATE realtime_web_service.realtime_web_service SET "IfUse" = \'{0}\''.format(0)
        print(SQL)
        cur.execute(SQL)
        conn.commit()
        #update specific channel
        SQL = 'UPDATE realtime_web_service.realtime_web_service SET "IfUse" = \'{0}\' WHERE "channelID" = \'{1}\''.format(value,channel_name)
        print(SQL)
        cur.execute(SQL)        
        conn.commit()
        #SQL = "SELECT * FROM realtime_web_service.realtime_web_service WHERE channel_name='%s'" % (channel_name)
        #print('perform checking: %s' % SQL)
        cur.execute(SQL)
        #cur.execute("SELECT * FROM realtime_web_service.realtime_web_service WHERE channel_name='TPM K1廢氣風扇(西) 背輥/工輥 驅動側軸承'")
        # display the PostgreSQL database server version
        #result = cur.fetchall()
        #print(result)
        #print([n.name for n in cur.description]) #找出欄位名稱
        # close the communication with the PostgreSQL
        print('perform close & commit:')
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
 
 
if __name__ == '__main__':
    connect()