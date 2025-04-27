-- add cities
-- depends: dating_20250426_01_RjNkB-add-interested-in

CREATE TABLE IF NOT EXISTS dating."cities" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL
);

CREATE INDEX cities_points_idx ON dating."cities" (lat, lon);

ALTER TABLE dating."profiles" ADD COLUMN city_name VARCHAR(256);
ALTER TABLE dating."profiles" ADD COLUMN city_id UUID REFERENCES dating."cities";
