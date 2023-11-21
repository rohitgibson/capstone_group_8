from asyncio import get_event_loop

from quart import Quart

from blueprints.address import address_blueprint
from blueprints.users import user_blueprint
from blueprints.demo import demo_blueprint

app = Quart(__name__)
    
app.register_blueprint(address_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(demo_blueprint)

if __name__ == "__main__":
    print(app.url_map)
    app.run(host="127.0.0.1", port=5005, debug=False)




