"""
OPIS TODO!!!
"""

def more_info_jpg(pic_inf):

    print("\n\n\n")

    for nec_chunk in pic_inf.necessary_chunks:
        try:
            nec_chunk.print_info()
        except:
            pass

    for comment in pic_inf.comments:
        print("\nKomentarz: " + comment + "\n")

    if pic_inf.adh_chunk != None:
        pic_inf.adh_chunk.print_info()