-- Initial
-- depends: 

create extension if not exists "uuid-ossp";

create schema if not exists dating;

create table dating."accounts" (
    id uuid primary key default uuid_generate_v4(),
    telegram_id int8 not null unique,
    telegram_username varchar(32),
    created_at timestamp default now(),
    updated_at timestamp default now()
);

create or replace function update_updated_at_column()
    returns trigger
    language plpgsql
as
$$
begin
    new.updated_at = now();
    return new;
end;
$$;

create trigger update_accounts_updated_at
before update on dating."accounts"
for each row
execute function update_updated_at_column();