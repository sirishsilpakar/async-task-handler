import contextvars
import types

request_global = contextvars.ContextVar(
    "request_global", default=types.SimpleNamespace()
)


def g():
    """Responsible for setting request-response cycle variables"""
    return request_global.get()
