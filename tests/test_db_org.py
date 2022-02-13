from typing import Any, Dict

from db_org import create_org, delete_org


def test_create_org() -> None:
    """
    tests creating a new organization
    """
    name: str = "test create org"
    try:
        success: bool
        result: Dict[str, Any]
        success, result = create_org(name)

        assert success
        assert result["org_name"] == name
    finally:
        delete_org(name)


def test_create_created_org() -> None:
    """
    tests creating an org that is already created.
    The second creation should fail.
    """
    name: str = "test already exist org"
    try:
        success: bool
        result: Dict[str, Any]
        success, result = create_org(name)

        assert success
        assert result["org_name"] == name

        success, result = create_org(name)
        assert not success

    finally:
        delete_org(name)


def test_delete_org() -> None:
    """
    tests deleting an existing org
    """
    name: str = "test delete org"

    success: bool = False
    success, _ = create_org(name)
    assert success

    success = delete_org(name)

    assert success


def test_delete_deleted_org() -> None:
    """
    tests deleting an already deleted organization
    The second deletion should effectively be a no op
    """
    name: str = "test already deleted org"

    create_org(name)

    success: bool = delete_org(name)
    assert success

    success = delete_org(name)
    assert success
