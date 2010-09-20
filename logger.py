import logging

logger = logging.getLogger("PlanetBusterLogger")
logger.setLevel(logging.DEBUG)

class NullHandler(logging.Handler):
    """Logs everything to /dev/null"""
    def emit(self, record):
        pass

def configure_logger():
    try:
       import redis
       class RedisHandler(logging.Handler):
           """Logs messages to a Redis Server."""
           def __init__(self):
               logging.Handler.__init__(self)
               self.r = redis.Redis()
               pbl = "planet-buster-logger"
               self.key = "%s-%d" % (pbl, self.r.incr(pbl))
               self.emit("Initialized the logger") 

           def emit(self, record):
               self.r.rpush(self.key, record)

       logger.addHandler(RedisHandler())
    except ImportError:
       logger.addHandler(NullHandler())
