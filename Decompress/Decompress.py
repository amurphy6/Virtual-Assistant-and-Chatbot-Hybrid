import zstandard
import pathlib
import shutil

input_file = "C:/Users/Adam Murphy/Downloads/RC_2019-12.zst"
def decompress_zstandard_to_folder(input_file):
    input_file = pathlib.Path(input_file)
    with open(input_file, 'rb') as compressed:
        decomp = zstandard.ZstdDecompressor()
        output_path = pathlib.Path("C:/Users/Adam Murphy/Downloads") / input_file.stem
        with open(output_path, 'wb') as destination:
            decomp.copy_stream(compressed, destination)

if __name__ == '__main__':
    decompress_zstandard_to_folder(input_file)
