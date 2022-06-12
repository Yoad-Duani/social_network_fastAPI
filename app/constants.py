from typing import Final




###  User Routers Constants  ###

USER_ID_GE: Final[int] = 1  # The user's id must be 1 or more (g = Greater than, e = equal to)

EXAMPLE_USER_ID: Final[int] = 1  # Example of a user id





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

MIN_LENGTH_TITLE_POST_SCHEMAS: Final[int] = 2  # The minimum length of the title in a post

MAX_LENGTH_TITLE_POST_SCHEMAS: Final[int] = 20  # The maximum length of the title in a post

MIN_LENGTH_CONTENT_POST_SCHEMAS: Final[int] = 2  # The minimum length of content in a post

MAX_LENGTH_CONTENT_POST_SCHEMAS: Final[int] = 560  # The maximum length of content in a post
