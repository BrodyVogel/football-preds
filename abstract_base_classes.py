from abc import ABC, abstractmethod

class Bet(ABC):

    def __init__(self):
        self.description = 'Instantiation of "Bet" Abstract Base Class'

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def get_schedule(self):
        pass

    @abstractmethod
    def get_historical_stats(self):
        pass

    @abstractmethod
    def get_historical_results(self):
        pass