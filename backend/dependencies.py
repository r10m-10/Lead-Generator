from fastapi import Request

def get_browser(request: Request):
    return request.app.state.browser