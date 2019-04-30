CREATE TABLE "PICS" (
    pic_id		SERIAL,
    pic_data	OID NOT NULL,
    pic_name	VARCHAR(255) NOT NULL,
    pic_type	VARCHAR(5) NOT NULL,
    PRIMARY KEY (pic_id)
);

CREATE TABLE "USER" (
    us_id		SERIAL,
    us_state	VARCHAR(15),
    us_city		VARCHAR(25),
    passwd		VARCHAR(87) NOT NULL,
    first_name	VARCHAR(25) NOT NULL,
    last_name	VARCHAR(25) NOT NULL,
    email		VARCHAR(50) UNIQUE NOT NULL,
    dob			DATE NOT NULL,
    age			NUMERIC(3,0) check (age >- 18),
    prof_pic	INTEGER,
    PRIMARY KEY (us_id),
    FOREIGN KEY (prof_pic) REFERENCES "PICS"(pic_id)
        ON DELETE CASCADE
);

CREATE TABLE "EVENT" (
    ev_id		SERIAL,
    ev_name		VARCHAR(100) NOT NULL,
    ev_desc		VARCHAR(1000) NOT NULL,
    ev_time		TIMESTAMP NOT NULL,
    ev_street	VARCHAR(50) NOT NULL,
    ev_city		VARCHAR(25) NOT NULL,
    ev_state	VARCHAR(15) NOT NULL,
    ev_zip		VARCHAR(5) NOT NULL,
    ev_pic		INTEGER,
    PRIMARY KEY (ev_id),
    FOREIGN KEY (ev_pic) REFERENCES "PICS"(pic_id)
        ON DELETE CASCADE
);

CREATE TABLE "RSVP" (
    us_id		INTEGER,
    ev_id		INTEGER,
    PRIMARY KEY (us_id, ev_id),
    FOREIGN KEY (us_id) REFERENCES "USER"
        ON DELETE CASCADE,
    FOREIGN KEY (ev_id) REFERENCES "EVENT"
        ON DELETE CASCADE
);

CREATE TABLE "POST" (
    us_id		INTEGER,
    pt_fullname VARCHAR(50) NOT NULL,
    pt_time		TIMESTAMP DEFAULT now(),
    pt_txt		VARCHAR(1000) NOT NULL,
    pt_pic		INTEGER,
    PRIMARY KEY (us_id, pt_time),
    FOREIGN KEY (us_id) REFERENCES "USER"(us_id)
        ON DELETE CASCADE,
    FOREIGN KEY (pt_pic) REFERENCES "PICS"(pic_id)
        ON DELETE CASCADE
);

CREATE TABLE "FOLLOW" (
    flwr_id		INTEGER,
    flwe_id		INTEGER,
    PRIMARY KEY (flwr_id, flwe_id),
    FOREIGN KEY (flwr_id) REFERENCES "USER"(us_id)
        ON DELETE CASCADE,
    FOREIGN KEY (flwe_id) REFERENCES "USER"(us_id)
        ON DELETE CASCADE	
);
