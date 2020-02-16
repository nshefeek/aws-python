#! /home/nshefeek/anaconda3/bin/python
# serverless database query - mysql example


import pymysql
import logging
import traceback
from os import environ

#port=environ.get('PORT')
#dbuser=environ.get('DBUSER')
#password=environ.get('DBPASSWORD')
#database=environ.get('DATABASE')

port=3306
dbuser='admin'
password='admin-rds'
database='sql_hr'
endpoint='database-1.cswjhuhatrp4.us-east-2.rds.amazonaws.com'


query="SELECT * FROM employees LIMIT 2"

logger=logging.getLogger()
logger.setLevel(logging.INFO)

def make_connection():
    return pymysql.connect(host=endpoint, user=dbuser, passwd=password,
        port=port, db=database, autocommit=True)

def log_err(errmsg):
    logger.error(errmsg)
    return {"body": errmsg , "headers": {}, "statusCode": 400,
        "isBase64Encoded":"false"}

logger.info("Cold start complete.")

def handler(event,context):

    try:
        cnx = make_connection()
        cursor=cnx.cursor()

        try:
            cursor.execute(query)
        except:
            return log_err ("ERROR: Cannot execute cursor.\n{}".format(
                traceback.format_exc()) )

        try:
            results_list=[]
            for result in cursor: results_list.append(result)
            print(results_list)
            cursor.close()

        except:
            return log_err ("ERROR: Cannot retrieve query data.\n{}".format(
                traceback.format_exc()))


        return {"body": str(results_list), "headers": {}, "statusCode": 200,
        "isBase64Encoded":"false"}


    except:
        return log_err("ERROR: Cannot connect to database from handler.\n{}".format(
            traceback.format_exc()))


    finally:
        try:
            cnx.close()
        except:
            pass

if __name__== "__main__":
    handler(None,None)
