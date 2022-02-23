# TL21-55

This is a semester project for the course _Software Engineering_ at the National Technical University of Athens (NTUA).

It was implemented during the winter semester of the academic year 2021-2022.

You can find out how to install it [here](https://github.com/ntua/TL21-55/blob/master/doc/setup_guide.md).

## Implementation

The project was implemented in Python. We used:
* [Django](https://www.djangoproject.com/) (for the backend)
* [Django REST framework](https://www.django-rest-framework.org/) (for the REST API)
* [django-rest-framework-jwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) (for the authentication)
* [Bootstrap](https://getbootstrap.com) (for the frontend)

## Testing

Testing is implemented using python's [unittest](https://docs.python.org/3/library/unittest.html) module 
and [django's testing framework](https://docs.djangoproject.com/en/4.0/topics/testing/) (which builds upon unittest)

Before running the tests make sure the 'tolls_root'@'localhost' has permissions to create a DB so the test_db can be created. This can be done by executing the following command inside mysql:

```
GRANT ALL PRIVILEGES ON * . * TO 'tolls_root'@'localhost';
```

In order to run the tests execute the following command from the source directory:

```
python manage.py test
```
