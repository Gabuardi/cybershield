create table assets
(
    asset_id  serial
        primary key,
    owner_org integer not null
        constraint fk_organization
            references organizations,
    ip        inet    not null
        unique,
    dns       varchar
        unique,
    os        varchar
);

alter table assets
    owner to doadmin;

