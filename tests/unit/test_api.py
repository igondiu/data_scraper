import os
import sys
sys.path.append(os.path.dirname(os.path.abspath("./tests")))

import requests
import pytest
from flask import Flask
from werkzeug.datastructures import FileStorage
from config import config
from src.data_manager import DataManager
from src.main import main
import config.config as cfg

app = Flask(__name__)


@pytest.fixture
def data_manager():
    return DataManager(cfg)


def test_post_headers_body_json(data_manager):
    get_url = 'http://0.0.0.0:5000/test_upciti/api/v1/get_cell_towers/'
    post_url = "http://0.0.0.0:5000/test_upciti/api/v1/populate_db"
    root_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_dir, "../test_data/data_for_tests.csv")
    print(file_path)
    # Additional headers.
    headers = {'Content-Type': 'application/json'}

    # Body
    mcc_arg = 270
    net_arg = 99
    area_arg = 12
    cell_arg = 22222

    # run main.py
    main(config, app)

    # POST Request :

    with open(file_path, 'rb') as fp:
        file = FileStorage(fp)
        resp = requests.get(post_url, file=file, headers=headers)
        assert resp.status_code == 201
        print(resp)

    # GET Request :
    get_url = get_url + "'{0}'&'{1}'&'{2}'&'{3}'".format(mcc_arg, net_arg, area_arg, cell_arg)

    resp = requests.get(get_url, headers=headers)
    assert resp.status_code == 200
