from typing import List

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

    @staticmethod
    def edit_for_tabs(encrypted_tab: List[int]) -> List[int]:
        
        new_lenght = [0] * 2

        len_num = len(encrypted_tab) + 2
        new_lenght[1] = len_num & 0xff
        new_lenght[0] = (len_num >> 8) & 0xff

        return new_lenght