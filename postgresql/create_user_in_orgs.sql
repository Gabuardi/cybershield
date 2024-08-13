create table users_in_organization
(
    user_id integer not null
        constraint fk_user
            references users,
    org_id  integer not null
        constraint fk_org
            references organizations,
    primary key (user_id, org_id)
);

alter table users_in_organization
    owner to doadmin;

