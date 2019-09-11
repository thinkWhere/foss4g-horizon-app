-- Connect to Postgres Database

CREATE DATABASE viewpointdb
  WITH OWNER = twadmin
       ENCODING = 'UTF8'
	   TEMPLATE = template0
       LC_COLLATE = 'en_GB.UTF-8'
       LC_CTYPE = 'en_GB.UTF-8'
       CONNECTION LIMIT = -1;
GRANT CONNECT, TEMPORARY ON DATABASE viewpointdb TO public;
GRANT ALL ON DATABASE viewpointdb TO twadmin;

-- Connect to viewpointdb Database

CREATE EXTENSION postgis;

CREATE ROLE viewpoint_user LOGIN encrypted password 'viewpoint' NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;

create table viewpoint
(
	id serial primary key,
	geometry geometry(Point,27700),
	processed boolean default false,
	image_file character varying(50),
	peaks_file character varying(50)
);

create index viewpoint_sdx on viewpoint using gist (geometry);

GRANT SELECT,INSERT,UPDATE,DELETE ON table viewpoint TO viewpoint_user;
GRANT USAGE on SEQUENCE viewpoint_id_seq to viewpoint_user;

-- Test as viewpoint_user
--insert into viewpoint(geometry, processed) values(ST_GeomFromText('POINT(279093 693777)',27700), false);
