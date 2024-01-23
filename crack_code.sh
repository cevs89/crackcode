#!/usr/bin/env bash
set -e


DOCKER_COMPOSE=`which docker-compose || echo "docker compose"`
COMPOSE="$DOCKER_COMPOSE -f docker-compose-local.yml"

case $1 in
  -h|--help|help)
    echo "crack_code.sh commands:"
    echo "  runserver: run the development stack"
    echo "  migrate: run migrate to DB"
    echo "  run: Just run de server"
    echo "  manage.py: run a manage.py command"
    ;;
  runserver)
    function cleanup {
      $COMPOSE down
    }
    trap cleanup EXIT
    $COMPOSE up -d --build --remove-orphans
    $COMPOSE exec web python manage.py migrate
    $COMPOSE logs -f web
    ;;
    migrate)
    shift
    $COMPOSE exec web python manage.py migrate
    ;;
    exec  )
    shift
    $COMPOSE exec web bash
    ;;
    run)
    function cleanup {
      $COMPOSE down
    }
    trap cleanup EXIT
    $COMPOSE up -d --build --remove-orphans
    $COMPOSE logs -f web
    ;;
    manage.py)
    shift
    $COMPOSE exec web python manage.py $@
    ;;
esac
