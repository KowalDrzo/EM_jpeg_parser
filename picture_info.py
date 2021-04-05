
class PictureInfo:

    file = None

    def __init__(self, file_name):
        self.file = open(file_name, "rb")

    def __del__(self):
        self.file.close()

    def read_chunk_name(self) -> int:
        chunk_name = self.file.read(2)
        return int.from_bytes(chunk_name, "big")

    def check_soi(self):

        int_byte = self.read_chunk_name()

        if int_byte != 0xffd8:
            
            print("Niepoprawny JPEG!")
            raise IOError