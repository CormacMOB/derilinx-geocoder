CREATE EXTENSION postgis;
CREATE EXTENSION fuzzystrmatch;

CREATE TEMP TABLE tmp_townlands
(
OBJECTID INTEGER PRIMARY KEY,
County TEXT,
Contae TEXT,
Local_Government_Area TEXT,
Limistéar_Rialtas_Áitiúil TEXT,
Classification VARCHAR(10),
Cineál VARCHAR(10),
Gaeltacht VARCHAR(10),
Town_Classification VARCHAR(10),
ID INTEGER,
English_Name TEXT,
Irish_Name TEXT,
Foirm_Ghinideach TEXT,
Alternative_Name TEXT,
IG_E INTEGER,
IG_N INTEGER,
ITM_E INTEGER,
ITM_N INTEGER, 
Irish_Validation INTEGER,
Legislation INTEGER,
Validated_By TEXT,
Date_ TEXT,
Comment_ TEXT
);


CREATE TEMP TABLE tmp_counties
(
OBJECTID INTEGER PRIMARY KEY,
County TEXT,
Contae TEXT,
Local_Government_Area TEXT,
Limistéar_Rialtas_Áitiúil TEXT,
Classification VARCHAR(10),
Cineál VARCHAR(10),
Gaeltacht VARCHAR(10),
Town_Classification VARCHAR(10),
ID INTEGER,
English_Name TEXT,
Irish_Name TEXT,
Foirm_Ghinideach TEXT,
Alternative_Name TEXT,
IG_E INTEGER,
IG_N INTEGER,
ITM_E INTEGER,
ITM_N INTEGER, 
Irish_Validation INTEGER,
Legislation INTEGER,
Validated_By TEXT,
Date_ TEXT,
Comment_ TEXT
);

COPY tmp_counties FROM '/tmp/Counties_-_OSi_National_Placenames_Gazetteer.csv' CSV HEADER;
COPY tmp_townlands FROM '/tmp/Townlands_-_OSi_National_Placenames_Gazetteer.csv' CSV HEADER;

CREATE TABLE counties AS
(   
    SELECT
        OBJECTID,
        ID, 
        County,
        Local_Government_Area,
        English_Name,
        Alternative_Name,
        ST_Transform(ST_SetSRID(ST_MakePoint(ITM_E, ITM_N), 2157), 4326) as centroid
    FROM tmp_counties
);

CREATE TABLE townlands AS
(   
    SELECT
        OBJECTID,
        ID, 
        County,
        Local_Government_Area,
        English_Name,
        Irish_Name,
        Alternative_Name,
        ST_Transform(ST_SetSRID(ST_MakePoint(ITM_E, ITM_N), 2157), 4326) as centroid
    FROM tmp_townlands
);

CREATE INDEX "county_english_name_idx" on public."counties"("english_name");
CREATE INDEX "townland_english_name_idx" on public."townlands"("english_name");
