#credit to Jaza on Stackoverflow
from gunicorn.app.wsgiapp import WSGIApplication

class GunicornApp(WSGIApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.app=app
        super().__init__()

    def load_config(self):
        config={key:value for key, value in self.options.items() 
                if key in self.cfg.settings and value is not None}
        for key,value in config.items():
            self.cfg.set(key.lower(),value)
