
from src.modules import *


class Robot(object):
    _instance = None

    @staticmethod
    def instance():
        if Robot._instance is None:
            Robot._instance = Robot()
        return Robot._instance

    @staticmethod
    def release():
        Robot._instance = None

    # def ATR_strategy(self):

