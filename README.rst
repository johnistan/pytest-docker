pytest-docker
===================================

Plugin to help launch docker containers

----

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.


Features
--------

* TODO


Requirements
------------

* docker-py

Example
-----------

.. code-block:: python

        import pytest
        from pytest_docker import AbstractDockerContainer

        class RedisDockerContainer(AbstractDockerContainer):
            image_name = 'redis'

        @pytest.yield_fixture
        def redis_container(docker_client):
            container = RedisDockerContainer(docker_client)
            container.start()
            yield container
            container.kill()

        def test_redis_container_start(redis_container):
            assert '6379' in redis_container.log


Installation
------------

You can install "pytest-docker" via conda

    $ conda install pytest-docker


Usage
-----

* TODO

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `BSD-3`_ license, "pytest-docker" is free and open source software
