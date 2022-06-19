


# ###  Test Unauthorized Methods  ###

def test_get_user_head_method(client,test_user):
    id = test_user["id"]
    res = client.head(f"users/{id}")
    assert res.status_code == 405

def test_get_user_optinons_method(client,test_user):
    id = test_user["id"]
    res = client.options(f"users/{id}")
    assert res.status_code == 405

def test_get_user_patch_method(client,test_user):
    id = test_user["id"]
    res = client.patch(f"users/{id}")
    assert res.status_code == 405



