# Vietnamese_address_parsing
Vietnamese address parsing is my personal project which concentrate on parsing location real estate data from Internet.
The input is presented as a string containing user-generated address, which is then parsed into hierachial token as city/province, district, ward.
It could determine the province if it is not provided in the input. 
## Features
-  Address Extraction: Extracts Vietnamese existing address from PostgresSQL/ SQL Server database from filtering raw data purpose.
-  Data Transformation: Parse raw data into tokens which could be province, district, ward.
-  Comprehensive Support: Handles anll existing addresses in Vietnam
## Goals
- Automate the process of parsing Vietnamese addresses from multiple datasource.
- Improve accuracy and efficiency in identifying locations from text data.
## Example
- For list:
  - Raw address: ['123, KTX khu B, Đông Hoà, Dĩ An, BD']
  - -> Parsed: {'tinh': 'bình dương', 'tinh_cat': 'tỉnh', 'qh': 'dĩ an', 'qh_cat': 'thành phố', 'px': None, 'px_cat': None, 'duong': None, 'Address_ch': '123 k khu b đông hoà bd', 't_check': 1, 'h_check': 1}
- For file:
  - Raw file -> Parsed file
  - # Image
  - # Image
