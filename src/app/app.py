import logging
import socket

from quart import Quart
import uvicorn

from blueprints.address import address_blueprint
from blueprints.users import user_blueprint
from blueprints.demo import demo_blueprint

# logging.basicConfig(filename="/src/app/logs/avs.log", level=logging.DEBUG)

app = Quart(__name__)

app.register_blueprint(address_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(demo_blueprint)

print(app.url_map)

# uvicorn.run(app=app, host=socket.gethostbyname(socket.gethostname()), port=8000)




