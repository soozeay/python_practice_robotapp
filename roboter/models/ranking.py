"""Generates ranking model to write to CSV
"""
# collectionライブラリについて https://qiita.com/apollo_program/items/165fb01b52702274936c
import collections
import csv
import os
import pathlib # PythonでUNIXやWindowsのファイルやディレクトリ（のパス）を扱うためのもの


RANKING_COLUMN_NAME = 'NAME'
RANKING_COLUMN_COUNT = 'COUNT'
RANKING_CSV_FILE_PATH = 'ranking.csv'


class CsvModel(object):
    """Base csv model."""
    def __init__(self, csv_file):
        self.csv_file = csv_file
        # 初回起動時にcsv_fileを生成
        if not os.path.exists(csv_file):
            pathlib.Path(csv_file).touch()


class RankingModel(CsvModel):
    """Definition of class that generates ranking model to write to CSV"""
    def __init__(self, csv_file=None, *args, **kwargs): # *args：複数の引数をタプルとして受け取る, **kwargs：複数のキーワード引数を辞書として受け取る
        if not csv_file:
            csv_file = self.get_csv_file_path() # get_csv_file_pathの中身は csv_file_path = 'ranking.csv'
        super().__init__(csv_file, *args, **kwargs)
        self.column = [RANKING_COLUMN_NAME, RANKING_COLUMN_COUNT]
        # collections.defaultdict：存在しないキーを参照した際にデフォルト値が入った状態になっている辞書型風のデータ構造
        self.data = collections.defaultdict(int)
        self.load_data()

    def get_csv_file_path(self):
        """Set csv file path.

        Use csv path if set in settings, otherwise use default
        """
        csv_file_path = None
        try:
            import settings # console.py同様の扱い、今回はヒットしない
            if settings.CSV_FILE_PATH:
                csv_file_path = settings.CSV_FILE_PATH
        except ImportError:
            pass

        if not csv_file_path:
            csv_file_path = RANKING_CSV_FILE_PATH
        return csv_file_path

    def load_data(self):
        """Load csv data.

        Returns:
            dict: Returns ranking data of dict type.
        """
        with open(self.csv_file, 'r+') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.data[row[RANKING_COLUMN_NAME]] = int(row[RANKING_COLUMN_COUNT])
        return self.data

    def save(self):
        """Save data to csv file."""
        with open(self.csv_file, 'w+') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.column)
            writer.writeheader()

            for name, count in self.data.items():
                writer.writerow({
                    RANKING_COLUMN_NAME: name,
                    RANKING_COLUMN_COUNT: count
                })

    def get_most_popular(self, not_list=None):
        """Fetch the data of the top most ranking.

        Args:
            not_list (list): Excludes the name on the list.

        Returns:
            str: Returns the data of the top most ranking
        """
        if not_list is None: # 初回起動時にリストを生成
            not_list = []

        if not self.data: # data = collections.defaultdict(int)
            return None

        sorted_data = sorted(self.data, key=self.data.get, reverse=True)
        for name in sorted_data:
            if name in not_list:
                continue
            return name

    def increment(self, name):
        """Increase rank for the give name."""
        self.data[name.title()] += 1
        self.save()
