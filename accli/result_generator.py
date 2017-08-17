# -*-  coding:utf-8 -*-

from abc import ABCMeta


class ResultGenerator(metaclass=ABCMeta):
    @abstractmethod
    def generate(self):
        ...
