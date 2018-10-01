--Create Master key to encrypt connection to Azure Blob. 
IF NOT EXISTS (SELECT * FROM sys.symmetric_keys WHERE symmetric_key_id = 101)
BEGIN
    PRINT 'Creating Master Key'
    CREATE MASTER KEY;
END
ELSE
BEGIN
    PRINT 'Master Key already exists'
END

--Then execute the following code where IDENTITY contains a random string and SECRET contains the copied key from your Azure Storage account.
CREATE DATABASE SCOPED CREDENTIAL myid_credential WITH IDENTITY = '<YOUR-ID>', SECRET = '<YOUR-SECRET>';

--Next you define the external Azure Blob Storage data source with the previously created credential:
CREATE EXTERNAL DATA SOURCE AzureStorage
WITH (
    TYPE = HADOOP,
    LOCATION = 'wasbs://<YOUR-CONTAINER-NAME@<YOUR-STORAGE-ACCOUNT-NAME>.blob.core.windows.net',
    CREDENTIAL = myid_credential
);
GO

--Creating a Stage and Prod schema to separate staging (Polybase) tables from Production tables.
CREATE SCHEMA Stage AUTHORIZATION dbo;
GO
CREATE SCHEMA Prod AUTHORIZATION dbo;
GO
---------------------------------------------------------------------------------------------

--And for the source data, define the file format and external table definition:
CREATE EXTERNAL FILE FORMAT pipedelimited
WITH (FORMAT_TYPE = DELIMITEDTEXT,
      FORMAT_OPTIONS(
          FIELD_TERMINATOR = ',',
          FIRST_ROW  = 2,
          STRING_DELIMITER = '',
          DATE_FORMAT ='',
          USE_TYPE_DEFAULT = False)
);

--Create external table from Blob CSV file using Polybase
CREATE EXTERNAL TABLE Stage.AdjustmentTable (
    adjustment_uuid varchar(10) NULL,
    approval_type varchar(10) NULL
)
WITH (LOCATION='/<SOURCE-FILE-NAME>',
      DATA_SOURCE = AzureStorage,
      FILE_FORMAT = pipedelimited, --check if this can be done in line.
      REJECT_TYPE = VALUE,
      REJECT_VALUE = 0
);

--Use CTAS (Create Table As Select) to load the data from Azure Blob Storage to SQL Data Warehouse
CREATE TABLE Prod.AdjustmentTable
WITH
(
    DISTRIBUTION = ROUND_ROBIN
,   CLUSTERED COLUMNSTORE INDEX
)
AS
SELECT * 
from Stage.AdjustmentTable;