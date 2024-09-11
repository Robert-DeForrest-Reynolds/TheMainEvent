if __name__ == '__main__':
    from timeit import timeit
    print(timeit('Launcher().__init__', setup='from Self import Launcher', number=1))