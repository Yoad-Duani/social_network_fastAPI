def user_serializer(user) -> dict:
    return{
        "id": str(user["_id"]),
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"]
    }


def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]