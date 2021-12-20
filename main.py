import dataclasses
import functools
import logging
import uuid
import time
from typing import List

import dataclasses_json
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

emans_server = "https://wes-api-test.dedoles.net:8443/"
emans_username = "photoneo"
emans_password = "ph0T10"

# emans_server = "https://wes-api.dedoles.net:8443/"
# emans_username = "photoneo"
# emans_password = "s0MYGVo6ZJ5xFtxGDwId"
emans_endpoint = "picking-services/photoneo/photoneo-integration/matrix-picking-box-check"
# emans_endpoint = "picking-services/photoneo/photoneo-integration/matrix-picking-request"
emans_url = emans_server + emans_endpoint


@dataclasses.dataclass
class PickingBox(dataclasses_json.DataClassJsonMixin):
    pickingBoxId: str = str(uuid.uuid4())


@dataclasses.dataclass
class MatrixPickingBoxes(dataclasses_json.DataClassJsonMixin):
    pickingBoxes: List[PickingBox]
    matrixCheckRequestId: str = str(uuid.uuid4())


def _authentication() -> requests.auth.HTTPBasicAuth:
    return requests.auth.HTTPBasicAuth(emans_username, emans_password)


def log_function_execution_time(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        logger.info("{:s} function took {:.3f} ms".format(f.__qualname__, (time2 - time1) * 1000.0))

        return ret

    return wrap


@log_function_execution_time
def do_call(endpoint_url: str, authentication: requests.auth.HTTPBasicAuth = _authentication()):
    boxes = [PickingBox(pickingBoxId=str(uuid.uuid4())) for _ in range(8)]
    data = MatrixPickingBoxes(pickingBoxes=boxes)
    response = requests.post(endpoint_url, json=data.to_dict(), auth=authentication)
    if response.status_code != 200:
        raise RuntimeError(f"Error {endpoint_url} response: {str(response)}")
    return True


if __name__ == '__main__':
    for _ in range(20):
        do_call(emans_url)
