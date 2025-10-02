managepy := "battlecode/manage.py"
dev_db := "docker-compose.dev.yaml"


@default:
  echo "〽️ Available commands: \
  \n   db_up      - start database \
  \n   db_migrate - migrate database \
  \n   db_dw      - stops database \
  \n   serve      - run server"

db_up:
    docker compose -f {{dev_db}} up -d --build

db_migrate:
    uv run {{managepy}} makemigrations
    uv run {{managepy}} migrate

db_dw:
  docker compose -f {{dev_db}} down

serve:
  uv run {{managepy}} makemigrations
  uv run {{managepy}} migrate
  uv run {{managepy}} runserver
