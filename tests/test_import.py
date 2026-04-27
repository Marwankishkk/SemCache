def test_import_package():
    from semcache import Cache, EmbeddingModel, Storage

    assert Cache is not None
    assert Storage is not None
    assert EmbeddingModel is not None
