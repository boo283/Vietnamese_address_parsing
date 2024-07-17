 -- \i D:/ki6/DS108/ThucHanh/address_Data/createTable.sql
 
CREATE TABLE administrative_regions (
	id integer NOT NULL,
	name TEXT NOT NULL  ,
	name_en TEXT NOT NULL,
	code_name TEXT NULL,
	code_name_en TEXT NULL,
	CONSTRAINT administrative_regions_pkey PRIMARY KEY (id)
);


-- CREATE administrative_units TABLE
CREATE TABLE administrative_units (
	id integer NOT NULL,
	full_name TEXT NULL  ,
	full_name_en TEXT NULL,
	short_name TEXT NULL  ,
	short_name_en TEXT NULL,
	code_name TEXT NULL  ,
	code_name_en TEXT NULL,
	CONSTRAINT administrative_units_pkey PRIMARY KEY (id)
);


-- CREATE provinces TABLE
CREATE TABLE provinces (
	code TEXT NOT NULL,
	name TEXT NOT NULL  ,
	name_en TEXT NULL,
	full_name TEXT NOT NULL  ,
	full_name_en TEXT NULL,
	code_name TEXT NULL  ,
	administrative_unit_id integer NULL,
	administrative_region_id integer NULL,
	CONSTRAINT provinces_pkey PRIMARY KEY (code)
);


-- provinces foreign keys

ALTER TABLE provinces ADD CONSTRAINT provinces_administrative_region_id_fkey FOREIGN KEY (administrative_region_id) REFERENCES administrative_regions(id);
ALTER TABLE provinces ADD CONSTRAINT provinces_administrative_unit_id_fkey FOREIGN KEY (administrative_unit_id) REFERENCES administrative_units(id);

CREATE INDEX idx_provinces_region ON provinces(administrative_region_id);
CREATE INDEX idx_provinces_unit ON provinces(administrative_unit_id);
CREATE INDEX idx_provinces_full_name ON provinces(full_name);
CREATE INDEX idx_provinces_name ON provinces(name);

-- CREATE districts TABLE
CREATE TABLE districts (
	code TEXT NOT NULL,
	name TEXT NOT NULL  ,
	name_en TEXT NULL,
	full_name TEXT NULL  ,
	full_name_en TEXT NULL,
	code_name TEXT NULL  ,
	province_code TEXT NULL,
	administrative_unit_id integer NULL,
	CONSTRAINT districts_pkey PRIMARY KEY (code)
);


-- districts foreign keys

ALTER TABLE districts ADD CONSTRAINT districts_administrative_unit_id_fkey FOREIGN KEY (administrative_unit_id) REFERENCES administrative_units(id);
ALTER TABLE districts ADD CONSTRAINT districts_province_code_fkey FOREIGN KEY (province_code) REFERENCES provinces(code);

CREATE INDEX idx_districts_province ON districts(province_code);
CREATE INDEX idx_districts_unit ON districts(administrative_unit_id);
CREATE INDEX idx_districts_full_name ON districts(full_name);
CREATE INDEX idx_districts_name ON districts(name);


-- CREATE wards TABLE
CREATE TABLE wards (
	code TEXT NOT NULL,
	name TEXT NOT NULL  ,
	name_en TEXT NULL,
	full_name TEXT NULL  ,
	full_name_en TEXT NULL,
	code_name TEXT NULL  ,
	district_code TEXT NULL,
	administrative_unit_id integer NULL,
	CONSTRAINT wards_pkey PRIMARY KEY (code)
);


-- wards foreign keys

ALTER TABLE wards ADD CONSTRAINT wards_administrative_unit_id_fkey FOREIGN KEY (administrative_unit_id) REFERENCES administrative_units(id);
ALTER TABLE wards ADD CONSTRAINT wards_district_code_fkey FOREIGN KEY (district_code) REFERENCES districts(code);

CREATE INDEX idx_wards_district ON wards(district_code);
CREATE INDEX idx_wards_unit ON wards(administrative_unit_id);
CREATE INDEX idx_wards_name ON wards(name);
CREATE INDEX idx_wards_full_name ON wards(full_name);
