from app import create_app


test_server = create_app(test_config="banana")

test_server.run()
