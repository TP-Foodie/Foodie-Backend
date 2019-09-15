def assert_attr_exists(obj, attr_name):
    try:
        getattr(obj, attr_name)
        assert True
    except KeyError:
        assert False
