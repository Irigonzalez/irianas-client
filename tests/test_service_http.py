import os
import pytest
from irianas_client.services.webserver.apache import HTTPDService

obj_httpd = HTTPDService()
tmp_path_config_file = '/tmp/httpd.conf'
tmp_path_sysconfig_file = '/tmp/httpd'


class TestHttpService(object):

    def test_get_params(self):
        assert obj_httpd.keep_alive == 'Off'
        assert obj_httpd.get('keep_alive') == 'Off'

    def test_set_params(self):
        obj_httpd.keep_alive = 'On'
        assert obj_httpd.keep_alive == 'On'
        obj_httpd.set('keep_alive', 'Off')
        assert obj_httpd.keep_alive == 'Off'

    def test_save_config_file(self):
        obj_httpd.save_attr(tmp_path_config_file)
        assert open(tmp_path_config_file)

    def test_save_sysconfig_file(self):
        obj_httpd.worker(tmp_path_sysconfig_file)
        assert open(tmp_path_sysconfig_file)

    def test_create_vhost_file(self):
        assert obj_httpd.create_vhost('example.com', '/tmp', True)
        assert open('/tmp/example.com.conf')

    def test_remove_vhost_file(self):
        obj_httpd.remove_vhost('example.com', '/tmp', True)
        assert not os.path.exists(os.path.join('/tmp',
                                               'example.com' + '.conf'))

    @pytest.mark.skipif("'VIRTUAL_ENV' in os.environ",
                        reason="requires root permission")
    @pytest.mark.skipif("'TRAVIS' in os.environ",
                        reason="requires root permission")
    def test_install(self):
        assert obj_httpd.install()

    @pytest.mark.skipif("'VIRTUAL_ENV' in os.environ",
                        reason="requires root permission")
    @pytest.mark.skipif("'TRAVIS' in os.environ",
                        reason="requires root permission")
    def test_uninstall(self):
        assert obj_httpd.remove()
