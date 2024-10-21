create schema blub;
alter schema blub owner to postgres;

create table if not exists blub."user"
(
    user_id    serial
    constraint user_pk
    primary key,
    discord_id bigint not null
);

alter table blub."user"
    owner to postgres;

create table if not exists blub.activity
(
    activity_id   serial
    constraint activity_pk
    primary key,
    activity_name varchar not null
);

alter table blub.activity
    owner to postgres;

create table if not exists blub.highscore
(
    highscore_id serial
    constraint highscore_pk
    primary key,
    user_id      integer not null
    constraint user___fk
    references blub."user",
    activity_id  integer not null
    constraint activity___fk
    references blub.activity,
    score        integer not null
);

alter table blub.highscore
    owner to postgres;

/* Manual data entries */
insert into blub."activity" (activity_name)
values ('pingpong')
on conflict (activity_name) do nothing;
