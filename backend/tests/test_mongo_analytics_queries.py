from db import mongo_analytics_queries as q


def test_get_popular_search_queries_calls_aggregate_with_pipeline(mocker):
    fake_rows = [{"_id": "mat", "count": 3, "last_seen_at": "x"}]

    agg_mock = mocker.Mock(return_value=fake_rows)
    mocker.patch.object(q, "search_log_collection", mocker.Mock(aggregate=agg_mock))

    out = q.get_popular_search_queries(limit=5, min_results=1, search_type=None)

    assert out == fake_rows
    assert agg_mock.call_count == 1

    pipeline = agg_mock.call_args[0][0]
    assert isinstance(pipeline, list)

    assert any("$match" in stage for stage in pipeline)
    assert any("$project" in stage for stage in pipeline)
    assert any("$group" in stage for stage in pipeline)

    project_stage = next(stage["$project"] for stage in pipeline if "$project" in stage)
    assert "query" in project_stage
    assert "$toLower" in project_stage["query"]


def test_get_recent_genre_searches_uses_aggregate(mocker):
    fake_rows = [{"timestamp": "x", "genre_id": 1, "results_count": 10}]

    agg_mock = mocker.Mock(return_value=fake_rows)
    mocker.patch.object(q, "search_log_collection", mocker.Mock(aggregate=agg_mock))

    out = q.get_recent_genre_searches(limit=3)

    assert out == fake_rows
    assert agg_mock.call_count == 1
