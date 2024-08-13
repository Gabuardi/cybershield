create table organizations
(
    org_id   serial
        primary key,
    org_name varchar not null
        unique
);

alter table organizations
    owner to doadmin;

