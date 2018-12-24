DROP TABLE IF EXISTS poems;

CREATE TABLE poems (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  created TIMESTAMP NOT NULL DEFAULT current_timestamp():::TIMESTAMP,
  body STRING NOT NULL,
  CONSTRAINT "primary" PRIMARY KEY (id ASC),
  FAMILY "primary" (id, created, body)
);
