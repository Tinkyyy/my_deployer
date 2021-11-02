import click

from deployer.dataclass.url_parser import ParsedURL
from deployer.executors.docker_commands_executors import DockerExecutors


@click.command(name='healthcheck')
@click.argument("url", type=str)
@click.argument("services", type=str, nargs=-1)
def health_check(url: str, services: str):
    docker_url = ParsedURL(url)
    executor = DockerExecutors(docker_url)

    if services:
        for service in services:
            executor.display_healthy_containers(name=service)
    else:
        executor.display_healthy_containers(name=None)
