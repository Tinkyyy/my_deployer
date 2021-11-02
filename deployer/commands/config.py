import click

from deployer.dataclass.url_parser import ParsedURL
from deployer.executors.ssh_commands_executors import SSHExecutors


@click.command('config')
@click.argument('url', type=str)
def config(url: str):
    ssh_url = ParsedURL(url)
    executor = SSHExecutors(ssh_url)

    if not executor.is_docker_installed():
        executor.install_docker()
    else:
        if not executor.is_docker_up_to_date():
            executor.uninstall_docker()
            executor.install_docker()
