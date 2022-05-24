# Social Network fastAPI
This is a full API for simaple social network develop with FastApi and Postgresql,
You can view the demo [here](https://www.social-network-fastapi.xyz/docs "here")

------------

### Table of contents
1. [Features](https://github.com/Yoad-Duani/social_network_fastAPI#Features "Features")
2. [Tests](https://github.com/Yoad-Duani/social_network_fastAPI#Tests "Tests")
3. [CI CD](https://github.com/Yoad-Duani/social_network_fastAPI#CI-CD "CI CD")
4. [Alembic](https://github.com/Yoad-Duani/social_network_fastAPI#Alembic "Alembic")

------------
## Features
Currently the project contains the following topics: 
&nbsp;
**Users**
There is a registration and login, the registration is verified by email verification, and the login is based on JWT.
Most features are conditional on a authenticated user and verified user.
&nbsp;
**Posts**
The user can create a post visible to everyone or in a specific group.
Can update or delete, and filter posts of your choice.
&nbsp;
**Votes**
Each user has the option to like the post, and can cancel the like
&nbsp;
**Comments**
Each user has the option to add a comment to the post.
The user can update or delete the comment.
&nbsp;
**Groups** 
Groups is the most multi-function feature,
Any verified user can create and manage a group,
Users can send a join request, the onwer of the group can choose whether to confirm or not.
The administrator of the group can block a user from the group, can exclude users,
or can replace himself with another member of the group

# 
# 





## Tests

## CI CD

## Alembic

##### Disclaimer
This project is based on [Sanjeev's](https://www.youtube.com/channel/UC2sYgV-NV6S5_-pqLGChoNQ "Sanjeev's") excellent tutorial.
Of course I added my own content and plan to add more advanced content like cookies, headers, background task, files, email verification and more.