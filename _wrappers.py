def login_required(f):
    def wrapper(*args, **kwargs):
        api = args[0]
        if not api.logged_in:
            raise Exception(f"You must be logged in to access this resource: {f.__name__}")
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    def wrapper(*args, **kwargs):
        api = args[0]
        if not api.logged_in:
            raise Exception(f"You must be logged in to access this resource: {f.__name__}")
        elif not api.logininfo.is_admin:
            raise Exception(f"You must be an admin to access this resource")
        return f(*args, **kwargs)
    return wrapper

if __name__ == "__main__":
    pass