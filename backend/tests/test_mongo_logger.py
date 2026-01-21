from backend.services.mongo_logger import _normalize_parameters


def test_normalize_parameters_lowercases_query_and_full_name():
    p = {"query": "  MAT  ", "full_name": "  KeAnU ReEveS  ", "offset": 10}
    out = _normalize_parameters("all", p)

    assert out["query"] == "mat"
    assert out["full_name"] == "keanu reeves"
    assert out["offset"] == 10


def test_normalize_parameters_keeps_non_string_values():
    p = {"query": 123, "full_name": None}
    out = _normalize_parameters("all", p)

    assert out["query"] == 123
    assert out["full_name"] is None


def test_normalize_parameters_handles_none_dict():
    out = _normalize_parameters("all", None)
    assert out == {}
