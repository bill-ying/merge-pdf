import glob
import os
import sys
import argparse

from pdf_scan import PdfScan, FRONT_PAGE_FILE
from lexmart_pdf_scan import LexmarkPdfScan


def main(input_directory, is_lexmark):
    return_code = 0

    if not os.path.exists(input_directory):
        print('Error: ' + input_directory + ' does not exist')

        return_code = 1001
    else:
        file_to_search = os.path.join(input_directory, '*' + FRONT_PAGE_FILE)
        front_page_pdf_files = glob.glob(file_to_search)

        if len(front_page_pdf_files) == 0:
            print('No file to process.')
        else:
            scan = _get_scan(is_lexmark)

            for front_page_file_name in front_page_pdf_files:
                scan.merge_pdf(front_page_file_name)

            print(str(scan.count) + ' documents processed.')

    return return_code


# Factory method pattern
def _get_scan(is_lexmark):
    return LexmarkPdfScan() if is_lexmark else PdfScan()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description
                                     ='Merge front and back PDF pages from scanned one side scanner into one PDF file.'
                                      '  The merged files will be located in <input_directory>/output')
    parser.add_argument('input_directory', help='the directory for front page and back page PDFs, contains a list of '
                                                '<file>_front.pdf and <file>_back.pdf files')
    parser.add_argument('-l', '--lexmark', action='store_true', help='for Lexmark X5470 scanner')
    args = parser.parse_args()
        sys.exit(main(args.input_directory, args.lexmark))
