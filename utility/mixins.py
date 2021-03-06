import functools


class KeyedEqualityMixin(object):
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.__key__() == other.__key__()

    def __ne__(self, other):
        return not self == other


@functools.total_ordering
class KeyedComparisonMixin(KeyedEqualityMixin):
    def __lt__(self, other):
        if type(self) != type(other):
            return id(self) < id(other)
        return self.__key__() < other.__key__()


class KeyedHashingMixin(KeyedEqualityMixin):
    def __hash__(self):
        return hash(self.__key__())
