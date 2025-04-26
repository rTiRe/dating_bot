-- rating field
-- depends: dating_20250424_02_A57eP-name-columns

ALTER TABLE dating."profiles"
ADD COLUMN rating INTEGER
  GENERATED ALWAYS AS (
    (CASE WHEN biography IS NOT NULL AND biography <> '' THEN 20 ELSE 0 END)
    + cardinality(image_names) * 10
  ) STORED;
