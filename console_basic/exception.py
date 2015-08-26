from oslo_config import cfg
from oslo_log import log
from oslo_utils import encodeutils


CONF = cfg.CONF
LOG = log.getLogger(__name__)

class Error(Exception):

    message_format = None

    def __init__(self, message=None, **kwargs):
        try:
            message = self._build_message(message, **kwargs)
        except KeyError:
            LOG.warning('missing exception kwargs (programmer error)')
            message = self.message_format

        super(Error, self).__init__(message)

    def _build_message(self, message, **kwargs):
        """Builds and returns an exception message.

        :raises: KeyError given insufficient kwargs

        """
        if not message:
            try:
                message = self.message_format % kwargs
            except UnicodeDecodeError:
                try:
                    kwargs = {k: encodeutils.safe_decode(v)
                              for k, v in kwargs.items()}
                except UnicodeDecodeError:
                    message = self.message_format
                else:
                    message = self.message_format % kwargs

        return message



class HTTPCodeError(Error):
    message_format = "HTTP Code is %(code)d."


class HTTPContentError(Error):
    message_format = "There is error in HTTP content, %(error)s."
