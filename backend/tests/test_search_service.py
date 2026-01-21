from backend.services.search_service import search_all


def test_search_all_combines_title_and_actor_results(mocker):
    mocker.patch("backend.services.search_service.count_titles_by_keyword", return_value=2)
    mocker.patch(
        "backend.services.search_service.search_titles_by_keyword",
        return_value=[
            {"film_id": 10, "title": "Matrix", "description": None, "poster_path": None, "backdrop_path": None},
            {"film_id": 11, "title": "Matrix Reloaded", "description": None, "poster_path": None, "backdrop_path": None},
        ],
    )

    mocker.patch("backend.services.search_service.count_people_by_name", return_value=1)
    mocker.patch(
        "backend.services.search_service.search_people_by_name",
        return_value=[{"person_id": 99, "name": "Keanu Reeves", "profile_path": None}],
    )

    mocker.patch(
        "backend.services.search_service.get_titles_for_person",
        return_value=[{"film_id": 10, "title": "Matrix", "description": None, "poster_path": None, "backdrop_path": None}],
    )

    mocker.patch("backend.services.search_service.map_title_rows", side_effect=lambda x: x)

    res = search_all(query="  MAT  ", limit_per_section=20, title_offset=0)

    assert res.query == "MAT" 
    assert res.by_title.count == 2
    assert len(res.by_title.items) == 2

    assert res.by_actor.count == 1
    assert len(res.by_actor.items) == 1
    assert res.by_actor.items[0].actor_id == 99
    assert res.by_actor.items[0].full_name == "Keanu Reeves"
    assert len(res.by_actor.items[0].films) == 1
