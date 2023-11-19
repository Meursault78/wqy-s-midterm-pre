create database if not exists movie_ruc
use movie_ruc

DROP TABLE IF EXISTS `movie_info`;
Create Table movie_info
(
 movie_id varchar(10) Not Null,
 movie_name varchar(20) Not Null,
 release_date datetime,
 country varchar(20),
 type varchar(10),
 year int check( year>=1000 and  year<=2100),
 primary key(movie_id)
);

DROP TABLE IF EXISTS `move_box`;
#此处表的名称为move_box
Create Table move_box
(
 movie_id varchar(10) Not Null,
 box float,
 primary key(movie_id)
);

DROP TABLE IF EXISTS `actor_info`;
Create Table actor_info
(
 actor_id varchar(10) Not Null,
 actor_name varchar(20) Not Null,
 gender varchar(2) Not Null,
 country varchar(20),
 primary key(actor_id)
);

DROP TABLE IF EXISTS `movie_actor_relation`;
Create Table movie_actor_relation
(
 id varchar(10) Not Null,
 movie_id varchar(10) Not Null,
 actor_id varchar(10) Not Null,
 relation_type varchar(20),
 primary key(id),
 foreign Key(movie_id) references movie_info(movie_id),
 foreign Key(actor_id) references actor_info( actor_id)
);
