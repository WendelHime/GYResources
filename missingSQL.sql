CREATE TABLE TEXTS (
   id SERIAL PRIMARY KEY,
   language VARCHAR(20),
   tag VARCHAR(2000),
   value VARCHAR(100000),
   description VARCHAR(2000)
);

CREATE TABLE USERS (
   id SERIAL PRIMARY KEY,
   id_type SERIAL,
   email VARCHAR(200),
   username VARCHAR(20),
   password VARCHAR(2000),
   salt VARCHAR(32),
   date_insertion VARCHAR(100),
   date_last_update VARCHAR(100)
);

ALTER TABLE analysis ADD CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USERS(id);
