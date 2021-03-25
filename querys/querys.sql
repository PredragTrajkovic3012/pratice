--Install postgresql koristeci uputstva iz 
--https://docs.google.com/document/d/1F-epM5KskFVMwHMuCka9Km6AY3U6QsJPq3QIXtb8Jbg/edit

--psql -U postgres template1
-- create role predrag with login createdb password '123
--psql -U predrag template1
--create database projekat;
--konektovanje sa bazom \c projekat

--CREAT DATABASE with CREATE:
create table person (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	email VARCHAR(150),
	gender VARCHAR(15) NOT NULL,
	date_of_birth DATE NOT NULL,
	country_of_birth VARCHAR(50) NOT NULL
);

--Insertovanje podataaka 
insert into person (first_name, last_name, email, gender, date_of_birth, country_of_birth) values ('Jaclin', 'Syne', 'jsyne0@dmoz.org', 'Non-binary', '2020/11/04', 'Russia');
insert into person (first_name, last_name, email, gender, date_of_birth, country_of_birth) values ('Ogden', 'Ridulfo', 'oridulfo1@google.com.br', 'Male', '2020/09/05', 'Republic of the Congo');
insert into person (first_name, last_name, email, gender, date_of_birth, country_of_birth) values ('Letty', 'Dymoke', 'ldymoke2@parallels.com', 'Genderfluid', '2021/01/25', 'Colombia');
insert into person (first_name, last_name, email, gender, date_of_birth, country_of_birth) values ('Roscoe', 'Pyle', null, 'Agender', '2021/02/09', 'Poland');
insert into person (first_name, last_name, email, gender, date_of_birth, country_of_birth) values ('Eric', 'Goman', 'egoman4@4shared.com', 'Agender', '2020/06/06', 'China');

--moguce je generisati podatke na mackaroo sacuvati fajl i pokrenuti komandu sa \i imeputanje do fajla
--OPASANA KOMANDA DROP DATABASE ime baze

select * from person;
select first_name from person;
select * from person ORDER BY date_of_birth DESC;
--selektovanje order by DESK opadajuce asc normalno

--
select * from person where country_of_birth='China';

-- OR AND < > <= >= = aritmeticke operacije

select * from person LIMIT 10;

--select * from person OFFSET 5 LIMIT 5; od petog narednih 5

--select * from person OFFSET 5 FETCH first 5 ROW ONLY; isto samo sto je FETCH prihvatljiviji kao sql standard
-- sve koji su rodjeni u kini congo ili rusiji
select * from person where country_of_birth IN('China','Congo','Russia')


--Ssve izmedju datuma
select * from person where date_of_birth BETWEEN DATE '2019-01-05' AND '2015-01-01';

-- % bilo sta pre toga .com
select * from person where email LIKE '%.com'

-- _ _ _ _ cetri slova ili pet 
select * from person where email LIKE '______%.com'

--redja sve zemlje i koliko ljudi ima 
select country_of_birth,COUNT(*) FROM person GROUP BY country_of_birth;
-- isto samo gde je > 5 ljudi
select country_of_birth,COUNT(*) FROM person GROUP BY country_of_birth HAVING COUNT(*) > 5 ORDER BY country_of_birth



