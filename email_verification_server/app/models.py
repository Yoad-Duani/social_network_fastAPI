def user_serializer(user) -> dict:
    return{
        "user_id": user["_id"],
        "name": user["name"],
        "email": user["email"]
    }


def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]