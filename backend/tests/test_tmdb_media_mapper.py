from backend.services import tmdb_media_mapper as m


def test_build_image_url_none_returns_none():
    assert m.build_image_url(None, m.TMDB_POSTER_SIZE) is None


def test_build_image_url_builds_full_url():
    url = m.build_image_url("/abc.jpg", m.TMDB_POSTER_SIZE)
    assert url is not None
    assert url.startswith(m.TMDB_IMAGE_BASE)
    assert url.endswith("/abc.jpg")


def test_build_profile_url_uses_w185():
    url = m.build_profile_url("/p.png")
    assert url is not None
    assert "/w185" in url
    assert url.endswith("/p.png")


def test_map_title_row_adds_urls_and_removes_paths():
    row = {
        "film_id": 1,
        "title": "Matrix",
        "poster_path": "/poster.jpg",
        "backdrop_path": "/backdrop.jpg",
    }

    out = m.map_title_row(row)

    assert "poster_path" not in out
    assert "backdrop_path" not in out

    assert out["poster_url"] is not None and out["poster_url"].endswith("/poster.jpg")
    assert out["backdrop_url"] is not None and out["backdrop_url"].endswith("/backdrop.jpg")


def test_map_title_row_handles_missing_paths():
    row = {"film_id": 2, "title": "No Media"}
    out = m.map_title_row(row)

    assert out["poster_url"] is None
    assert out["backdrop_url"] is None


def test_map_title_rows_maps_list_length_preserved():
    rows = [
        {"film_id": 1, "title": "A", "poster_path": "/a.jpg"},
        {"film_id": 2, "title": "B", "poster_path": None, "backdrop_path": "/b.jpg"},
    ]
    out = m.map_title_rows(rows)
    assert isinstance(out, list)
    assert len(out) == 2
    assert out[0]["film_id"] == 1
    assert out[1]["film_id"] == 2
