from typing import Any, Dict

import illu_db

illu_db.init_db()

# TODO: test against sql injection


def test_create_org():
    name: str = "test create org"
    try:
        success: bool
        result: Dict[str, Any]
        success, result = illu_db.create_org(name)

        assert success
        assert result["org_name"] == name
    finally:
        illu_db.delete_org(name)


def test_create_created_org():
    name: str = "test already exist org"
    try:
        success: bool
        result: Dict[str, Any]
        success, result = illu_db.create_org(name)

        assert success
        assert result["org_name"] == name

        success, result = illu_db.create_org(name)
        assert not success

    finally:
        illu_db.delete_org(name)


def test_delete_org():
    name: str = "test delete org"

    success: bool = False
    success, _ = illu_db.create_org(name)
    assert success

    success = illu_db.delete_org(name)

    assert success


def test_delete_deleted_org():
    name: str = "test already deleted org"

    illu_db.create_org(name)

    success: bool = illu_db.delete_org(name)
    assert success

    success: bool = illu_db.delete_org(name)
    assert success


class CommonUserData:
    phone_prefix: str
    phone: str
    user_name: str
    pw_hash: str

    def __init__(self, user_name):
        self.phone_prefix = "+1"
        self.phone = "1234567"
        self.user_name = user_name
        self.pw_hash = "fakehash"


def check_created_user(
    success: bool, user_data: CommonUserData, created_user_data: Dict[str, Any]
):
    assert success
    assert not (created_user_data["id"] is None)
    assert created_user_data["phone_prefix"] == user_data.phone_prefix
    assert created_user_data["phone"] == user_data.phone
    assert created_user_data["user_name"] == user_data.user_name


def test_create_user():
    user_data: CommonUserData = CommonUserData("test create user")

    try:
        success: bool
        result: Dict[str, Any]
        success, result = illu_db.create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
        )
        check_created_user(success, user_data, result)
    finally:
        illu_db.delete_user(user_data.phone_prefix, user_data.phone)


def test_create_created_user():
    user_data: CommonUserData = CommonUserData("test create created user")

    try:
        success: bool
        result: Dict[str, Any]
        success, result = illu_db.create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
        )
        check_created_user(success, user_data, result)

        success, result = illu_db.create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
        )
        assert not success
    finally:
        illu_db.delete_user(user_data.phone_prefix, user_data.phone)


def test_create_user_jwt():
    user_data: CommonUserData = CommonUserData("test create user with jwt")

    try:
        success: bool
        result: Dict[str, Any]
        success, result = illu_db.create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
            jwt="fakejwt",
        )
        check_created_user(success, user_data, result)
    finally:
        illu_db.delete_user(user_data.phone_prefix, user_data.phone)


def test_create_user_org_id():
    user_data: CommonUserData = CommonUserData("test create user with org_id")

    org_name: str = "create user with org id org"
    try:
        org_created: bool
        org_data: Dict[str, Any]
        org_created, org_data = illu_db.create_org(org_name)
        assert org_created

        user_created: bool
        user_data: Dict[str, Any]
        user_created, created_user_data = illu_db.create_user(
            phone_prefix=user_data.phone_prefix,
            phone=user_data.phone,
            user_name=user_data.user_name,
            pw_hash=user_data.pw_hash,
            org_id=org_data["id"],
        )

        check_created_user(user_created, user_data, created_user_data)
        assert created_user_data["org_id"] == org_data["id"]
    finally:
        illu_db.delete_user(user_data.phone_prefix, user_data.phone)
        illu_db.delete_org(org_name)


def test_delete_user():
    user_data = CommonUserData("test delete user")

    success: bool
    success, _ = illu_db.create_user(
        phone_prefix=user_data.phone_prefix,
        phone=user_data.phone,
        user_name=user_data.user_name,
        pw_hash=user_data.pw_hash,
    )
    assert success

    success = illu_db.delete_user(user_data.phone_prefix, user_data.phone)
    assert success


def test_delete_deleted_user():
    user_data = CommonUserData("test delete deleted user")

    success: bool
    success, _ = illu_db.create_user(
        phone_prefix=user_data.phone_prefix,
        phone=user_data.phone,
        user_name=user_data.user_name,
        pw_hash=user_data.pw_hash,
    )
    assert success

    success = illu_db.delete_user(user_data.phone_prefix, user_data.phone)
    assert success

    success = illu_db.delete_user(user_data.phone_prefix, user_data.phone)
    assert success
