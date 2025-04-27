CREATE DATABASE IF NOT EXISTS event;

USE event;

CREATE TABLE IF NOT EXISTS event (
    `timestamp` DateTime,
    `id` UInt32,
    `body` String
) Engine = Memory;

CREATE TABLE IF NOT EXISTS rabbitmq_entry
(
    `timestamp` UInt64,
    `id` UInt32,
    `body` String
) ENGINE = RabbitMQ SETTINGS
    rabbitmq_host_port = 'rabbitmq:5672',
    rabbitmq_exchange_name = 'interactions_exchange',
    rabbitmq_routing_key_list = 'interactions_queue',
    rabbitmq_format = 'JSONEachRow',
    rabbitmq_exchange_type = 'fanout',
    rabbitmq_num_consumers = 1
    ;

CREATE MATERIALIZED VIEW IF NOT EXISTS event_view
TO event AS
SELECT
    toDateTime(toUInt64(divide(timestamp, 1000000000))) AS timestamp,
    id AS id,
    body AS body
FROM rabbitmq_entry;
