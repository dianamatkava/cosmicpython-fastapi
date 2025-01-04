from collections.abc import Iterable, Sequence


class MyIteratorWithNext:
    def __init__(self, iterable):
        self.index = 0
        self.iterable = iterable

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.iterable):
            raise StopIteration()
        value = self.iterable[self.index]
        self.index += 1
        return value


class MyIterable:
    def __init__(self, *data):
        self.data = data

    def __iter__(self):
        return iter(self.data)


class MySequence(Sequence):
    def __init__(self, *data):
        if not isinstance(data, Iterable):
            raise TypeError("Provided data is not iterable")
        self.data = tuple(data)

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)


class ValidIterable(MyIterable, Iterable):
    pass


class WrongIterable(Iterable):
    def __init__(self, *data):
        self.iterable = data

    def __iter__(self):
        pass


def validate_iterator(iterable, iterator_class):
    iterator = iterator_class(iterable)
    try:
        for _ in iterator:
            pass
        print(f"{iterator_class.__name__} is a valid iterator.")
    except Exception as e:
        print(f"{iterator_class.__name__} failed as an iterator: {e}")


def validate_iterable(iterable_class):
    try:
        iterable = iterable_class(1, 2, 3)
        try:
            iterator = iter(iterable)
            list(iterator)  # Exhaust iterator to test
            print(f"{iterable_class.__name__} is a valid iterable.")
        except StopIteration:
            print(f"{iterable_class.__name__} satisfies Iterable but is a valid iterable.")
    except TypeError as e:
        missing_methods = Iterable.__abstractmethods__ - set(dir(iterable_class))
        print(f"{iterable_class.__name__} is not a valid Iterable: {missing_methods or e}")


if __name__ == "__main__":
    validate_iterable(ValidIterable)
    validate_iterable(WrongIterable)
    validate_iterator([1, 2, 3], MyIteratorWithNext)
    validate_iterator(MySequence(ValidIterable(1, 2, 3)), MyIteratorWithNext)
