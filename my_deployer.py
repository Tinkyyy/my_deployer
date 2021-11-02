import click

from deployer.commands.build import build
from deployer.commands.config import config
from deployer.commands.deploy import deploy
from deployer.commands.healthcheck import health_check


@click.group()
def deployer():
    """Deployer group instance"""


# noinspection PyTypeChecker
def init():
    """Execute the command using the CLI flags."""
    deployer.add_command(config)
    deployer.add_command(build)
    deployer.add_command(deploy)
    deployer.add_command(health_check)

    deployer()


if __name__ == '__main__':
    init()
