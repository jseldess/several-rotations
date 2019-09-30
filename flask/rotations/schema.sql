CREATE DATABASE IF NOT EXISTS several_rotations;
USE several_rotations;

CREATE TABLE IF NOT EXISTS poems (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  created TIMESTAMP NOT NULL DEFAULT current_timestamp():::TIMESTAMP,
  body STRING NOT NULL,
  CONSTRAINT "primary" PRIMARY KEY (id ASC),
  INDEX poems_created_idx (created ASC),
  FAMILY "primary" (id, created, body)
);

CREATE TABLE IF NOT EXISTS state (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  poem_id UUID NULL,
  max_sections INT NULL,
  lines_per_section INT NOT NULL DEFAULT 0,
  repeat BOOL NULL DEFAULT false,
  max_lines INT NULL,
  remove_words INT NULL,
  CONSTRAINT fk_poem_id_ref_poems FOREIGN KEY (poem_id) REFERENCES poems (id),
  INDEX state_auto_index_fk_poem_id_ref_poems (poem_id ASC),
  FAMILY "primary" (id, poem_id, repeat, max_lines, rowid, remove_words)
);

INSERT INTO poems (body, created) VALUES
  ('Seed poem 1', '2019-09-01 17:00:01'),
  ('Seed poem 2', '2019-09-02 17:00:01'),
  ('Seed poem 3', '2019-09-03 17:00:01'),
  ('Seed poem 4', '2019-09-04 17:00:01'),
  ('Seed poem 5', '2019-09-05 17:00:01'),
  ('Seed poem 6', '2019-09-06 17:00:01'),
  ('Seed poem 7', '2019-09-07 17:00:01'),
  ('Seed poem 8', '2019-09-08 17:00:01'),
  ('Seed poem 9', '2019-09-09 17:00:01'),
  ('Seed poem 10', '2019-09-10 17:00:01')
;

INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 1';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 2';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 3';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 4';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 5';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 6';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 7';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 8';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 9';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 10';
