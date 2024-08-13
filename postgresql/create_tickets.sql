create table tickets
(
    ticket_id     serial
        primary key,
    assignee_user integer
        constraint fk_assignee
            references users,
    asset         integer                   not null
        constraint fk_asset
            references assets,
    status        integer                   not null
        constraint fk_status
            references status,
    summary       varchar                   not null,
    description   text,
    solution      text,
    created_date  date default CURRENT_DATE not null,
    priority      priority                  not null
);

alter table tickets
    owner to doadmin;

create table ticket_logs
(
    ticket_id     integer                                            not null
        constraint fk_ticket
            references tickets,
    new_status_id integer                                            not null
        constraint fk_new_status
            references status,
    date          timestamp with time zone default CURRENT_TIMESTAMP not null,
    user_id       integer                                            not null
        constraint fk_user
            references users,
    primary key (ticket_id, new_status_id, date)
);

alter table ticket_logs
    owner to doadmin;

create table comments
(
    ticket_id integer                                            not null
        constraint fk_ticket
            references tickets,
    "user"    integer                                            not null
        constraint fk_user
            references users,
    date      timestamp with time zone default CURRENT_TIMESTAMP not null,
    content   text                                               not null,
    primary key (ticket_id, "user", date)
);

alter table comments
    owner to doadmin;

