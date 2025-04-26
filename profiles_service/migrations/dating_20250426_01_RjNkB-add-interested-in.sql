-- add interested_in
-- depends: dating_20250424_03_j8sYy-rating-field

ALTER TABLE dating."profiles" ADD COLUMN interested_in CHAR(1) NOT NULL;
