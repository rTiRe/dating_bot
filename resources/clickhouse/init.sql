CREATE DATABASE IF NOT EXISTS dating;
USE dating;

-- Итоговая таблица с автоматическим заполнением времени
CREATE TABLE IF NOT EXISTS interactions (
    `timestamp`       DateTime    DEFAULT now(),   -- по-умолчанию текущее время
    `liker_id`        UInt32,
    `liked_id`        UInt32,
    `interaction_type`String
) ENGINE = Memory;

-- Источник из RabbitMQ остаётся без поля timestamp
CREATE TABLE IF NOT EXISTS rabbitmq_entry (
    liker_id          UInt32,
    liked_id          UInt32,
    interaction_type  String
) ENGINE = RabbitMQ
SETTINGS
    rabbitmq_host_port       = 'rabbitmq:5672',
    rabbitmq_exchange_name   = 'interactions_exchange',
    rabbitmq_routing_key_list= 'clickhouse_queue',
    rabbitmq_format          = 'JSONEachRow',
    rabbitmq_exchange_type   = 'fanout',
    rabbitmq_num_consumers   = 1,
    rabbitmq_queue_base      = 'clickhouse_queue',
    rabbitmq_queue_consume   = true
;

-- MV вставляет только три поля — timestamp заполняется default now()
CREATE MATERIALIZED VIEW IF NOT EXISTS event_view
TO interactions AS
SELECT
    liker_id,
    liked_id,
    interaction_type
FROM rabbitmq_entry;
