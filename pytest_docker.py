# -*- coding: utf-8 -*-
import time
import pytest

from docker.client import Client
from docker.utils import kwargs_from_env, create_host_config


def retry(assertion_callable, retry_time=10, wait_between_tries=0.1, exception_to_retry=AssertionError):
    start = time.time()
    while True:
        try:
            return assertion_callable()
        except exception_to_retry as e:
            if time.time() - start >= retry_time:
                raise e
            time.sleep(wait_between_tries)


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
    return Client(version='auto')


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
    tag = 'latest'
    port_mappings = None
    network_mode = 'bridge'
    env = {}

    _log = None

    def __init__(self, docker_client, tag=None):
        self.docker_client = docker_client
        if tag:
            self.tag = tag

    @property
    def full_image_name(self):
        if self.repository:
            return '{}/{}:{}'.format(self.repository, self.image_name, self.tag)
        else:
            return '{}:{}'.format(self.image_name, self.tag)

    @property
    def environment(self):
        return self.env

    def pull_container(self):
        if not self.docker_client.images(self.full_image_name):
            self.docker_client.pull(self.full_image_name)

    def start(self):
        self.pull_container()
        self.build_container()

        result = self.docker_client.start(self._container)
        time.sleep(1)
        return result

    def restart(self):
        result = self.docker_client.restart(self._container)
        time.sleep(1)
        return result

    def build_container(self):
        if self.port_mappings:
            self._container = self.docker_client.create_container(
                image=self.full_image_name,
                environment=self.environment,
                ports=list(self.port_mappings.keys()),
                host_config=create_host_config(
                    port_bindings=self.port_mappings,
                    network_mode=self.network_mode
                )
            )
        else:
            self._container = self.docker_client.create_container(
                image=self.full_image_name,
                environment=self.environment,
                host_config=create_host_config(
                    network_mode=self.network_mode
                )
            )

    def stop(self):
        return self.docker_client.stop(self._container)

    def pause(self):
        return self.docker_client.pause(self._container)

    def unpause(self):
        return self.docker_client.unpause(self._container)

    def kill(self):
        return self.docker_client.kill(self._container)

    @property
    def ip(self):
        return self.docker_client.inspect_container(self._container)['NetworkSettings']['IPAddress']

    @property
    def log(self):
        if not self._log:
            self._log = DockerLog(self._container, self.docker_client)
        return self._log


class KafkaDockerContainer(AbstractDockerContainer):
    """
    Because how the kafka is setup we have to know the ip of the cluster so we
    have to use localhost
    """
    image_name = 'spotify/kafka'
    port_mappings = {9092: 9092, 2181: 2181}
    env = {
        'ADVERTISED_HOST': 'localhost',
    }


@pytest.yield_fixture(scope='session')
def kafka_container(docker_client):
    container = KafkaDockerContainer(docker_client)
    container.start()
    time.sleep(2)
    yield container
    container.kill()


class ElasticsearchDockerContainer(AbstractDockerContainer):
    """
    """

    def __init__(self, docker_client, tag='1.5'):
        self.image_name = 'elasticsearch'
        self.port_mappings = {9200: 9200}
        super().__init__(docker_client, tag)


    def build_container(self):
        self._container = self.docker_client.create_container(
            image=self.full_image_name,
            environment=self.environment,
            ports = [(9200, 'tcp')],
            command='elasticsearch -Dhttp.host=0.0.0.0'
        )


@pytest.yield_fixture
def elasticsearch_container(docker_client):
    container = ElasticsearchDockerContainer(docker_client)
    container.start()
    yield container
    container.kill()
