import glob
import os
import sys
import argparse

from pdf_scan import PdfScan, FRONT_PAGE_FILE
from lexmart_pdf_scan import LexmarkPdfScan


def main(input_directory, is_lexmark):
    return_code = 0

    if not os.path.exists(input_directory):
        print('Error: path ' + input_directory + ' does not exist')
        return_code = 1002
    else:
        file_name = os.path.join(input_directory, '*' + FRONT_PAGE_FILE)
        pdf_file_list = glob.glob(file_name)

        if len(pdf_file_list) == 0:
            print('No files to process.')
        else:
            scan = _get_scan(is_lexmark)

            for front_page_file_name in pdf_file_list:
                scan.merge_pdf(front_page_file_name)

    return return_code


def _get_scan(is_lexmark):
    return LexmarkPdfScan() if is_lexmark else PdfScan()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description
                                     ='Merge front and back PDF pages from one side scanner into one PDF file.')
    parser.add_argument('path')
    parser.add_argument('-l', '--lexmark', action='store_true', help='for Lexmark X5470 scanner')
    args = parser.parse_args()
    sys.exit(main(args.path, args.lexmark))
