import psycopg2
#from datetime import datetime, timezone
import datetime 

def connect():
    
    print('Connecting to the PostgreSQL database...')
 
    try:       
        con = psycopg2.connect(
                        host="ec2-3-229-252-6.compute-1.amazonaws.com",
                        database="d2oesls1sroim3",
                        user="usorejrzywbkzj",
                        password="e99d35ae8aec135d8be184b24346ffbcd178ef2769c02b798bafce7be9e3e417")
        con.set_client_encoding('UTF8')
        return con
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    
def delete_pattern(pattern):
     delete_sql = """delete from public.stock_signals where signal=%s"""
     try:

        print('deleting...'+pattern) 
        conn=connect()
        cur = conn.cursor()
        cur.execute(delete_sql, (pattern,))
        conn.commit()
        cur.close()
        conn.close()
     except (Exception, psycopg2.DatabaseError) as error:
        print(error)
     finally:
        if conn:
            conn.close()
            print('Database connection closed.')     

def insert_signals(stocks,source,type,period):
    print('Connecting to the PostgreSQL database...')
    #dt = datetime.now(timezone.utc)
    #tday = dt.strftime("%Y-%m-%d")
    
    sql = """INSERT INTO public.stock_signals(date, stock, company, signal, type, link, source,period, id)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, nextval('stock_signals_seq')) RETURNING stock;"""

    #delete_sql = """delete from public.stock_signals where signal=%s and date_trunc('day', date)::date=%s"""
   
    
    formattedDate = datetime.datetime.today().strftime('%d/%m/%Y')
    
    print("Today is : "+ formattedDate) 

    #print(tday)

    
    try:

        conn=connect()
        cur = conn.cursor()   
        stock_ret = None

        print('inserting...')              

        for stock in stocks:
            cur.execute(sql, (formattedDate, stock, stocks[stock]['company'], stocks[stock]['pattern'], type, stocks[stock]['symbol_org'], source,period,))
            stock_ret = cur.fetchone()[0]
    
        conn.commit()
        print(stock_ret)
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()
            print('Database connection closed.')
    return stock_ret
 
def insert_stock_signal(stock,company,pattern,source,type,symbol_org,period):
    print('Connecting to the PostgreSQL database...')
    #dt = datetime.now(timezone.utc)
    #tday = dt.strftime("%Y-%m-%d")
    
    
    sql = """INSERT INTO public.stock_signals(date, stock, company, signal, type, link, source,period, id)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, nextval('stock_signals_seq'));"""

    #delete_sql = """delete from public.stock_signals where signal=%s and date_trunc('day', date)::date=%s"""
    
    formattedDate = datetime.datetime.today().strftime('%d/%m/%Y')
    print("Today is : "+ formattedDate) 

    #print(tday)
    
    try:
        conn=connect()        
        cur = conn.cursor()   
        stock_ret = None

        print('inserting...'+symbol_org)   
           
        print(sql)
        print(stock)
        print(company)
        print(pattern)
        print(type)
        print(symbol_org)
        print(source)
        print(period)

        cur.execute(sql, (formattedDate, stock, company,pattern, type, symbol_org, source,period,))
        #stock_ret = cur.fetchone()[0]
    
        conn.commit()
        print(stock_ret)
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()
            print('Database connection closed...')

 
def main():
    print('main')
    insert_stock_signal('stock','Kütahya','MACDBUY','source','type','symbol_org','period')
        
if __name__ == '__main__':
    main()
