# run tests via pytest, creates coverage report, and then opens it up
test:
    coverage run -m pytest
    open htmlcov/index.html

# deploys the code to the `target` server, which can be either an IP Address or alias to an IP
deploy target: test
    @echo 'Deploying to {{target}}...'
    cd {{invocation_directory()}}/scripts; ./deploy.sh {{target}}

# merge current branch with dev
branch_name := `git branch --show-current`
merge:
    @echo "{{branch_name}}"
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
    @echo 'This may take a while ... got do something nice for yourself'
    mutmut run

# builds the styles.css into the static directory
style-build:
    npx tailwindcss-cli@latest build jstoolchain/css/tailwind.css -c jstoolchain/tailwind.config.js -o staticfiles/css/styles.css

# checks the deployment for prod settings; will return error if the check doesn't pass
check:
    cp {{cookiecutter.project_slug}}/.env {{cookiecutter.project_slug}}/.env_staging
    cp {{cookiecutter.project_slug}}/.env_prod {{cookiecutter.project_slug}}/.env
    -python manage.py check --deploy
    cp {{cookiecutter.project_slug}}/.env_staging {{cookiecutter.project_slug}}/.env

# pulls from branch
sync branch:
    git switch {{branch}}
    git pull github {{branch}}

# applies linting to project (black, djhtml, flake8)
lint:
    pre-commit run --all-files

# creates graph of models
graph:
    python manage.py graph_models \
        {{cookiecutter.project_slug}}
        -o my_project_visualized.png