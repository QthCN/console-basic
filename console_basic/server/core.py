import os

from oslo_config import cfg
import pbr.version
import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver

from console_basic import config
from console_basic.handlers.helloworld import HelloWorldHandler


CONF = cfg.CONF


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", HelloWorldHandler)
        ]
        settings = dict(
            blog_title="console",
            template_path=os.path.join(os.path.dirname(__file__),
                                       "..",
                                       "templates"),
            static_path=os.path.join(os.path.dirname(__file__),
                                     "..",
                                     "static"),
            debug=True,
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login.html",
        )
        super(Application, self).__init__(handlers, **settings)


def run(possible_topdir, conf_dir="etc", conf_file="console-basic.conf"):
    dev_conf = os.path.join(possible_topdir,
                            conf_dir,
                            conf_file)
    config_files = None
    if os.path.exists(dev_conf):
        config_files = [dev_conf]

    config.configure(
        version=pbr.version.VersionInfo("console_basic").version_string(),
        config_files=config_files,
    )

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(CONF.server.port)
    tornado.ioloop.IOLoop.current().start()
