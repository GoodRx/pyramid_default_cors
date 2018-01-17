# pyramid_default_cors

Set up default handling of CORS XHR in Pyramid.

## Setting up local dev environment


```bash
virtualenv .venv
source .venv/bin/activate
pip install -r tasks/requirements.txt
```

## Example

1. Make sure you have followed steps to set up local environment first

1. Starting from your workspace directory (``~/projects/tutorial``), create a directory for this step:

    ```bash
    cd ~/projects/tutorial; mkdir default_cors_example; cd default_cors_example
    ```

1. Copy the following into ``~/your_projects/tutorial/app.py``:

    ```python
    from waitress import serve
    from pyramid.config import Configurator
    from pyramid.response import Response
    import pyramid_default_cors

    def hello_world(request):
        print('Incoming request')
        return Response('<body><h1>Hello World!</h1></body>')

    if __name__ == '__main__':
        with Configurator() as config:
            # This should be included before any other route definitions
            config.include('pyramid_default_cors')
            config.add_route('hello', '/')
            config.add_view(hello_world, route_name='hello')
            app = config.make_wsgi_app()
        serve(app, host='0.0.0.0', port=6543)
    ```

1. Run the application

  ```bash
  # You can run this app using the local dev environment outlined above
  python app.py
  ```

Your App should now be ready to handle CORS preflight requests via OPTIONS verb

```bash
curl -H "Origin: http://foobar.xyz"  \
     -H "Access-Control-Request-Method: POST"  \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS --verbose http://localhost:6543/
> OPTIONS / HTTP/1.1
> Host: localhost:6543
> User-Agent: curl/7.54.0
> Accept: */*
> Origin: http://foobar.xyz
> Access-Control-Request-Method: POST
> Access-Control-Request-Headers: X-Requested-With
>
< HTTP/1.1 200 OK
< Access-Control-Allow-Headers: Accept, Content-Type, X-Requested-With
< Access-Control-Allow-Methods: PUT, DELETE, POST
< Access-Control-Allow-Origin: http://foobar.xyz
< Access-Control-Max-Age: 3600
< Content-Length: 0
< Content-Type: text/html; charset=UTF-8
< Date: Wed, 17 Jan 2018 23:49:16 GMT
< Server: waitress
<
```
## Testing

To run tests, simply run ``tox``
```bash
source .venv/bin/activate
tox
```

## Releases

Install [pandoc]

[pandoc]: http://johnmacfarlane.net/pandoc/
