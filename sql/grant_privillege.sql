-- chcp 65001; change code page to UTF-8

-- Create database WITH Vietnamese collation
CREATE DATABASE vietnamese_administrative_units ENCODING 'UTF8'
WITH COLLATE ='Vietnamese_Vietnam.1258' LC_CTYPE = 'Vietnamese_Vietnam.1258'
LC_COLLATE = 'Vietnamese_Vietnam.1258'
TEMPLATE template0;

use [vietnamese_administrative_units]

-- Grant privillege to DataEngineer role
SET client_encoding = 'UTF8';

 GRANT CONNECT ON DATABASE vietnamese_administrative_units TO DataEngineer;
 ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE, TRIGGER ON TABLES TO DataEngineer;
 GRANT CREATE ON DATABASE vietnamese_administrative_units TO DataEngineer;
 GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public TO DataEngineer;