from pathlib import Path
from typing import Optional

from docker.errors import DockerException
from docker.models.containers import Container

from deployer.dataclass.url_parser import ParsedURL
import docker


class DockerExecutors:
    def __init__(self, url: ParsedURL):
        self.client = docker.DockerClient(base_url=url.url, use_ssh_client=True)

    def build_service(self, path: Path, name: str, tag: str = 'latest'):
        image, _ = self.client.images.build(
            path=path.absolute().as_posix(),
            tag=f"{name}:{tag}",
            labels={
                'management.tool': 'deployer'
            },
        )
        print(f'Successfully built {name}:{tag} with id: {image.id}')

    def start_container(self, image: str, tag: str) -> Optional[Container]:
        running_containers = self.retrieve_running_containers(image, tag)
        container = None
        is_success: bool = True

        try:
            container = self.client.containers.run(
                f"{image}:{tag}",
                labels={
                    'deployer.app.image': image,
                    'deployer.app.tag': tag,
                },
                publish_all_ports=True,
                name=image,
                detach=True
            )
        except DockerException:
            is_success = False

        if is_success:
            self.remove_container(running_containers)
        else:
            self.restore_containers(running_containers)

        return container

    @staticmethod
    def remove_container(containers: list[Container]):
        for container in containers:
            container.remove()

    @staticmethod
    def restore_containers(containers: list[Container]):
        for container in containers:
            container.start()

    def retrieve_running_containers(self, name: str, tag: str) -> list:
        label_filter = {
            'label': [
                f"deployer.app.image={name}",
            ]
        }

        containers: list[Container] = self.client.containers.list(filters=label_filter)

        for container in containers:
            if container.image.tags[0] >= tag:
                container.stop()

        return containers

    def display_healthy_containers(self, name):
        containers: list = self.client.containers.list()
        if not name:
            containers: list[Container] = self.client.containers.list(filters={'name': name})

        for container in containers:
            health = container.attrs.get('State').get('Health', None)
            if not health:
                print(f"Container {container.name} is not checkable")
                continue

            print(f"Container {container.name} is currently {health.get('Status')}")

            if health.get('Status').lower() in ['unhealthy']:
                print(f'Container {container.id} is restarting...')
                container.restart()

