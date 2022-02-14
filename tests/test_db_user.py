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


def check_get_user_by_id(user_id: int, expected_user_data: Dict[str, Any]) -> None:
    users: List[Dict[str, Any]]
    success, users = get_user(user_id=user_id)
    assert success
    assert len(users) == 1
    assert users[0] == expected_user_data


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

        check_get_user_by_id(created_user_data["id"], created_user_data)
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

        check_get_user_by_id(created_user_data["id"], created_user_data)
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)


def test_update_user_one_field() -> None:
    user_data: CommonUserData = CommonUserData(
        "test update user function with one arguments"
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

        check_get_user_by_id(created_user_data["id"], expected_user_data)
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)


def test_update_user_two_fields() -> None:
    user_data: CommonUserData = CommonUserData(
        "test update user function with two arguments"
    )

    try:
        org_name: str = "test org"
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
        )
        check_created_user(user_created, user_data, created_user_data)

        new_user_name: str = "new_user_name"
        user_updated: bool
        user_updated = update_user(
            user_data.phone_prefix,
            user_data.phone,
            user_name=new_user_name,
            org_id=org_data["id"],
        )
        assert user_updated

        expected_user_data: Dict[str, Any] = created_user_data.copy()
        expected_user_data["user_name"] = new_user_name
        expected_user_data["org_id"] = org_data["id"]

        check_get_user_by_id(created_user_data["id"], expected_user_data)
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)
        delete_org(org_name)


def test_update_user_phone() -> None:
    user_data: CommonUserData = CommonUserData(
        "test update user function with phone argument"
    )
    new_phone: str = "0000000"
    assert new_phone != user_data.phone

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
        user_updated = update_user(
            user_data.phone_prefix, user_data.phone, new_phone=new_phone
        )
        assert user_updated

        expected_user_data: Dict[str, Any] = created_user_data.copy()
        expected_user_data["phone"] = new_phone

        check_get_user_by_id(created_user_data["id"], expected_user_data)
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)
        delete_user(user_data.phone_prefix, new_phone)


def test_update_user_prefix_and_phone() -> None:
    user_data: CommonUserData = CommonUserData(
        "test update user function with phone argument"
    )
    new_phone: str = "0000000"
    new_prefix: str = "+009"
    assert new_phone != user_data.phone
    assert new_prefix != user_data.phone_prefix

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
        user_updated = update_user(
            user_data.phone_prefix,
            user_data.phone,
            new_phone=new_phone,
            new_phone_prefix=new_prefix,
        )
        assert user_updated

        expected_user_data: Dict[str, Any] = created_user_data.copy()
        expected_user_data["phone"] = new_phone
        expected_user_data["phone_prefix"] = new_prefix

        check_get_user_by_id(created_user_data["id"], expected_user_data)
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)
        delete_user(new_prefix, new_phone)


def test_update_user_all_args() -> None:
    user_data: CommonUserData = CommonUserData(
        "test update user function with all arguments"
    )
    new_user_name: str = "new user name"
    new_jwt_token: str = "new fake jwt token"
    new_pw_hash: str = "new fake pw hash"
    new_phone: str = "0000000"
    new_prefix: str = "+009"
    assert new_user_name != user_data.user_name
    assert new_phone != user_data.phone
    assert new_prefix != user_data.phone_prefix
    assert new_pw_hash != user_data.pw_hash

    org_name: str = "test org"
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
        )
        check_created_user(user_created, user_data, created_user_data)

        user_updated: bool
        user_updated = update_user(
            user_data.phone_prefix,
            user_data.phone,
            new_phone=new_phone,
            new_phone_prefix=new_prefix,
            user_name=new_user_name,
            pw_hash=new_pw_hash,
            jwt=new_jwt_token,
            org_id=org_data["id"],
        )
        assert user_updated

        expected_user_data: Dict[str, Any] = created_user_data.copy()
        expected_user_data["phone"] = new_phone
        expected_user_data["phone_prefix"] = new_prefix
        expected_user_data["user_name"] = new_user_name
        expected_user_data["org_id"] = org_data["id"]

        check_get_user_by_id(created_user_data["id"], expected_user_data)
    finally:
        delete_user(user_data.phone_prefix, user_data.phone)
        delete_user(new_prefix, new_phone)
        delete_org(org_name)


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
    # TODO: check that user is gone and can no longer be queried


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
