from typing import Any, Dict

from db_org import create_org, delete_org


def create_and_check_org(org_name: str) -> Dict[str, Any]:
    org_created: bool
    org_data: Dict[str, Any]
    org_created, org_data = create_org(org_name)

    assert org_created
    assert org_data["org_name"] == org_name

    return org_data


def test_create_org() -> None:
    """
    tests creating a new organization
    """
    name: str = "test create org"
    try:
        create_and_check_org(name)
    finally:
        delete_org(name)


def test_create_created_org() -> None:
    """
    tests creating an org that is already created.
    The second creation should fail.
    """
    name: str = "test already exist org"
    try:
        create_and_check_org(name)

        success, result = create_org(name)
        assert not success

    finally:
        delete_org(name)


def test_delete_org() -> None:
    """
    tests deleting an existing org
    """
    name: str = "test delete org"

    create_and_check_org(name)

    success: bool = delete_org(name)
    assert success

    # TODO: actually check that the org is gone and can no longer be accessed


def test_delete_deleted_org() -> None:
    """
    tests deleting an already deleted organization
    The second deletion should effectively be a no op
    """
    name: str = "test already deleted org"

    create_and_check_org(name)

    success: bool = delete_org(name)
    assert success

    success = delete_org(name)
    assert success
