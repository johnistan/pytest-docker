# -*- coding: utf-8 -*-
import time
import pytest

from docker.client import Client
from docker.utils import kwargs_from_env, create_host_config


def pytest_addoption(parser):
    group = parser.getgroup('docker')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default=2015,
        help='Set the value for the fixture "bar".'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo


@pytest.fixture(scope='session')
def docker_client():
    # MAC OSX SUPPORT
    # if platform.system() == 'Darwin':
        # kwargs = kwargs_from_env(assert_hostname=False)
        # return Client(**kwargs)
    # else:
    return Client()


class DockerLog:
    def __init__(self, container, client):
        self.container = container
        self.client = client

    def __contains__(self, t):
        return t in self.logs 

    @property
    def logs(self):
        return self.client.logs(self.container).decode()

    def __str__(self):
        return self.logs

    def __repr__(self):
        return self.logs


class AbstractDockerContainer(object):
    repository = None
    image_name = None
    _log = None

    def __init__(self, docker_client, tag='latest'):
        self.docker_client = docker_client
        self.tag = tag

    @property
    def full_image_name(self):
        if self.repository:
            return '{}/{}:{}'.format(self.repository, self.image_name, self.tag)
        else:
            return '{}:{}'.format(self.image_name, self.tag)

    @property
    def environment(self):
        _environment = {
        }
        return _environment

    def pull_container(self):
        if not self.docker_client.images(self.full_image_name):
            self.docker_client.pull(self.full_image_name)

    def start(self):
        self.pull_container()

        self._container = self.docker_client.create_container(
            image = self.full_image_name,
            environment = self.environment
        )
        result = self.docker_client.start(self._container)
        time.sleep(1)
        return result 

    def stop(self):
        return self.docker_client.stop(self._container)

    def pause(self):
        return self.docker_client.pause(self._container)

    def unpause(self):
        return self.docker_client.unpause(self._container)

    def kill(self):
        return self.docker_client.kill(self._container)

    @property
    def log(self):
        if not self._log:
            self._log = DockerLog(self._container, self.docker_client)
        return self._log
