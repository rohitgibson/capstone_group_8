from asyncio import get_event_loop

from quart import Quart

from blueprints.address import address_blueprint
from blueprints.users import user_blueprint
from blueprints.demo import demo_blueprint

app = Quart(__name__)
    
app.register_blueprint(address_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(demo_blueprint)

print(app.url_map)




