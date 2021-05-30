from typing import List, Type

class ChunkEditor:

    @staticmethod
    def edit_for_sof(encrypted_sof: List[int], decryption: bool) -> List[int]:
        
        if not decryption:

            i = 0
            for element in encrypted_sof:
                i += 1
                if element == 0xff:
                    encrypted_sof.insert(i, 0x00)

        else:
            i = 0
            for element in encrypted_sof:
                i += 1
                if element == 0xff:
                    encrypted_sof.pop(i)


        return encrypted_sof

