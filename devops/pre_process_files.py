import sys
from array import array
import os
from zipfile import ZipFile


def process_all(data_path):
    """
    Processes the tree of Terrain 50 data, creating a "bin" file of 200 x 200 IEE float height values, which have been
    read from the ASCII files for each tile.
    :param data_path:
    :return:
    """
    for dirName, subdirList, fileList in os.walk(data_path):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            # Looks for ZIP files, which should contain an ASC file whit a name matching the ZIP file name
            # This is extracted to  a temp location, then read to produce the bin file. The temp file is then deleted
            if fname[-4:] == ".zip":
                print('ZIP file: \t%s' % fname)
                full_name = os.path.join(dirName, fname)
                zip_file = ZipFile(full_name)
                asc_file = fname[0:4].upper() + ".asc"
                target = os.path.join(dirName, fname[0:4] + ".bin")
                temp_file = os.path.join(dirName, asc_file)
                asc_data = zip_file.extract(asc_file, dirName)
                process_file(temp_file, target)
                os.remove(temp_file)
            # If the ZIP files have already been extracted, then we can process the ASC files directly, but store the
            # bin files in the grid square folder rather than inside another directory level
            elif fname[-4:] == ".asc":
                print('ASC file: \t%s' % fname)
                full_name = os.path.join(dirName, fname)
                target_dir = "\\".join(dirName.split("\\")[:-1])
                target = os.path.join(target_dir, fname[0:-3] + "bin")
                process_file(full_name, target)


def process_file(asc_file, target):
    """
    Process a single ASC file, creating a bin file containing the 200x200 float values
    :param asc_file: asc file path
    :param target: target bin file path
    :return:
    """
    save_file = open(target, "wb")
    data_items = []

    with open(asc_file) as file_reader:
        nrows_row = file_reader.readline()
        ncols_row = file_reader.readline()
        xllcorner_row = file_reader.readline()
        yllcorner_row = file_reader.readline()
        cellsize_row = file_reader.readline()
        row = 0
        while row < 200:
            data_row = file_reader.readline()
            data_row_items = data_row.split(" ")
            for data_row_value in data_row_items:
                data_row_float_value = float(data_row_value)
                data_items.append(data_row_float_value)
            row += 1

    data_array = array("f", data_items)
    data_array.tofile(save_file)
    save_file.close()


if __name__ == "__main__":
    process_all(sys.argv[1])
