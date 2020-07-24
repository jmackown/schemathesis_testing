
from hypothesis import settings

import schemathesis
import os

abs_file_path = os.path.abspath(os.path.dirname(__file__))
openapi_path = os.path.join(abs_file_path, "../", "static/schema.json")
schema = schemathesis.from_path(openapi_path, base_url="http://localhost:57244")


@schema.parametrize()
@settings(max_examples=20)
def test_no_server_errors_uri(case, test_server):
    
    response = case.call()

    assert response.status_code in [200, 201, 400]
