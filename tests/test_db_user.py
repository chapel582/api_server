from typing import Any, Dict, List

from db_org import create_org, delete_org
from db_user import create_user, get_user, update_user, delete_user


class CommonUserData:
    """
    common user data for user tests
    """

    phone_prefix: str
    phone: str
    user_name: str
    pw_hash: str

    def __init__(self, user_name):
        """
        user_name:
            the name of the user
        """
        self.phone_prefix = "+1"
        self.phone = "1234567"
        self.user_name = user_name
        self.pw_hash = "fakehash"


def check_created_user(
    success: bool, user_data: CommonUserData, created_user_data: Dict[str, Any]
) -> None:
    """
    Check whether the user creation succeeded. Asserts on failure

    success:
        The boolean returned from create_user
    user_data:
        The user data used for creation
    created_user_data:
        The user data returned from create_user
    """
    assert success
    assert not (created_user_data["id"] is None)
    assert created_user_data["phone_prefix"] == user_data.phone_prefix
    assert created_user_data["phone"] == user_data.phone
    assert created_user_data["user_name"] == user_data.user_name


def test_create_user() -> None:
    """
    tests creating a user
    """
    user_data: CommonUserData = CommonUserData("test create user")

    try:
        success: bool
        result: Dict[str, Any]
        success, result = create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
        )
        check_created_user(success, user_data, result)
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)


def test_create_created_user() -> None:
    """
    Tests creating an already created user
    The second create call should fail
    """
    user_data: CommonUserData = CommonUserData("test create created user")

    try:
        success: bool
        result: Dict[str, Any]
        success, result = create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
        )
        check_created_user(success, user_data, result)

        success, result = create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
        )
        assert not success
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)


def test_create_user_jwt() -> None:
    """
    Tests creating a user with the optional jwt parameter
    """
    # TODO: check that jwt token is in the user data
    user_data: CommonUserData = CommonUserData("test create user with jwt")

    try:
        success: bool
        result: Dict[str, Any]
        success, result = create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
            jwt="fakejwt",
        )
        check_created_user(success, user_data, result)
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)


def test_create_user_org_id() -> None:
    """
    Tests creating a user with the optional org data
    """
    user_data: CommonUserData = CommonUserData("test create user with org_id")

    org_name: str = "create user with org id org"
    try:
        org_created: bool
        org_data: Dict[str, Any]
        org_created, org_data = create_org(org_name)
        assert org_created

        user_created: bool
        created_user_data: Dict[str, Any]
        user_created, created_user_data = create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
            org_id=org_data["id"],
        )

        check_created_user(user_created, user_data, created_user_data)
        assert created_user_data["org_id"] == org_data["id"]
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)
        delete_org(org_name)


def test_get_user_id() -> None:
    """
    test get user by id
    """
    user_data: CommonUserData = CommonUserData("test create user with org_id")

    try:
        user_created: bool
        created_user_data: Dict[str, Any]
        user_created, created_user_data = create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
        )
        check_created_user(user_created, user_data, created_user_data)

        get_user_data_check: List[Dict[str, Any]]
        success, get_user_data_check = get_user(user_id=created_user_data["id"])
        assert success
        assert get_user_data_check[0] == created_user_data
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)


def test_update_user_no_fields() -> None:
    user_data: CommonUserData = CommonUserData(
        "test update user function without any arguments"
    )

    try:
        user_created: bool
        created_user_data: Dict[str, Any]
        user_created, created_user_data = create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
        )
        check_created_user(user_created, user_data, created_user_data)

        user_updated: bool
        user_updated = update_user(user_data.phone_prefix, user_data.phone)
        assert user_updated

        got_user: bool
        get_user_data_check: List[Dict[str, Any]]
        got_user, get_user_data_check = get_user(user_id=created_user_data["id"])
        assert got_user
        assert get_user_data_check[0] == created_user_data
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)


def test_update_user_one_field() -> None:
    user_data: CommonUserData = CommonUserData(
        "test update user function without any arguments"
    )

    try:
        user_created: bool
        created_user_data: Dict[str, Any]
        user_created, created_user_data = create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
        )
        check_created_user(user_created, user_data, created_user_data)

        new_user_name: str = "new_user_name"
        user_updated: bool
        user_updated = update_user(
            user_data.phone_prefix, user_data.phone, user_name=new_user_name
        )
        assert user_updated

        expected_user_data: Dict[str, Any] = created_user_data.copy()
        expected_user_data["user_name"] = new_user_name

        got_user: bool
        get_user_data_check: List[Dict[str, Any]]
        got_user, get_user_data_check = get_user(user_id=created_user_data["id"])
        assert got_user
        assert get_user_data_check[0] == expected_user_data
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)


# def test_update_user_two_fields():
#     pass

# def test_update_user_all_fields():
#     pass


def test_delete_user() -> None:
    """
    Test deleting a user
    """
    user_data = CommonUserData("test delete user")

    success: bool
    success, _ = create_user(
        phone_prefix=user_data.phone_prefix,
        phone=user_data.phone,
        user_name=user_data.user_name,
        pw_hash=user_data.pw_hash,
    )
    assert success

    success = delete_user(user_data.phone_prefix, user_data.phone)
    assert success


def test_delete_deleted_user() -> None:
    """
    Test deleting an already deleted user
    """
    user_data = CommonUserData("test delete deleted user")

    success: bool
    success, _ = create_user(
        phone_prefix=user_data.phone_prefix,
        phone=user_data.phone,
        user_name=user_data.user_name,
        pw_hash=user_data.pw_hash,
    )
    assert success

    success = delete_user(user_data.phone_prefix, user_data.phone)
    assert success

    success = delete_user(user_data.phone_prefix, user_data.phone)
    assert success
