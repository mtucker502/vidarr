def dict_helper(res, columns):
    return {name: getattr(res, name) for name in columns}
