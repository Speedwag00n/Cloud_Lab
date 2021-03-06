CREATE TABLE USERS
(
    ID                 SERIAL               PRIMARY KEY,
    USERNAME           VARCHAR (64)         NOT NULL CHECK (CHAR_LENGTH(USERNAME) > 5),
    PASSWORD           VARCHAR (256)        NOT NULL
);

CREATE TABLE TAG
(
    ID                 SERIAL               PRIMARY KEY,
    NAME               VARCHAR (32)         NOT NULL CHECK (CHAR_LENGTH(NAME) > 1) UNIQUE
);

CREATE TABLE IMAGE
(
    ID                 SERIAL                     PRIMARY KEY,
    NAME               VARCHAR(128)               NOT NULL CHECK (CHAR_LENGTH(NAME) > 5),
    IMAGE_NAME         VARCHAR(128)               NOT NULL,
    OWNER_ID           INTEGER                    REFERENCES USERS (ID) ON UPDATE CASCADE ON DELETE CASCADE NOT NULL,
    WIDTH              BIGINT                     CHECK (WIDTH > 0),
    HEIGHT             BIGINT                     CHECK (HEIGHT > 0),
    CREATION_DATE      TIMESTAMP WITH TIME ZONE   NOT NULL,
    ALTITUDE           DOUBLE PRECISION           ,
    LATITUDE           DOUBLE PRECISION           CHECK (LATITUDE >= -90 AND LATITUDE <= 90),
    LONGITUDE          DOUBLE PRECISION           CHECK (LONGITUDE >= -180 AND LONGITUDE <= 180)
);

CREATE TABLE IMAGE_TAG
(
    IMAGE_ID           INTEGER              REFERENCES IMAGE (ID) ON UPDATE CASCADE ON DELETE CASCADE NOT NULL,
    TAG_ID             INTEGER              REFERENCES TAG (ID) ON UPDATE CASCADE ON DELETE CASCADE NOT NULL
);
