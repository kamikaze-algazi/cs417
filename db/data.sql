INSERT INTO "PICS"(pic_name)
VALUES ('helloworld.jpeg');
INSERT INTO "PICS"(pic_name)
VALUES ('SpongeBob.png');
INSERT INTO "PICS"(pic_name)
VALUES ('Patrick.png');

INSERT INTO "USER"(passwd, first_name, last_name, email, dob, prof_pic)
VALUES ('$pbkdf2-sha256$29000$.t9bK8W4FwIAIASA0JpT6g$5xB8Ek9lojNNHG9iiUGjsIBd9Kmz4ZLSHhTjDSVc2hM', 'Alyx', 'Algazi', 'kamikaze.algazi@gmail.com', '11-25-1996', 2);
INSERT INTO "USER"(passwd, first_name, last_name, email, dob, prof_pic)
VALUES ('$pbkdf2-sha256$29000$59w7BwCglDKmFOI855wTIg$AX2BuwfiA0ruoNhkv.eVr68kf5g7O5mYbW9/9yMHJvg', 'Sunny', 'Jones', 'najon002@mail.goucher.edu', '03-22-1997', 3);
INSERT INTO "USER"(passwd, first_name, last_name, email, dob, prof_pic)
VALUES ('$pbkdf2-sha256$29000$59w7BwCglDKmFOI855wTIg$AX2BuwfiA0ruoNhkv.eVr68kf5g7O5mYbW9/9yMHJvg', 'Destiny', 'Jones', 'decam@morgan.edu', '02-9-1998', 3);
INSERT INTO "USER"(passwd, first_name, last_name, email, dob, prof_pic)
VALUES ('$pbkdf2-sha256$29000$59w7BwCglDKmFOI855wTIg$AX2BuwfiA0ruoNhkv.eVr68kf5g7O5mYbW9/9yMHJvg', 'Mike', 'Young', 'Justice@gmail.com', '03-23-1997', 2);
INSERT INTO "USER"(passwd, first_name, last_name, email, dob, prof_pic)
VALUES ('$pbkdf2-sha256$29000$59w7BwCglDKmFOI855wTIg$AX2BuwfiA0ruoNhkv.eVr68kf5g7O5mYbW9/9yMHJvg', 'Damen', 'Rogersz', 'Damen.Rogers@gmail.com', '04-25-1989', 3);
INSERT INTO "USER"(passwd, first_name, last_name, email, dob, prof_pic)
VALUES ('$pbkdf2-sha256$29000$59w7BwCglDKmFOI855wTIg$AX2BuwfiA0ruoNhkv.eVr68kf5g7O5mYbW9/9yMHJvg', 'trentons', 'hams', 'hams@aol.com', '06-2-2000', 2);





INSERT INTO "EVENT"(ev_name, ev_desc, ev_time, ev_street, ev_city, ev_state, ev_zip)
VALUES ('Christmas Dinner', 'Eat!', '2019-12-25 19:00:00', '2003 Chapel Ct.', 'Frederick', 'Maryland', '21702');

INSERT INTO "EVENT"(ev_name, ev_desc, ev_time, ev_street, ev_city, ev_state, ev_zip)
VALUES ('sadboi club', ':(', '2020-04-20 16:20:00', '8417 Loch Raven Blvd', 'Towson', 'Maryland', '21218');
INSERT INTO "EVENT"(ev_name, ev_desc, ev_time, ev_street, ev_city, ev_state, ev_zip)
VALUES ('42 Party', 'come party with time', '2019-04-20 18:30:00', 'Goucher College X-Lab', 'Towson', 'Maryland', '21218');

INSERT INTO "EVENT"(ev_name, ev_desc, ev_time, ev_street, ev_city, ev_state, ev_zip)
VALUES ('Pride After Party', 'Its a celebration', '2019-06-14 11:00:00', '900 Druid Park Lake Dr', 'Baltimore', 'Maryland', '21217');

INSERT INTO "EVENT"(ev_name, ev_desc, ev_time, ev_street, ev_city, ev_state, ev_zip)
VALUES ('Vania Vegan Eats Opening', 'Opening of new returant', '2019-08-27 13:00:00', '1 york road', 'Towson', 'Maryland', '21218');

INSERT INTO "EVENT"(ev_name, ev_desc, ev_time, ev_street, ev_city, ev_state, ev_zip)
VALUES ('Frank Ocean Release Party', 'What we all have been crying over!', '2023-07-10 20:20:20', '10 Art Museum Dr', 'Baltimore', 'Maryland', '21218');





INSERT INTO "RSVP"(us_id, ev_id)
VALUES ('1', '1');
INSERT INTO "RSVP"(us_id, ev_id)
VALUES ('2', '1');
INSERT INTO "RSVP"(us_id, ev_id)
VALUES ('1', '2');

INSERT INTO "POST"(us_id, pt_fullname, pt_txt)
VALUES ('1', 'Alyx Algazi', 'Hello, World!');
INSERT INTO "POST"(us_id, pt_fullname, pt_txt)
VALUES ('2', 'Sunny Jones', 'ok');

INSERT INTO "FOLLOW"(flwr_id, flwe_id)
VALUES ('1', '2');
INSERT INTO "FOLLOW"(flwr_id, flwe_id)
VALUES ('2', '1');







INSERT INTO "POST"(us_id, pt_fullname, pt_txt, pt_time)
VALUES ('1', 'ya boi', '30 min', 'now'::timestamp - '30 minutes'::interval);

INSERT INTO "POST"(us_id, pt_fullname, pt_txt, pt_time)
VALUES ('1', 'ya boi', 'hour', 'now'::timestamp - '1 hour'::interval);

INSERT INTO "POST"(us_id, pt_fullname, pt_txt, pt_time)
VALUES ('1', 'ya boi', 'six hr', 'now'::timestamp - '6 hours'::interval);

INSERT INTO "POST"(us_id, pt_fullname, pt_txt, pt_time)
VALUES ('1', 'ya boi', 'twelve hr', 'now'::timestamp - '12 hours'::interval);

INSERT INTO "POST"(us_id, pt_fullname, pt_txt, pt_time)
VALUES ('1', 'ya boi', '1 day', 'now'::timestamp - '1 day'::interval);

INSERT INTO "POST"(us_id, pt_fullname, pt_txt, pt_time)
VALUES ('1', 'ya boi', '3 days', 'now'::timestamp - '3 days'::interval);

INSERT INTO "POST"(us_id, pt_fullname, pt_txt, pt_time)
VALUES ('1', 'ya boi', '7 days', 'now'::timestamp - '7 days'::interval);

INSERT INTO "POST"(us_id, pt_fullname, pt_txt, pt_time)
VALUES ('1', 'ya boi', '8 days', 'now'::timestamp - '8 days'::interval);

INSERT INTO "POST"(us_id, pt_fullname, pt_txt, pt_time)
VALUES ('1', 'ya boi', 'month', 'now'::timestamp - '1 month'::interval);

INSERT INTO "POST"(us_id, pt_fullname, pt_txt, pt_time)
VALUES ('1', 'ya boi', 'year', 'now'::timestamp - '1 year'::interval);

INSERT INTO "POST"(us_id, pt_fullname, pt_txt, pt_time)
VALUES ('1', 'ya boi', 'The FitnessGram Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly but gets faster each minute after you hear this signal bodeboop. A sing lap should be completed every time you hear this sound. ding Remember to run in a straight line and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark. Get ready!… Start.', 'now'::timestamp - '2 years'::interval);
