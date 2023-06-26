import os
import pymongo
from parser import Parser

parser = Parser('https://xxxxx.hentaichan.live/manga/new')

maxOffset = parser.get_max_offset()
for offset in range(0, maxOffset+20, 20):
    print(f"Offset {offset} from {maxOffset}")
    if not os.path.exists(os.path.join(os.getcwd(), "manga")):
        os.mkdir("manga")
    parser.parse_page(parser.startLink+"?offset="+str(offset))
