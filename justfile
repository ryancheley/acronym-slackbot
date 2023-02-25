# run tests via pytest, creates coverage report, and then opens it up
test:
    coverage run -m pytest --cov-report html
    open htmlcov/index.html

# merge current branch with dev
branch_name := `git branch --show-current`
merge:
    echo "{{branch_name}}"
    git switch dev
    git merge "{{branch_name}}"

# prunes remote branches from github
prune:
    git remote prune github

# removes all but main and dev local branch
gitclean:
    git branch | grep -v "main" | grep -v "dev"| xargs git branch -D

# runs mutation testing
mutmut:
    echo 'This may take a while ... got do something nice for yourself'
    mutmut run

# builds the styles.css into the static directory
style-build:
    npx tailwindcss-cli@latest build jstoolchain/css/tailwind.css -c jstoolchain/tailwind.config.js -o staticfiles/css/styles.css

# checks the deployment for prod settings; will return error if the check doesn't pass
check:
    cp core/.env core/.env_staging
    cp core/.env_prod core/.env
    -python manage.py check --deploy
    cp core/.env_staging core/.env

# pulls from branch
sync branch:
    git switch {{branch}}
    git pull origin {{branch}}

# applies linting to project (black, djhtml, flake8)
lint:
    pre-commit run --all-files

run:
    python manage.py runserver

pip:
    pip install -U pip
    pip-compile --resolver=backtracking --generate-hashes --upgrade --output-file requirements.txt
    pip install -r requirements.txt