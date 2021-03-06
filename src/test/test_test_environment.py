import unittest

import docker

from src.test import utils


class DockerTestEnvironmentTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(f"SetUp {cls.__name__}")
        cls.test_environment = utils.ExaslctTestEnvironment(cls, "./start-test-env",
                                                            clean_images_at_close=False)
        # TODO cls.test_environment.clean_images()
        cls.docker_environment_name = cls.__name__
        cls.on_host_docker_environment, cls.google_cloud_docker_environment = \
            cls.test_environment.spawn_docker_test_environment(cls.docker_environment_name)

    def setUp(self):
        self.client = docker.from_env()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.on_host_docker_environment.close()
        except Exception as e:
            print(e)
        try:
            cls.test_environment.close()
        except Exception as e:
            print(e)

    def tearDown(self):
        self.client.close()

    def test_all_containers_started(self):
        containers = [c.name for c in self.client.containers.list() if self.docker_environment_name in c.name]
        self.assertEqual(len(containers), 2, f"Not exactly 2 containers in {containers}")
        db_container = [c for c in containers if "db_container" in c]
        self.assertEqual(len(db_container), 1, f"Found no db container in {containers}")
        test_container = [c for c in containers if "test_container" in c]
        self.assertEqual(len(test_container), 1, f"Found no test container in {containers}")

    def test_docker_available_in_test_container(self):
        containers = [c.name for c in self.client.containers.list() if self.docker_environment_name in c.name]
        test_container = [c for c in containers if "test_container" in c]
        exit_result = self.client.containers.get(test_container[0]).exec_run("docker ps")
        exit_code = exit_result[0]
        output = exit_result[1]
        self.assertEqual(exit_code, 0, f"Error while executing 'docker ps' in test container got output\n {output}")


if __name__ == '__main__':
    unittest.main()
