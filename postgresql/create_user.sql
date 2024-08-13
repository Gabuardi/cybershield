create table users
(
    user_id   serial
        primary key,
    name      varchar not null,
    last_name varchar,
    email     varchar not null
        unique,
    password  varchar not null
);

alter table users
    owner to doadmin;

