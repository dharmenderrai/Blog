import dataclasses
from dataclasses import dataclass
from collections.abc import Set, Hashable

C = dataclasses.make_dataclass('VendingMachine', [('water', int),
                                                  ('chips', int),
                                                  ('z', int)
                                                  ], order = True)

class CustomSet(Set, Hashable):
    __hash__ = Set._hash

    wrapped_methods = ('difference', 'intersection', 'union')

    def __repr__(self):
        return "CustomSet({0})".format(list(self._set))

    def __new__(cls, iterable=None):
        selfobj = super(CustomSet, cls).__new__(CustomSet)
        selfobj._set = frozenset() if iterable is None else frozenset(iterable)
        for method_name in cls.wrapped_methods:
            setattr(selfobj, method_name, cls._wrap_method(method_name, selfobj))
        return selfobj

    @classmethod
    def _wrap_method(cls, method_name, obj):
        def method(*args, **kwargs):
            result = getattr(obj._set, method_name)(*args, **kwargs)
            return CustomSet(result)
        return method

    def __getattr__(self, attr):
        return getattr(self._set, attr)

    def __contains__(self, item):
        return item in self._set

    def __len__(self):
        return len(self._set)

    def __iter__(self):
        return iter(self._set)