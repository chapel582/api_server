from typing import Any, Dict

import illu_db

illu_db.init_db()

# TODO: cleanup tests
# TODO: test inserting already existing org
# TODO: test deleting non-existent org
# TODO: delete org test
# TODO: test inserting already existing user
# TODO: create user test
# TODO: delete user test


def test_create_org():
    try:
        name: str = "test create org"
        success: bool
        result: Dict[str, Any]
        success, result = illu_db.create_org(name)

        assert success
        assert result["org_name"] == name
    finally:
        illu_db.delete_org(name)


def test_delete_org():
    name: str = "test delete org"

    illu_db.create_org(name)
    success: bool = illu_db.delete_org(name)

    assert success
