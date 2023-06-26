import os
import zipfile
import wget


class Downloader:

    """
   
    Класс, скачивающий и распаковывающий архивы в директории с указаным названием

    """

    def download(self,name,link) -> None:
        dir = os.path.join(os.getcwd(),"manga", name)
        if os.path.isdir(dir):
            print("Skipping")
            return
        os.mkdir(dir)
        filename = wget.download(link,dir)
        self.unzip(dir,filename)

    def unzip(self,dir,filename) -> None:
        with zipfile.ZipFile(filename, 'r') as zip_file:
            zip_file.extractall(dir)


