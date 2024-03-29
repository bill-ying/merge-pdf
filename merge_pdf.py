import concurrent.futures
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
            output_directory = os.path.join(input_directory, 'output')

            if not os.path.exists(output_directory):
                os.mkdir(output_directory)

            scan = __get_scan(is_lexmark)

            # Use multi-processor for CPU bond operations
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = [executor.submit(scan.merge_pdf, f, output_directory) for f in front_page_pdf_files]

            for result in concurrent.futures.as_completed(results):
                print(result.result())

            print('All documents have been processed.')

    return return_code


# Factory method pattern
def __get_scan(is_lexmark):
    return LexmarkPdfScan() if is_lexmark else PdfScan()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description
                                     ='Merge front and back PDF pages from scanned one side scanner into one PDF file.'
                                      '  The merged files will be located in <input_directory>/output')
    parser.add_argument('input_directory', help='the directory for front page and back page PDFs, contains a list of '
                                                '<file>_front.pdf and <file>_back.pdf files')
    parser.add_argument('-r', '--reverse', action='store_true', help='for Lexmark X5470 scanner')
    args = parser.parse_args()
    sys.exit(main(args.input_directory, args.reverse))
