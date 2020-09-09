import requests
import pytest
from src.data_manager import DataManager
import config.config as cfg


@pytest.fixture
def data_manager():
    return DataManager(cfg)


def test_post_headers_body_json(data_manager):
    get_url = 'http://0.0.0.0:5000/test_upciti/api/v1/get_cell_towers/'
    post_url = "http://0.0.0.0:5000/test_upciti/api/v1/populate_db"

    # Additional headers.
    headers = {'Content-Type': 'application/json'}

    # Body
    mcc_arg = 270
    net_arg = 99
    area_arg = 12
    cell_arg = 22222

    get_url = get_url + "'{0}'&'{1}'&'{2}'&'{3}'".format(mcc_arg, net_arg, area_arg, cell_arg)

    resp = requests.get(get_url, headers=headers)

    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['url'] == get_url
