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
  ('Seed poem 10', '2019-09-10 17:00:01'),
  ('Seed poem 11', '2019-09-11 17:00:01'),
  ('Seed poem 12', '2019-09-12 17:00:01'),
  ('Seed poem 13', '2019-09-13 17:00:01'),
  ('Seed poem 14', '2019-09-14 17:00:01'),
  ('Seed poem 15', '2019-09-15 17:00:01'),
  ('Seed poem 16', '2019-09-16 17:00:01'),
  ('Seed poem 17', '2019-09-17 17:00:01'),
  ('Seed poem 18', '2019-09-18 17:00:01'),
  ('Seed poem 19', '2019-09-19 17:00:01'),
  ('Seed poem 20', '2019-09-20 17:00:01'),
  ('Seed poem 21', '2019-09-21 17:00:01'),
  ('Seed poem 22', '2019-09-22 17:00:01'),
  ('Seed poem 23', '2019-09-23 17:00:01'),
  ('Seed poem 24', '2019-09-24 17:00:01')
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
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 11';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 12';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 13';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 14';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 15';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 16';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 17';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 18';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 19';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 20';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 21';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 22';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 23';
INSERT INTO state (poem_id) SELECT id FROM poems WHERE body = 'Seed poem 24';
