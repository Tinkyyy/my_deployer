import paramiko

from deployer.dataclass.url_parser import ParsedURL


class SSHExecutors:
    def __init__(self, credentials: ParsedURL):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            hostname=credentials.hostname,
            port=credentials.port,
            username=credentials.username,
            password=credentials.password
        )

    def send_command(self, command: str) -> (bool, (str, str)):
        _, stdout, stderr = self.client.exec_command(f"{command}", get_pty=True)
        status = stdout.channel.recv_exit_status()

        if status != 0:
            return False, (stdout.read().decode(), stderr.read().decode())

        return True, (stdout.read().decode(), stderr.read().decode())

    def install_docker(self) -> bool:
        """Install docker using SSH"""
        print('Docker is installing...')
        for command in INSTALL_DOCKER:
            status, [stdout, _] = self.send_command(command)
            for line in stdout:
                print(f"{line}", end="")

        return True

    def uninstall_docker(self) -> bool:
        """Uninstall docker using SSH"""
        status: bool = True

        print('Docker is uninstalling...')
        for command in UNINSTALL_DOCKER:
            status, [stdout, _] = self.send_command(command)
            for line in stdout:
                print(f"{line}", end="")

        if status is False:
            return False

        return True

    def is_docker_up_to_date(self, version: str = "19.03.15") -> bool:
        """Check if the docker version is the same as the one passed in parameter"""
        _, (stdout, _) = self.send_command('docker -v')
        up_to_date = version in stdout

        return up_to_date

    def is_docker_installed(self) -> bool:
        """Check if docker is installed by reading the stderr"""
        status, (_, _) = self.send_command('docker -v')
        return status


INSTALL_DOCKER = [
    'sudo apt update',
    'sudo apt install -y curl',
    'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -',
    'sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"',
    'sudo apt install -y docker-ce=5:19.03.15~3-0~ubuntu-focal docker-ce-cli=5:19.03.15~3-0~ubuntu-focal',
    'sudo usermod -aG docker $USER'
]

UNINSTALL_DOCKER = [
    'sudo apt-get purge -y docker-engine docker docker.io docker-ce docker-ce-cli',
    'sudo apt-get autoremove -y --purge docker-engine docker docker.io docker-ce',
    'sudo rm -rf /var/lib/docker /etc/docker',
    'sudo rm /etc/apparmor.d/docker',
    'sudo groupdel docker',
    'sudo rm -rf /var/run/docker.sock'
]
