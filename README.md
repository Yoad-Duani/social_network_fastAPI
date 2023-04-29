## Social Network fastAPI
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Yoad-Duani/social_network_fastAPI/build-deploy.yml?style=flat-square)
&nbsp;
![GitHub](https://img.shields.io/github/license/Yoad-Duani/social_network_fastAPI?style=flat-square)
&nbsp;
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/Yoad-Duani/social_network_fastAPI?style=flat-square)
&nbsp;
![Lines of code](https://img.shields.io/tokei/lines/github/Yoad-Duani/social_network_fastAPI?style=flat-square)
&nbsp;
![GitHub deployments](https://img.shields.io/github/deployments/Yoad-Duani/social_network_fastAPI/testing?label=deployments-state&style=flat-square)

This is a full API for simaple social network develop with FastApi Postgresql and MongoDB in microservices architecture, 
deployed as containerized application with Docker
<br/>
You can view the demo run on Ubuntu [here](https://www.social-network-fastapi.xyz/docs "here")
<br/>
You can get the project images [here](https://hub.docker.com/repository/docker/yoad787/social-network-fastapi "here")

------------

**Table of Contents**
- [Social Network fastAPI](#social-network-fastapi)
- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Docker-compose](#docker-compose)
    - [Kubernetes](#kubernetes)
    - [systemd](#systemd)
- [Features](#features)
- [Authentication \& Security](#authentication--security)
- [Tests](#tests)
- [CI CD](#ci-cd)
- [Database \& Alembic](#database--alembic)
- [env](#env)

------------
## Overview
This is a full API for simaple social network which was developed in microservices architecture,
<br/>
The architecture looks something like this:
<br/>

![](https://i.ibb.co/nmqWLZG/Whats-App-Image-2023-01-07-at-14-39-22.jpg)
> Example of docker-compose run on Ubuntu machine. <br/>
> I am not a professional developer, I have background in the IT field and recently I moved to devops <br/>
> The architecture could have been better and so the development itself

## Getting Started

You can view the Getting Started presentation **[Here](https://www.social-network-fastapi.xyz/guides/getting-started.md#/ "Here")**

#### Docker-compose
#### Kubernetes
#### systemd


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
There is email verification for new users
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
I decided to gain experience with `Keycloak`, so user authentication is performed with Keycloak and postgresql,
<br/>
I'm not sure if it fits the requirement for this kind of software, but for the purpose of studying I used it.
<br/>
I used the `fastapi-keycloak` package, and Keycloak 16.0.1, it's a bit outdated, but it's what fits the package right now.
<br/>
Because I didn't want user communication with Keycloak (That's why I said it might not be suitable for the project),
<br/>
For some of the requirements I did not find a way to work with the keycloak API, `action-token` for example,
<br/>
So I added some features with `JWT`.
<br/>
CORS (Cross Origin Resource Sharing) is implemented
<br/>
Using environment variables, you can see more in the `.env` section.




## Tests
There are currently 335 tests, implemented with pytest,
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
The project has a simple CI/CD based on GitHub Actions.
<br/>
For each push or pull request, a build is performed for a test environment with all the dependencies,
<br/>
If the build is completed successfully, two security jobs start running,
<br/>
The first is `git-guardian-scanning` - uses gitguardian's feature for scanning
<br/>
The second is `trufflehog-credential-verification` - Credential Verification Scanning
<br/>
If these two jobs are completed successfully, three jobs for deploy start running,
<br/>
The first is `deploy-to-heroku` the second is `deploy-to-ubunto-server` and the third is `update-docker-image`
<br/>
The last job that runs is `notification`, This is a custom email that gives status update on the other jobs
<br/>
All jobs use environmental variables, which are explained in the [.env section](https://github.com/Yoad-Duani/social_network_fastAPI#.env ".env")

## Database & Alembic
**Postgres**

<br/>
In the `main_server` I used postgresql and there are 8 tables:
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
I set the primary key to be `INT` type `(AUTO_INCREMENT)` and not `UUID` to simplify
<br>

**Mongodb**
In the `email_verification_server` I used mongodb and there are 1 DB and 1 collection,
Use for track users who need to verify email

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
