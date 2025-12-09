# run tests via pytest, creates coverage report, and then opens it up
@test:
    coverage run -m pytest --cov-report html
    open htmlcov/index.html

# merge current branch with dev
branch_name := `git branch --show-current`
@merge:
    echo "{{branch_name}}"
    git switch dev
    git merge "{{branch_name}}"

# prunes remote branches from github
@prune:
    git remote prune github

# removes all but main and dev local branch
@gitclean:
    git branch | grep -v "main" | grep -v "dev"| xargs git branch -D

# runs mutation testing
@mutmut:
    echo 'This may take a while ... got do something nice for yourself'
    mutmut run

# checks the deployment for prod settings; will return error if the check doesn't pass
@check:
    cp core/.env core/.env_staging
    cp core/.env_prod core/.env
    -python manage.py check --deploy
    cp core/.env_staging core/.env

# pulls from branch
@sync branch:
    git switch {{branch}}
    git pull origin {{branch}}

# applies linting to project (ruff, djhtml, tryceratops, django-upgrade)
@lint:
    prek run --all-files

@run:
    python manage.py runserver

@pip:
    pip install -U pip uv
    uv pip install -e ".[dev]"

# Docker commands
@docker-build:
    docker build -t acronym-slackbot:latest .

@docker-up:
    docker compose up -d

@docker-down:
    docker compose down

@docker-logs:
    docker compose logs -f web

@docker-shell:
    docker compose exec web /bin/bash

@docker-test:
    docker compose exec web pytest

@docker-restart:
    docker compose restart web

@docker-clean:
    docker compose down -v
    docker system prune -f