docker compose \
    --env-file ./accounts_service/config/.env \
    up -d --build $1