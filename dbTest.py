import psycopg2

def connect():
    
    print('Connecting to the PostgreSQL database...')
 
    try:
        
        conn = psycopg2.connect(
                        host="ec2-3-229-252-6.compute-1.amazonaws.com",
                        database="d2oesls1sroim3",
                        user="usorejrzywbkzj",
                        password="e99d35ae8aec135d8be184b24346ffbcd178ef2769c02b798bafce7be9e3e417")
    
    
    # create a cursor
        cur = conn.cursor()
        
    	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
    
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
        	# close the communication with the PostgreSQL
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
        
if __name__ == '__main__':
    connect()