from zipfile import ZipFile
import os
import requests
import time
from tqdm import tqdm


class Downloader:

    def __init__(self):
        self.data_zip_url = "http://web.stanford.edu/class/cs276/pa/pa1-data.zip"
        self.save_folder = "data/"
        self.data_zip_name = self.save_folder + "cs276.zip"
        self.setup_folder = self.save_folder + "cs276"

    def setup(self):
        if os.path.exists(self.setup_folder):
            print("data set cs276 is already setup")
        elif os.path.exists(self.data_zip_name):
            if self.__unzip_data():
                print("the data setup is done")
        else:
            if self.__download_data_zip():
                if self.__unzip_data():
                    print("the data setup is done")

    def __download_data_zip(self):
        try:
            pbar = tqdm(desc="downloading the cs276 data", total=94144554)
            with requests.get(self.data_zip_url, stream=True) as r:
                r.raise_for_status()
                with open("data/cs276.zip", 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            return True
        except Exception as e:
            print(f"Could not download the data set: {e}")
            return False

    def __unzip_data(self):
        try:
            with ZipFile(self.data_zip_name, "r") as zip_file:
                for file in tqdm(desc="extracting cs276 data", iterable=zip_file.namelist(), total=len(zip_file.namelist())):
                    zip_file.extract(member=file, path=self.save_folder)
                print("extraction finished")
            os.rename(self.save_folder + "pa1-data", self.setup_folder)
            os.remove(self.data_zip_name)
            return True
        except Exception as e:
            print(f"Could not unzip the data set: {e}")
            return False


if __name__ == "__main__":
    d = Downloader()
    d.setup()
