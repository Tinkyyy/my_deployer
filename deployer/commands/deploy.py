from pathlib import Path

import click

from deployer.dataclass.url_parser import ParsedURL
from deployer.executors.docker_commands_executors import DockerExecutors


@click.command('deploy')
@click.argument("url", type=str)
@click.argument("services", type=str, nargs=-1)
@click.option(
    "--tag",
    type=str,
    required=False,
    show_default=True,
    default='latest',
)
def deploy(url: str, services: str, tag: str = 'latest'):
    docker_url = ParsedURL(url)
    executor = DockerExecutors(docker_url)

    for service in services:
        path = Path(service).absolute()
        executor.start_container(image=path.name, tag=tag)
