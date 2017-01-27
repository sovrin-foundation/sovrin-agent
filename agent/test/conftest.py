from agent.api.apiServer import newApi

# noinspection PyUnresolvedReferences
from sovrin_client.test.conftest import *

# noinspection PyUnresolvedReferences
from sovrin_client.test.agent.conftest import *


@pytest.fixture(scope='function')
def api(looper):
    return newApi(looper.loop)
