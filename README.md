
# Acronym Slackbot

This is a Slackbot that I made to return the definitions for acronyms. While it's initial intention was for use in the Medical Sector, it can probably be used anywhere with lots of [TLA](https://en.wikipedia.org/wiki/Three-letter_acronym)

## Authors

- [@ryancheley](https://www.github.com/ryancheley)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SLACK_VERIFICATION_TOKEN`

`SLACK_BOT_USER_TOKEN`

`CONFLUENCE_LINK`

`DEBUG`

`SECRET_KEY`

`SECURE_HSTS_INCLUDE_SUBDOMAINS`

`SECURE_SSL_REDIRECT`

`SECURE_HSTS_SECONDS`

`SECURE_HSTS_PRELOAD`

`SESSION_COOKIE_SECURE`

`CSRF_COOKIE_SECURE`

`ALLOWED_HOSTS`

## Development

Development is done locally by creating a feature branch

```
git switch -c feature_branch_name
```

Once local development is ready to be moved to Prod you will push the feature branch to github

```
git push origin feature_branch_name
```

This will push to GitHub and run the GitHub Action `django.yml` which will run tests.

## Deployment

In order to deploy to `prod` you will need to perform a Pull Request to `main` and Merge on GitHub
