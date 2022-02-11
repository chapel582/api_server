from typing import Any, Dict

import illu_db

illu_db.init_db()

# TODO: test inserting already existing user
# TODO: create user test
# TODO: delete user test
# TODO: create a user with an org
# TODO: create a user with a jwt
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


def test_insert_already_exist_org():
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


def test_create_user():
    phone_prefix: str = "+1"
    phone: str = "1234567"
    user_name: str = "test create user"
    pw_hash: str = "fakehash"

    try:
        success: bool
        result: Dict[str, Any]
        success, result = illu_db.create_user(
            phone_prefix=phone_prefix, phone=phone, user_name=user_name, pw_hash=pw_hash
        )

        assert success
        assert not (result.get("id") is None)
        assert result["phone_prefix"] == phone_prefix
        assert result["phone"] == phone
        assert result["user_name"] == user_name
    finally:
        illu_db.delete_user(phone_prefix, phone)


def test_delete_user():
    phone_prefix: str = "+1"
    phone: str = "1234567"
    user_name: str = "test delete user"
    pw_hash: str = "fakehash"

    success: bool
    success, _ = illu_db.create_user(
        phone_prefix=phone_prefix, phone=phone, user_name=user_name, pw_hash=pw_hash
    )
    assert success

    success = illu_db.delete_user(phone_prefix, phone)
    assert success


def test_delete_deleted_user():
    phone_prefix: str = "+1"
    phone: str = "1234567"
    user_name: str = "test delete deleted user"
    pw_hash: str = "fakehash"

    success: bool
    success, _ = illu_db.create_user(
        phone_prefix=phone_prefix, phone=phone, user_name=user_name, pw_hash=pw_hash
    )
    assert success

    success = illu_db.delete_user(phone_prefix, phone)
    assert success

    success = illu_db.delete_user(phone_prefix, phone)
    assert success
