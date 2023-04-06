from ast import List
from typing import Final, Dict, Any




###  User Routers Constants  ###

USER_ID_GE: Final[int] = 1  # The user's id must be 1 or more (g = Greater than, e = equal to)

EXAMPLE_USER_ID: Final[int] = 1  # Example of a user id




###  User Schemas Constants  ###

MIN_LENGTH_PASSWORD_USER_SCHEMA: Final[int] = 8

MIN_LENGTH_NAME_USER_SCHEMA: Final[int] = 2

MAX_LENGTH_NAME_USER_SCHEMA: Final[int] = 16

MIN_LENGTH_DESCRIPTION_USER_SCHEMA: Final[int] = 2

MAX_LENGTH_DESCRIPTION_USER_SCHEMA: Final[int] = 100

MIN_LENGTH_COMPANY_NAME_USER_SCHEMA: Final[int] = 2

MAX_LENGTH_COMPANY_NAME_USER_SCHEMA: Final[int] = 18

MIN_LENGTH_POSITION_USER_SCHEMA: Final[int] = 2

MAX_LENGTH_POSITION_USER_SCHEMA: Final[int] = 18




###  Post Routers Constants  ###

POST_ID_GE: Final[int] = 1  # The post's id must be 1 or more (g = Greater than, e = equal to)

EXAMPLE_POST_ID: Final[int] = 1  # Example of a post id

DEFAULT_LIMIT_GET_POSTS: Final[int] = 30  # The number of posts that will return in the GET request if not set offset

MAX_LIMIT_GET_POSTS: Final[int] = 160  # The maximum number of posts that will return in the GET request

MIN_LIMIT_GET_POSTS: Final[int] = 1  # The minimum number of posts to return in the get request, If there are no posts it will be returned blank

EXAMPLE_LIMIT_GET_POSTS: Final[int] = 10  # Example of limit GET posts

DEFAULT_SKIP_GET_POSTS: Final[int] = 0  # The number of posts to be skip if not set offset

MAX_SKIP_GET_POSTS: Final[int] = 5  # The maximum number of posts to be skip

MIN_SKIP_GET_POSTS: Final[int] = 0  # The minimum number of posts to be skip

EXAMPLE_SKIP_GET_POSTS: Final[int] = 1  # Example of skip GET posts

MIN_LENGTH_SEARCH_KEY_GET_POSTS: Final[int] = 2  # The minimum length of the keyword in GET posts

MAX_LENGTH_SEARCH_KEY_GET_POSTS: Final[int] = 20  # The maximum length of the keyword in GET posts

DEFAULT_VALUE_SEARCH_KEY_GET_POSTS: Final[str] = ""  # The default value of the keyword




###  Post Schemas Constants  ###

COMMENT_ID_GE: Final[int] = 1  # The comment's id must be 1 or more (g = Greater than, e = equal to)

MIN_LENGTH_TITLE_POST_SCHEMAS: Final[int] = 2  # The minimum length of the title in a post

MAX_LENGTH_TITLE_POST_SCHEMAS: Final[int] = 20  # The maximum length of the title in a post

MIN_LENGTH_CONTENT_POST_SCHEMAS: Final[int] = 2  # The minimum length of content in a post

MAX_LENGTH_CONTENT_POST_SCHEMAS: Final[int] = 560  # The maximum length of content in a post






###  Comments Routers Constants  ###

DEFAULT_LIMIT_GET_COMMENTS: Final[int] = 3  # The number of comments that will return in the GET request if not set offset

MAX_LIMIT_GET_COMMENTS: Final[int] = 20  # The maximum number of comments that will return in the GET request

MIN_LIMIT_GET_COMMENTS: Final[int] = 1  # The minimum number of comments to return in the get request, If there are no comments it will be returned blank

DEFAULT_SKIP_GET_COMMENTS: Final[int] = 0  # The number of comments to be skip if not set offset

MAX_SKIP_GET_COMMENTS: Final[int] = 5  # The maximum number of comments to be skip

MIN_SKIP_GET_COMMENTS: Final[int] = 0  # The minimum number of comments to be skip




###  Comments Schemas Constants  ###

MIN_LENGTH_CONTENT_COMMENT_SCHEMAS: Final[int] = 2  # The minimum length of content in a comment

MAX_LENGTH_CONTENT_COMMENT_SCHEMAS: Final[int] = 160  # The maximum length of content in a comment







###  Groups Routers Constants  ###

DEFAULT_LIMIT_GET_GROUPS: Final[int] = 16

MAX_LIMIT_GET_GROUPS: Final[int] = 40  # The maximum number of groups that will return in the GET request

MIN_LIMIT_GET_GROUPS: Final[int] = 1  # The minimum number of groups to return in the get request, If there are no group it will be returned blank

DEFAULT_VALUE_SEARCH_KEY_GET_GROUPS: Final[str] = ""  # The default value of the keyword

MIN_LENGTH_SEARCH_KEY_GET_GROUPS: Final[int] = 2  # The minimum length of the keyword in GET groups

MAX_LENGTH_SEARCH_KEY_GET_GROUPS: Final[int] = 20  # The maximum length of the keyword in GET groups

GROUPS_ID_GE: Final[int] = 1  # The group's id must be 1 or more (g = Greater than, e = equal to)

EXAMPLE_GROUPS_ID: Final[int] = 1  # Example of a group id





###  Groups Schemas Constants  ###

MIN_LENGTH_NAME_GROUP_SCHEMAS: Final[int] = 2  # The minimum length of the name of a group

MAX_LENGTH_NAME_GROUP_SCHEMAS: Final[int] = 20  # The maximum length of the name of a group

MIN_LENGTH_DESCRIPTION_GROUP_SCHEMAS: Final[int] = 2  # The minimum length of description in a group

MAX_LENGTH_DESCRIPTION_GROUP_SCHEMAS: Final[int] = 280  # The maximum length of description in a group














###  Vote Schemas Constants  ###

VOTE_MIN_VALUE: Final[int] = 0

VOTE_MAX_VALUE: Final[int] = 1







###  FastAPI Middleware  ###
ALLOW_ORIGINS : Final[List] = ["https://127.0.0.1:8000", "http://127.0.0.1:8000","https://social-network-fastapi-yoad.herokuapp.com/","https://social-network-fastapi.xyz"] 

ALLOW_METHODS : Final[List] = ["GET", "POST", "PUT", "DELETE"]



###  FastAPI Metadata  ###

FASTAPI_METADATA_DESCRIPTION: Final[str] = '''
This is a full API for simaple social network develop with FastApi and Postgresql

'''
FASTAPI_METADATA_TITLE: Final[str] = "Social Network FastAPI Documentation"

FASTAPI_METADATA_VERSION: Final[str]= "1.0.0"

FASTAPI_METADATA_CONTACT_NAME: Final[str]= "Yoad Duani"
