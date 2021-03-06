from ...lib.base.info import Info
from ...lib.data.container_info import ContainerInfo
from ...lib.data.database_info import DatabaseInfo
from ...lib.data.docker_network_info import DockerNetworkInfo


class EnvironmentInfo(Info):

    def __init__(self,
                 name: str, env_type: str,
                 database_info: DatabaseInfo,
                 test_container_info: ContainerInfo,
                 network_info: DockerNetworkInfo):
        self.name = name
        self.type = env_type
        self.test_container_info = test_container_info
        self.database_info = database_info
        self.network_info = network_info
