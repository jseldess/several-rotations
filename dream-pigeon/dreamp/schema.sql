CREATE DATABASE dreamp;
USE dreamp;

CREATE TABLE poems (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  created TIMESTAMP NOT NULL DEFAULT current_timestamp():::TIMESTAMP,
  body STRING NOT NULL,
  CONSTRAINT "primary" PRIMARY KEY (id ASC),
  FAMILY "primary" (id, created, body)
);

CREATE TABLE state (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  poem_id UUID NULL,
  repeat BOOL NULL DEFAULT false,
  max_lines INT8 NULL,
  remove_words INT8 NULL,
  remove_words_gradual BOOL NULL DEFAULT false,
  CONSTRAINT fk_poem_id_ref_poems FOREIGN KEY (poem_id) REFERENCES poems (id),
  INDEX state_auto_index_fk_poem_id_ref_poems (poem_id ASC),
  FAMILY "primary" (id, poem_id, repeat, max_lines, rowid, remove_words, remove_words_gradual)
);
