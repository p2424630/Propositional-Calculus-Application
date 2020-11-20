# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from dataclasses import dataclass
from abc import ABC, abstractmethod


@abstractmethod
@dataclass(frozen=True)
class Proposition(object, ABC):

    def idempotence(self):
        return False
