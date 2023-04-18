from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
import json
import csv
import os
from pathlib import Path
import pandas as pd
import queue
import time
import threading
import asyncio
import aiohttp
import aiofiles
from uuid import uuid4

class FetchImageFile:
    
    def __init__(self, url: str, output_path: str, extension: str=".jpg", id:str=None) -> None:
        self.id = id if id is not None else uuid4().hex
        self.url = url
        if output_path[-1] != "/":
            output_path += "/"
        self.output_path = output_path + self.id + extension


class ImageFileSaveQueue:
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.__init__()
        return cls._instance
    
    def __init__(self, sleep_time:int = 2) -> None:
        self.queue = queue.Queue()
        self.sleep_time = sleep_time
        self.lock = threading.Lock()
    
    async def async_save_image(self, image: FetchImageFile):
        async with aiohttp.ClientSession() as session:
            async with session.get(image.url) as res:
                
                if res.status == 200:
                    content = await res.read()
                    async with aiofiles.open(image.output_path, "wb") as f:
                        await f.write(content)
                        print(image.id, "saved")
                else:
                    print("Download failed:", image.url)
                
    
    async def async_save_images(self, coroutines):
        await asyncio.gather(*coroutines, return_exceptions=True)
    
    def __start(self):
        
        while True:
            
            self.lock.acquire()
            size = self.queue.qsize()
            print('size', size)
            exit = False
            if size > 0:
                img_reqs = []
                
                for _ in range(0, size):
                    
                    item = self.queue.get()
                    if item is not None:
                        img_reqs.append(item)
                    else:
                        exit = True
                
                self.lock.release()
                
                with self.queue.mutex:
                    self.queue.queue.clear()
                
                coroutines = [
                    self.async_save_image(image=image_file)
                    for image_file in img_reqs
                ]
                
                asyncio.run(self.async_save_images(coroutines))
            else:
                self.lock.release()
            
            
            if self.queue.qsize() == 0 and exit:
                break
            time.sleep(self.sleep_time)
    
    def start(self):
        threading.Thread(target=self.__start).start()
        
    def put(self, item) -> None:
        self.lock.acquire()
        self.queue.put(item) 
        self.lock.release()
    
    

class File:
    
    @staticmethod
    def new(path: str) -> Path:
        p = Path(path)
        p.touch()
        return p
    
    @staticmethod
    def mkdir(path: str):
        Path(path).mkdir()
    
    @staticmethod
    def get_file_dir():
        return Path(__file__).parent.parent.resolve()
    
    @staticmethod
    def normailize(row: dict) -> dict:
        tmp_row = row.copy()
        if "session" in tmp_row:
            del tmp_row["session"]
        
        if "mutual_followed_by" in tmp_row:
            del tmp_row["mutual_followed_by"]

        if "post_edge" in tmp_row:
            del tmp_row["post_edge"]
        
        return tmp_row
    
    @staticmethod
    def append(data: list, output_path:str):
        if len(data) > 0:
            if not Path(output_path).exists():
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            fp = open(output_path, mode="a+", newline='', encoding='utf-8-sig')
            csv_writter = csv.DictWriter(fp, fieldnames=File.normailize(data[0].__dict__).keys())
            if os.stat(output_path).st_size == 0:
                csv_writter.writeheader()
            csv_writter.writerows([File.normailize(obj.__dict__) for obj in data])
            fp.close()


        

class CSVProcesser(ABC):
    
    def __init__(self, data: list) -> None:
        self.data = data
    
    @abstractmethod
    def execute(self):
        pass
    
class CSVMerge(CSVProcesser):
    
    def __init__(self, data: list) -> None:
        super().__init__(data)
    
    def execute(self):
        return [pd.concat(self.data, ignore_index=True, sort=False)]
    
class CSVDropDuplicate(CSVProcesser):
    
    def __init__(self, data: list) -> None:
        super().__init__(data)
        
    def execute(self):
        result = [d.drop_duplicates() for d in self.data]
        dup_result = [d[d.duplicated()] for d in self.data.copy()]
        for src_df, dup_df in zip(self.data, dup_result):
            print(f"Total: {len(src_df)} rows found, {len(dup_df)} row is duplicated.")
        return result

class CSVRMFollowed(CSVProcesser):
    
    def __init__(self, data: list) -> None:
        super().__init__(data)
        
    def execute(self):
        reuslt = [d[(d.followed_by_viewer == False) & (d.requested_by_viewer == False)] for d in self.data]
        print(f"{len(reuslt)} rows is followed or requested")
        return reuslt

class CSVRead(CSVProcesser):
    
    def __init__(self, data: list) -> None:
        super().__init__(data)
        
    def execute(self) -> list:
        return [pd.read_csv(path) for path in self.data]

class CSVPosting(CSVProcesser):
    
    def __init__(self, data: list, files: list, actions: list, output_path: str=None) -> None:
        super().__init__(data)
        self.actions = actions
        self.files = files
        self.output_path = output_path if output_path is not None else f"{File.get_file_dir()}/output/data-{''.join(actions).replace('&','_')}-{datetime.now().strftime('%d%m%YT%H%M%S')}.csv"
    
    def execute(self):
        if "merge" in self.actions:
            if len(self.data) == 1:
                df: pd.DataFrame = self.data.pop()
                df.to_csv(self.output_path,index=False, encoding='utf-8-sig')
                print(f"Saved at {self.output_path}")
            else:
                raise Exception("Length Error")
        else:
            for file_path, df in zip(self.files, self.data):
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                print(f"Saved at {file_path}")
            
class CSVProcess:
    
    def __init__(self, actions: list, file_paths: list, output_path: str) -> None:
        self.actions = actions
        self.file_paths = file_paths
        self.output_path = output_path
        
    
    def start(self):
        data = CSVRead(self.file_paths).execute()
        
        for action in self.actions:
            action = str(action).lower()
            print(action)
            if action == "merge":
                csvp = CSVMerge(data)
            elif action == "drop_dup":
                csvp = CSVDropDuplicate(data)
            elif action == "rm_fol":
                csvp = CSVRMFollowed(data)
            else:
                raise Exception("Action not found")
            
            data = csvp.execute()
        
        CSVPosting(data, self.file_paths, self.actions, self.output_path).execute()