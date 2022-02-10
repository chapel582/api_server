from typing import Any, Dict

import illu_db

illu_db.init_db()


def test_create_org():
    name: str = "test org"
    result: Dict[str, Any] = illu_db.create_org(name)

    assert result["name"] == name
