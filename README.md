# Social Network fastAPI
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Yoad-Duani/social_network_fastAPI/Build%20and%20Deploy%20Code?style=flat-square)
&nbsp;
![GitHub](https://img.shields.io/github/license/Yoad-Duani/social_network_fastAPI?style=flat-square)
&nbsp;
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/Yoad-Duani/social_network_fastAPI?style=flat-square)
&nbsp;
![GitHub deployments](https://img.shields.io/github/deployments/Yoad-Duani/social_network_fastAPI/testing?label=deployments-state&style=flat-square)

This is a full API for simaple social network develop with FastApi and Postgresql,
<br/>
You can view the demo [here](https://www.social-network-fastapi.xyz/docs "here")
<br/>
You can also get the project image for running on a docker [here](https://hub.docker.com/repository/docker/yoad787/social-network-fastapi "here")

------------

### Table of contents
- [Getting Started](https://github.com/Yoad-Duani/social_network_fastAPI#Getting-Started "Getting Started")
- [Features](https://github.com/Yoad-Duani/social_network_fastAPI#Features "Features")
- [Authentication & Security](https://github.com/Yoad-Duani/social_network_fastAPI#Authentication-&-Security "Authentication & Security")
- [Tests](https://github.com/Yoad-Duani/social_network_fastAPI#Tests "Tests")
- [CI CD](https://github.com/Yoad-Duani/social_network_fastAPI#CI-CD "CI CD")
- [Database & Alembic](https://github.com/Yoad-Duani/social_network_fastAPI#Database-&-Alembic "Database & Alembic")
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


## Authentication & Security
User authentication is performed with JWT, most requests require authentication
<br/>
Secure password hashing is performed
<br/>
CORS (Cross Origin Resource Sharing) is implemented
<br/>
Using environment variables, you can see more in the `.env` file



## Tests
There are currently 268 tests, implemented with pytest,
<br/>
Each test is isolated and independent of another, using `@pytest.fixture`
<br/>
There is a separate database for tests to maintain a proper test, which is initialized after each test
<br/>
For data validation I used `Field` and `validator` imported from `Pydantic`
<br/>
And `Query` `Path` and `Body` imported from `fastapi`
<br/>
You can see more in `validators.py`  and `schemas.py` Files


## CI CD
The project has a very simple CI/CD based on GitHub Actions.
<br/>
For each push or pull request, a build is performed for a test environment with all the dependencies,
<br/>
If the build is completed successfully, three jobs start running,
<br/>
The first is `deploy-to-heroku` the second is `deploy-to-ubunto-server` and the third is `update-docker-image`
<br/>
The last job that runs is notification, This is a custom email that gives status update to other jobs
<br/>
All jobs use environmental variables, which are explained in the [.env section](https://github.com/Yoad-Duani/social_network_fastAPI#.env ".env")

## Database & Alembic
I used postgresql and there are 8 tables:
<br/>
`Post`, `User`, `Vote`, `Comment`, `Groups`, `UserInGroups`, `JoinRequestGroups`, `alembic_version`
<br/>
**alembic_version -** This table is created by default following the use of alembic
<br/>
You can see all the fields and the relationships between the tables in the `app/models.py` file
<br/>
**All relevant tables support CASCADE, and I adhered to the ACID guidelines**
<br/>
All DB access has been implemented with SQLAlchemy
<br/>
I use Alembic to manage the versions of the database,
<br/>
All versions can be found here: `/ alembic / versions /`
<br/>
The id of the latest version (the version currently in use) is stored in the `alembic_version` table
<br/>
I set the primary key to be `INT` type `(AUTO_INCREMENT)` and not `UUID`


## env
A file containing the environment variables:
<br/>
**For These environment variables, it is required to set up a database first:**
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
**These environment variables required for create token, password hash and expiration for token:**
<br/>
SECRET_KEY=
<br/>
ALGORITHM=
<br/>
ACCESS_TOKEN_EXPIRE_MINUTES=
<br/>
<br/>
Note that there is a separate test database that also needs to be set up,
<br/>
At the moment his name is `{settings.database_name}_test` (like the main only with _test at the end)
<br/>
You can change its definition here: `/tests/conftest.py`
<br>
To use Workflow for GitHub Actions, you required to include additional environment variables in GitHub Secrets
<br>


##### Disclaimer
This project is based on [Sanjeev's](https://www.youtube.com/channel/UC2sYgV-NV6S5_-pqLGChoNQ "Sanjeev's") excellent tutorial.
Of course I added my own content and plan to add more advanced content like cookies, headers, background task, files, email verification and more.