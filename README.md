# Social Network fastAPI
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Yoad-Duani/social_network_fastAPI/Build%20and%20Deploy%20Code?style=flat-square)

This is a full API for simaple social network develop with FastApi and Postgresql,
<br/>
You can view the demo [here](https://www.social-network-fastapi.xyz/docs "here")

------------

### Table of contents
- [Getting Started](https://github.com/Yoad-Duani/social_network_fastAPI#Getting-Started "Getting Started")
- [Features](https://github.com/Yoad-Duani/social_network_fastAPI#Features "Features")
- [Tests](https://github.com/Yoad-Duani/social_network_fastAPI#Tests "Tests")
- [CI CD](https://github.com/Yoad-Duani/social_network_fastAPI#CI-CD "CI CD")
- [Alembic](https://github.com/Yoad-Duani/social_network_fastAPI#Alembic "Alembic")
- [env](https://github.com/Yoad-Duani/social_network_fastAPI#env "env")

------------
## Getting Started

## Features
Currently the project contains the following topics: 
<br/>
<br/>
**Users**
<br/>
There is a registration and login, the registration is verified by email verification, and the login is based on JWT.
<br/>
Most features are conditional on a authenticated user and verified user.
<br/>
<br/>
**Posts**
<br/>
The user can create a post visible to everyone or in a specific group.
<br/>
Can update or delete, and filter posts of your choice.
<br/>
<br/>
**Votes**
<br/>
Each user has the option to like the post, and can cancel the like
<br/>
<br/>
**Comments**
<br/>
Each user has the option to add a comment to the post.
<br/>
The user can update or delete the comment.
<br/>
<br/>
**Groups** 
<br/>
Groups is the most multi-function feature,
Any verified user can create and manage a group,
<br/>
Users can send a join request, the onwer of the group can choose whether to confirm or not.
<br/>
The administrator of the group can block a user from the group, can exclude users,
or can replace himself with another member of the group






## Tests
There are currently 188 tests, implemented with pytest,
<br/>
Each test is isolated and independent of another, using `@pytest.fixture`
<br/>
There is a separate database for tests to maintain a proper test, which is initialized after each test
<br/>


    def session():
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)

## CI CD
The project has a very simple CI/CD based on GitHub Actions.
<br/>
For each push or pull request, a build is performed for a test environment with all the dependencies,
<br/>
If the build is completed successfully, two jobs start running,
<br/>
the first is `deploy-to-heroku` and the second is `deploy-to-ubunto-server`
<br/>
All jobs use environmental variables, which are explained in the [.env section](https://github.com/Yoad-Duani/social_network_fastAPI#.env ".env")

## Alembic
I use Alembic to manage the versions of the database,
<br/>
All versions can be found here: `/ alembic / versions /`
<br/>
The id of the latest version (the version currently in use) is stored in the `alembic_version` table

## env
A file containing the environment variables:
<br/>
DATABASE_HOSTNAME=
<br/>
DATABASE_PORT=
<br/>
DATABASE_PASSWORD=
<br/>
DATABASE_NAME=
<br/>
DATABASE_USERNAME=
<br/>
SECRET_KEY=
<br/>
ALGORITHM=
<br/>
ACCESS_TOKEN_EXPIRE_MINUTES=


##### Disclaimer
This project is based on [Sanjeev's](https://www.youtube.com/channel/UC2sYgV-NV6S5_-pqLGChoNQ "Sanjeev's") excellent tutorial.
Of course I added my own content and plan to add more advanced content like cookies, headers, background task, files, email verification and more.