docker compose \
    --env-file ./accounts_service/config/.env \
    logs -f $1
