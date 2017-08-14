drop table if exists images;
create table images (
  id integer primary key autoincrement,
  title text not null,
  'text' text,
  image blob not null,
  lat real,
  lon real
);