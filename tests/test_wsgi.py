import schemathesis
from hypothesis import settings

from test_server import test_server

schema = schemathesis.from_wsgi("/static/schema.json", test_server)


@schema.parametrize()
# @settings(max_examples=5)
def test_no_server_errors(case):
    response = case.call_wsgi()
    print(f"case.body: {case.body}")
    print(f"response.status_code: {response.status_code}")
    print(f"response: {response}")
    if response.status_code == 400:
        pass
        # assert response.text == "blah"
    else:
        assert response.status_code in [200, 201]
