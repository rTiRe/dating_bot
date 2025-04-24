-- name columns
-- depends: dating_20250424_01_aFiY0-coordinates

ALTER TABLE dating."profiles"
  DROP COLUMN last_name;

ALTER TABLE dating."profiles"
  RENAME COLUMN first_name TO name;