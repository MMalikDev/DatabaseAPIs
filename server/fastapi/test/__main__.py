import sys
from pathlib import Path

path = str(Path.cwd())
sys.path.append(path)

from test.custom.albums import album_tests
from test.custom.artists import artist_tests
from test.custom.books import book_tests
from test.custom.items import item_tests
from test.custom.songs import song_tests


def main():
    item_tests.run()
    song_tests.run()
    album_tests.run()
    artist_tests.run()

    book_tests.run()


if __name__ == "__main__":
    main()
