"""
OPIS TODO!!!
"""

def more_info_jpg(pic_inf):

    print("\n\n\n")

    for nec_chunk in pic_inf.necessary_chunks:
        try:
            print("##############################################")
            nec_chunk.print_info()
        except:
            pass

    for comment in pic_inf.comments:
        print("\nKomentarz: " + comment + "\n")

    for met_chunk in pic_inf.metadata_chunks:
        try:
            print("##############################################")
            met_chunk.print_info()
        except:
            pass