# -*- coding: utf-8 -*-


def test_bar_fixture(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_sth(bar):
            assert bar == "europython2015"
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--foo=europython2015',
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'docker:',
        '*--foo=DEST_FOO*Set the value for the fixture "bar".',
    ])


def test_hello_ini_setting(testdir):
    testdir.makeini("""
        [pytest]
        HELLO = world
    """)

    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def hello(request):
            return request.config.getini('HELLO')

        def test_hello_world(hello):
            assert hello == 'world'
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_hello_world PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_docker_fixture(testdir):
    testdir.makepyfile("""
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
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_redis_container_start PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_kafka_docker_fixture(kafka_container):
    assert kafka_container


def test_elasticsearch_docker_fixture(elasticsearch_container):
    import ipdb; ipdb.set_trace()
