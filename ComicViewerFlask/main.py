# main.py
import json
import time
from pathlib import Path
import os

class ComicLibrary:
    def __init__(self, comics_folder):
        self.comics_folder = Path(comics_folder)
        self.comics = []
        self.load_comics()

    def load_comics(self):
        for root, _, files in os.walk(self.comics_folder):
            series_name = Path(root).name
            for file in sorted(files):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    filepath = Path(root) / file
                    comic_id = len(self.comics) + 1
                    comic = {
                        'id': comic_id,
                        'name': file,
                        'path': str(filepath.relative_to(self.comics_folder.parent)).replace('\\', '/'),
                        'series': series_name,
                        'timestamp': time.time()
                    }
                    self.comics.append(comic)
        self.save_comics()

    def save_comics(self):
        with open('comics.json', 'w') as f:
            json.dump(self.comics, f)

    def get_all_comics(self):
        return self.comics

    def get_comics_by_series(self):
        comics_by_series = {}
        for comic in self.comics:
            series = comic['series']
            if series not in comics_by_series:
                comics_by_series[series] = []
            comics_by_series[series].append(comic)
        return comics_by_series

    def get_comic_by_id(self, comic_id):
        for comic in self.comics:
            if comic['id'] == comic_id:
                return comic
        return None

    def get_pages_by_series(self, series):
        return [comic for comic in self.comics if comic['series'] == series]

    def get_next_comic(self, comic_id):
        current_index = next((index for (index, comic) in enumerate(self.comics) if comic['id'] == comic_id), None)
        if current_index is not None and current_index < len(self.comics) - 1:
            return self.comics[current_index + 1]
        return None

    def get_previous_comic(self, comic_id):
        current_index = next((index for (index, comic) in enumerate(self.comics) if comic['id'] == comic_id), None)
        if current_index is not None and current_index > 0:
            return self.comics[current_index - 1]
        return None
