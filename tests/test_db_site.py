from typing import Any, Dict, List

from db_org import delete_org
from db_site import create_site, get_site, update_site, delete_site
from test_db_org import create_and_check_org

# TODO: update site by name
# TODO: all the different update site parameters


def create_and_check_site(site_name: str, org_id: int) -> Dict[str, Any]:
    success: bool
    site_data: Dict[str, Any]
    success, site_data = create_site(site_name, org_id)
    assert success
    assert site_data["name"] == site_name
    assert site_data["org_id"] == org_id
    assert site_data["is_active"] is True

    return site_data


def test_create_site() -> None:
    """
    tests creating a site
    """
    org_name: str = "test org for site"
    site_name: str = "test create site"
    try:
        org_data: Dict[str, Any] = create_and_check_org(org_name)

        create_and_check_site(site_name, org_data["id"])
    finally:
        delete_site(name=site_name)
        delete_org(org_name)


def test_create_created_site() -> None:
    """
    Tests creating an already created site
    The second create call should fail
    """
    org_name = "test org for site"
    site_name = "test create created site"
    try:
        org_data: Dict[str, Any] = create_and_check_org(org_name)

        create_and_check_site(site_name, org_data["id"])

        success: bool
        success, _ = create_site(site_name, org_data["id"])
        assert not success
    finally:
        delete_site(name=site_name)
        delete_org(org_name)


def test_create_created_site_diff_org() -> None:
    org_one_name = "test org one"
    org_two_name = "test org two"
    site_one_name = "test site"
    site_two_name = "test site"
    try:
        org_one_data: Dict[str, Any] = create_and_check_org(org_one_name)
        org_two_data: Dict[str, Any] = create_and_check_org(org_two_name)

        create_and_check_site(site_one_name, org_one_data["id"])
        create_and_check_site(site_two_name, org_two_data["id"])
    finally:
        delete_site(name=site_one_name)
        delete_site(name=site_two_name)
        delete_org(org_one_name)
        delete_org(org_two_name)


def test_get_site_id() -> None:
    """ """
    org_name = "test org for site"
    site_name = "test get site by id"
    try:
        org_data: Dict[str, Any] = create_and_check_org(org_name)

        created_site: Dict[str, Any] = create_and_check_site(site_name, org_data["id"])

        success: bool
        sites: List[Dict[str, Any]]
        success, sites = get_site(site_id=created_site["id"])
        assert success
        assert len(sites) == 1
        assert sites[0] == created_site
    finally:
        delete_site(name=site_name)
        delete_org(org_name)


def test_get_site_name() -> None:
    """ """
    org_name = "test org for site"
    site_name = "test get site by name"
    try:
        org_data: Dict[str, Any] = create_and_check_org(org_name)

        created_site: Dict[str, Any] = create_and_check_site(site_name, org_data["id"])

        success: bool
        sites: List[Dict[str, Any]]
        success, sites = get_site(name=site_name)
        assert success
        assert len(sites) == 1
        assert sites[0] == created_site
    finally:
        delete_site(name=site_name)
        delete_org(org_name)


def test_get_org_sites() -> None:
    """ """
    org_name = "test org for site"
    site_one_name = "test site one"
    site_two_name = "test site two"

    try:
        org_data: Dict[str, Any] = create_and_check_org(org_name)

        site_one_data: Dict[str, Any] = create_and_check_site(
            site_one_name, org_data["id"]
        )

        site_two_data: Dict[str, Any] = create_and_check_site(
            site_two_name, org_data["id"]
        )

        success: bool
        sites: List[Dict[str, Any]]
        success, sites = get_site(org_id=org_data["id"])
        assert success
        assert len(sites) == 2
        assert sites[0] == site_one_data
        assert sites[1] == site_two_data
    finally:
        delete_site(name=site_one_name)
        delete_site(name=site_two_name)
        delete_org(org_name)


def test_update_site_by_id() -> None:
    """ """
    org_name = "test org for site"
    site_name = "test update site"
    new_site_name = "updated site name"
    try:
        org_data: Dict[str, Any] = create_and_check_org(org_name)

        created_site: Dict[str, Any] = create_and_check_site(site_name, org_data["id"])

        sites: List[Dict[str, Any]]
        success: bool = update_site(site_id=created_site["id"], new_name=new_site_name)
        assert success

        expected_site_data: Dict[str, Any] = created_site.copy()
        expected_site_data["name"] = new_site_name

        success, sites = get_site(site_id=created_site["id"])
        assert success
        assert len(sites) == 1
        assert sites[0] == expected_site_data
    finally:
        delete_site(name=site_name)
        delete_site(name=new_site_name)
        delete_org(org_name)


def test_delete_site() -> None:
    """
    tests deleting a site
    """
    org_name = "test org for site"
    site_name = "test create site"
    try:
        org_data: Dict[str, Any] = create_and_check_org(org_name)

        create_and_check_site(site_name, org_data["id"])
    finally:
        delete_site(name=site_name)
        delete_org(org_name)
