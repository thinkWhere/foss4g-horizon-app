from cachetools import cached, LRUCache
from s3_service import S3Service
from config import Config
import struct

# Path/format of the height data files
S3_DATA_ROOT = "data/{0}/{1}.bin"
# Float type length used to calculate offset within file
FLOAT_SIZE = 4
# No of columns in the files used to calculate offset within file
COLS = 200
ROWS = 200


class HeightData:
    """
    Reads height data from the binary terrain 50 files based on the requested locations
    Caches height files in an LRU cache
    """

    # Grid of square letters used by BNG system to calculate the grid square for a loation
    GRID = [
        ["V", "W", "X", "Y", "Z"],
        ["Q", "R", "S", "T", "U"],
        ["L", "M", "N", "O", "P"],
        ["F", "G", "H", "J", "K"],
        ["A", "B", "C", "D", "E"]]

    def get_height(self, x, y):
        """
        Returns the height value for a given coordinate
        :param x:
        :param y:
        :return: height value
        """
        grid, ox, oy = self._calc_grid_location(x, y)
        return self._read_height_from_file(grid, ox, oy)

    def _calc_grid_location(self, x, y):
        """
        Calculates the grid file, and 50m x and y offsets for a given coordinate
        :param x:
        :param y:
        :return:
        """
        x = int(round(x))
        y = int(round(y))
        x_s1 = (x // 500000) + 2
        y_s1 = (y // 500000) + 1
        x_s2 = (x % 500000) // 100000
        y_s2 = (y % 500000) // 100000
        x_10k = (x % 100000) // 10000
        y_10k = (y % 100000) // 10000
        s1 = self.GRID[y_s1][x_s1]
        s2 = self.GRID[y_s2][x_s2]
        grid = "{0}{1}{2}{3}".format(s1, s2, x_10k, y_10k)
        ox = (x % 10000) // 50
        oy = (y % 10000) // 50
        return grid, ox, oy

    def _read_height_from_file(self, grid, ox, oy):
        """
        Reads the height value by loading the correct file, and finding the correct value using the x and y offsets
        :param grid:
        :param ox: range 0 - 199
        :param oy: range 0 - 199
        :return:
        """
        file_reader = self._read_height_file(grid)
        if file_reader is None:
            return 0
        else:
            position = (((ROWS - 1 - oy) * COLS) + ox) * FLOAT_SIZE
            file_reader.seek(position)
            float_value = struct.unpack('f', file_reader.read(FLOAT_SIZE))
            return round(float_value[0], 1)

    # Cache for the height files
    file_cache = LRUCache(maxsize=10)

    @cached(cache=file_cache)
    def _read_height_file(self, grid):
        """
        Loads a height binary file from the grid square
        :param grid:
        :return:
        """
        s = grid[0:2]
        s3_file_path = S3_DATA_ROOT.format(s.lower(), grid.lower())
        s3_service = S3Service()
        buffer = s3_service.download_binary_data(Config.TERRAIN_DATA_BUCKET, s3_file_path)
        return buffer
