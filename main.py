import os

from parser import Parser
from db.manga_db import Client


if __name__ == '__main__':

    parser = Parser('https://xxxxx.hentaichan.live/manga/new')

    maxOffset = parser.get_max_offset()
    for offset in range(0, maxOffset+20, 20):
        print(f"Offset {offset} from {maxOffset}")
        if not os.path.exists(os.path.join(os.getcwd(), "manga")):
            os.mkdir("manga")
        parser.parse_page(parser.startLink+"?offset="+str(offset))
