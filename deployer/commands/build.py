from pathlib import Path

import click

from deployer.dataclass.url_parser import ParsedURL
from deployer.executors.docker_commands_executors import DockerExecutors


@click.command(name='build')
@click.argument('url', type=str)
@click.argument("services", type=str, nargs=-1)
@click.option(
    "--tag",
    type=str,
    required=False,
    default='latest',
    show_default=True,
)
def build(url: str, services: str, tag: str = 'latest'):
    docker_url = ParsedURL(url)
    executor = DockerExecutors(docker_url)
    for service in services:
        path = Path(service)
        name = path.absolute().name
        executor.build_service(path, name, tag)
