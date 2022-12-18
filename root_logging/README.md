# Logging middleware for Django

<hr/>

### pre-requirements:

    Python Version >= 3.5
    Django Version >= 2.0

<hr/>

# Simple Output Example

    2022-07-17 01:43:27,573 :: main:27 :: CRITICAL :: division by zero
    Traceback (most recent call last):
      File "/home/alex/home/Django/web/test/venv/lib/python3.9/site-packages/django/core/handlers/base.py", line 197, in _get_response
        response = wrapped_callback(request, *callback_args, **callback_kwargs)
      File "/home/alex/home/Django/web/test/venv/lib/python3.9/site-packages/django/views/generic/base.py", line 84, in view
        return self.dispatch(request, *args, **kwargs)
      File "/home/alex/home/Django/web/test/venv/lib/python3.9/site-packages/django/views/generic/base.py", line 119, in dispatch
        return handler(request, *args, **kwargs)
      File "/home/alex/home/Django/web/test/project/main_app/views.py", line 20, in get
        1 / 0
    ZeroDivisionError: division by zero
    2022-07-17 01:43:27,613 :: main:23 :: DEBUG :: Response from `main_app:index_view`. Request: `POST`. Response Code: `200`
    