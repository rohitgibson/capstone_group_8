import logging

from quart import Quart

from blueprints.address import address_blueprint
from blueprints.users import user_blueprint
from blueprints.demo import demo_blueprint

logging.basicConfig(filename="./logs/avs.log", level=logging.DEBUG)

app = Quart(__name__)

app.register_blueprint(address_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(demo_blueprint)

print(app.url_map)




