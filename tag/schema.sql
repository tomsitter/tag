drop table if exists entries;
create table images (
  id integer primary key autoincrement,
  title text not null,
  'text' text,
  image blob not null
);