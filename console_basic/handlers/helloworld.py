from console_basic.handlers import BaseHandler


class HelloWorldHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render("helloworld.html", parent_class="resourceA",
                    resource_class="Elements")
