CREATE DATABASE IF NOT EXISTS several_rotations;
USE several_rotations;

CREATE TABLE IF NOT EXISTS poems (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  created TIMESTAMP NOT NULL DEFAULT current_timestamp():::TIMESTAMP,
  body STRING NOT NULL,
  CONSTRAINT "primary" PRIMARY KEY (id ASC),
  FAMILY "primary" (id, created, body)
);

CREATE TABLE IF NOT EXISTS state (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  poem_id UUID NULL,
  max_sections INT NULL,
  lines_per_section INT NOT NULL,
  repeat BOOL NULL DEFAULT false,
  max_lines INT NULL,
  remove_words INT NULL,
  remove_words_gradual BOOL NULL DEFAULT false,
  CONSTRAINT fk_poem_id_ref_poems FOREIGN KEY (poem_id) REFERENCES poems (id),
  INDEX state_auto_index_fk_poem_id_ref_poems (poem_id ASC),
  FAMILY "primary" (id, poem_id, repeat, max_lines, rowid, remove_words, remove_words_gradual)
);
