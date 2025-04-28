CREATE DATABASE IF NOT EXISTS dating;
USE dating;

-- Итоговая таблица с автоматическим заполнением времени
CREATE TABLE IF NOT EXISTS interactions (
    `timestamp`       DateTime    DEFAULT now(),   -- по умолчанию текущее время
    `liker_id`        String,
    `liked_id`        String,
    `interaction_type` String
) ENGINE = Memory;

-- Источник из RabbitMQ без поля timestamp
CREATE TABLE IF NOT EXISTS rabbitmq_entry (
    liker_id          String,
    liked_id          String,
    interaction_type  String
) ENGINE = RabbitMQ
SETTINGS
    rabbitmq_host_port        = 'rabbitmq:5672',
    rabbitmq_exchange_name    = 'interactions_exchange',
    rabbitmq_routing_key_list = 'clickhouse_queue',
    rabbitmq_format           = 'JSONEachRow',
    rabbitmq_exchange_type    = 'fanout',
    rabbitmq_num_consumers    = 1,
    rabbitmq_queue_base       = 'clickhouse_queue',
    rabbitmq_queue_consume    = true
;

-- Materialized View для загрузки из rabbitmq_entry → interactions
CREATE MATERIALIZED VIEW IF NOT EXISTS event_view
TO interactions AS
SELECT
    liker_id,
    liked_id,
    interaction_type
FROM rabbitmq_entry;

-- Таблица для логирования взаимных лайков и пометки отправленных
CREATE TABLE IF NOT EXISTS mutual_likes_log (
    liker1     String,
    liker2     String,
    event_time DateTime,
    sent       UInt8     DEFAULT 0
) ENGINE = ReplacingMergeTree()
ORDER BY (liker1, liker2, event_time);

-- MV для заполнения mutual_likes_log при появлении взаимных лайков
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_mutual_likes
TO mutual_likes_log AS
SELECT
    least(i.liker_id, i.liked_id)   AS liker1,
    greatest(i.liker_id, i.liked_id) AS liker2,
    now()                            AS event_time
FROM interactions AS i
INNER JOIN interactions AS j
    ON j.liker_id = i.liked_id
   AND j.liked_id = i.liker_id
WHERE
    i.interaction_type = 'like'
  AND j.interaction_type = 'like'
  AND i.liker_id < i.liked_id
;
