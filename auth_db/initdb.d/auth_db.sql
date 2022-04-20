create table roles
(
    title varchar(50) not null
        constraint roles_pkey
            primary key
);

create index roles_title_c2f44585_like on roles (title varchar_pattern_ops);


create table users
(
    password     varchar(128) not null,
    last_login   timestamp with time zone,
    id           uuid         not null
        constraint users_pkey
            primary key,
    login        varchar(100) not null
        constraint users_login_key
            unique,
    email        varchar(254) not null
        constraint users_email_key
            unique,
    first_name   varchar(100),
    middle_name  varchar(100),
    last_name    varchar(100),
    is_superuser boolean      not null
);

create index users_login_3b007138_like on users (login varchar_pattern_ops);

create table users_roles
(
    role_id varchar(50) not null,
    user_id uuid        not null
);

create table login_history
(
    id            uuid                     not null
        constraint login_history_pkey primary key,
    user_agent    varchar(150)             not null,
    refresh_token text                     not null,
    created_at    timestamp with time zone not null,
    user_id       uuid                     not null
        constraint login_history_user_id_0eeaebb8_fk_users_id
            references users
            deferrable initially deferred
);

create index login_history_user_id_0eeaebb8 on login_history (user_id);
