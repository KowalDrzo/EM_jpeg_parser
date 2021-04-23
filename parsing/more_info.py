"""
OPIS TODO!!!
"""

def more_info_jpg(pic_inf):

    print("\n\n\n")

    """
    if pic_inf.necessary_chunks:
        pic_inf.sof_chunk.print_info()

    for scan in  pic_inf.binary_image_scan:
        scan.print_info()
    """
    for comment in pic_inf.comments:
        print("\nKomentarz: " + comment + "\n")

    if pic_inf.adh_chunk != None:
        pic_inf.adh_chunk.print_info()