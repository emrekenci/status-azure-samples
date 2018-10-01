import pyodbc

def gen_create_pb_table(table,columns,filename):
    sql = "CREATE EXTERNAL TABLE  Stage.%s  (" %table
    sql += "%s"%columns
    sql += ") WITH (LOCATION='/"
    sql += "%s',"%filename
    sql += "DATA_SOURCE = AzureStorage, FILE_FORMAT = pipedelimited, REJECT_TYPE = VALUE, REJECT_VALUE = 0 );"
    return sql

def gen_create_dw_table(table):
    sql = "CREATE TABLE Prod.%s " %table
    sql += "WITH "
    sql += "(    DISTRIBUTION = ROUND_ROBIN,   CLUSTERED COLUMNSTORE INDEX) "
    sql += "AS "
    sql += "SELECT * FROM Stage.%s;" %table
    return sql

if __name__ == '__main__':
    print(gen_create_pb_table('AdjustmentTable_Test','adjustment_uuid varchar(10) NULL, approval_type varchar(10) NULL','adjustmentTable.csv'))
    print(gen_create_dw_table('AdjustmentTable'))

server = '<YOUR-SERVER>.database.windows.net'
database = '<YOUR-DATABASE>'
username = '<YOUR-USERNAME>@<YOUR-DATABASE>'
password = '<YOUR-PASSWORD>'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
cnxn.autocommit = True #Commit needed to create SQL Server Tables.

cursor = cnxn.cursor()

#Create External tables in Azure DW via Polybase
cursor.execute(gen_create_pb_table('AdjustmentTable','adjustment_uuid varchar(10) NULL, approval_type varchar(10) NULL','adjustmentTable.csv'))

#Create Azure DW table from Polybase table via CTAS
cursor.execute(gen_create_dw_table('AdjustmentTable'))
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()