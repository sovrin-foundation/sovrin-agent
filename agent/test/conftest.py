from agent.api.apiServer import newApi

# noinspection PyUnresolvedReferences
from sovrin.test.conftest import *

# noinspection PyUnresolvedReferences
from sovrin.test.agent.conftest import *


@pytest.fixture(scope='function')
def api(looper):
    return newApi(looper.loop)
