create table status
(
    status_id   serial
        primary key,
    name        varchar not null
        unique,
    description text
);

alter table status
    owner to doadmin;

