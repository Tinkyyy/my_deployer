__author__ = "belgue_s"
__doc__ = "This service can retrieve information about the Docker containers on the host"

import docker
import flask
from docker import DockerClient
from flask import Flask, request, jsonify

docker_client: DockerClient = docker.DockerClient(base_url='unix://var/run/docker.sock')


def id_or_name(x, identifier):
    if x['Id'] == identifier or x['Names'][0] == '/' + identifier:
        return True
    return False


def get_container_data(identifier) -> dict:
    container_info: dict = {}
    for container in docker_client.containers.list():
        if container.id == identifier or container.name == identifier:
            api = container.client.api.containers()
            api = list(filter(lambda x: id_or_name(x, identifier), api))[0]

            container_info['name'] = container.name
            container_info['short_hash'] = container.short_id
            container_info['image'] = container.image.tags[0]
            container_info['uptime'] = api["Status"]
            container_info['published_ports'] = container.ports
            container_info['volumes'] = api["Mounts"]

            return container_info
    return {"message": "Container not found"}


def get_all_containers() -> list:
    containers: list = list()
    for container in docker_client.containers.list():
        containers.append(get_container_data(container.id))

    return containers


def get_all_running_containers() -> list:
    containers: list = list()
    for container in docker_client.containers.list():
        if container.attrs["State"]["Running"] is True:
            containers.append(get_container_data(container.id))

    return containers


def build_app() -> flask.app.Flask:
    """This function will return a Flask APP instance"""
    application = Flask("checker")
    application.debug = False

    return application


app: Flask = build_app()


@app.route('/containers/', methods=['GET'])
def route_get_all_containers():
    running_container = request.args.get('all', type=str, default='0')

    if running_container == '0':
        return jsonify(get_all_containers()), 200

    return jsonify(get_all_running_containers()), 200


@app.route('/containers/<id>', methods=['GET'])
def route_get_container_by_id(id):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    for container in client.containers.list():
        if container.id == id or container.name == id:
            container_info = get_container_data(id)

            return jsonify(container_info), 200
    return {"message": f"Container with id {id} doesn't exist"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
