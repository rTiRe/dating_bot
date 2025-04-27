CREATE DATABASE IF NOT EXISTS dating;

USE dating;

-- Таблица для хранения результирующих событий (Memory или MergeTree по необходимости)
CREATE TABLE IF NOT EXISTS interactions (
    `timestamp` DateTime,
    `liker_id` UInt32,
    `liked_id` UInt32,
    `interaction_type` String
) ENGINE = Memory;

-- Источник данных из RabbitMQ
CREATE TABLE IF NOT EXISTS rabbitmq_entry (
    timestamp         UInt64,
    liker_id          UInt32,
    liked_id          UInt32,
    interaction_type  String
) ENGINE = RabbitMQ
SETTINGS
    rabbitmq_host_port       = 'rabbitmq:5672',
    rabbitmq_exchange_name   = 'interactions_exchange',
    rabbitmq_routing_key_list= 'interactions_queue',
    rabbitmq_format          = 'JSONEachRow',
    rabbitmq_exchange_type   = 'fanout',
    rabbitmq_num_consumers   = 1,
    rabbitmq_queue_base      = 'interactions_queue',
    rabbitmq_queue_consume   = true
;


-- Материализованное представление для переноса данных в конечную таблицу
CREATE MATERIALIZED VIEW IF NOT EXISTS event_view
TO interactions AS
SELECT
    toDateTime(timestamp / 1000000000) AS timestamp,
    liker_id,
    liked_id,
    interaction_type
FROM rabbitmq_entry;
