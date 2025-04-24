-- Initial
-- depends:

create extension if not exists "uuid-ossp";

create schema if not exists dating;

create table dating."profiles" (
    id uuid primary key default uuid_generate_v4(),
    account_id uuid not null unique,
    first_name varchar(32),
    last_name varchar(32),
    age int8,
    gender char(1),
    biography text,
    language_locale varchar(2),
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    image_names text[] not null default ARRAY[]::text[]
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
before update on dating."profiles"
for each row
execute function update_updated_at_column();
