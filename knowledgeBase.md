# Knowledge Base


## Services

|  Server Name | Port  |
| ------------ | ------------ |
| main_server  |  8000:8000 |
| email_verification_server  |  8001:8001 |
| auth_server  |  8002:8002 |
| keycloak  |  8085:8080 |
| backend_for_frontend  |  8003:8003 |
| postgres_main  |  8051:5432 |
| postgres_auth  |  8052:5432 |
| mongodb-email-verification  |  8053:27017 |

<br/>

## Logs and Tracing
I created a simple system of logs using the logging package (Looking back I would have chosen loguru..),
<br/>
I added a UUID to each request, and thus each request that reaches the BFF service receives a UUID in the middleware,
<br/>
The UUID is transferred to the other servers, and every log related to that request will have the same UUID.
<br/>
This way I can know which request each log belongs to.
<br/>
The format looks like this:
<br/>

`INFO:     2023-04-15 23:30:18 [MainThread]  [main-logger]  (2f70bed8-8f74-410c-a20f-41e179c8ad23)  <The log message>`
<br/>

I used the `uvicorn.logging.DefaultFormatter` and I did a little personalization of my own
<br/>
It was implemented in a very basic way, there are alternatives and libraries to do this in a more sophisticated and elegant way,
<br/>
But I decided not to delve into another topic in this project because it is comprehensive anyway

##### Disclaimer
This is not the best practice for the observability system,
<br/>
The correct format should be json (for optimal machine reading).
<br/>
You'll probably want to use tools more suited to a disturbed system than the simple logger,
<br/>

like `Structlog`, `Datadog`, `OpenTelemetry` and more. 
 