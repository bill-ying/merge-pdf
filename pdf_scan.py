import itertools
import os
import re

import pypdf

FRONT_PAGE_FILE = '_front.pdf'
BACK_PAGE_FILE = '_back.pdf'


class PdfScan:
    def __init__(self):
        self.__pdf_merge = None
        self.__pdf_front = None
        self.__pdf_back = None

    def merge_pdf(self, front_page_file_name, output_directory):
        self.__pdf_merge = pypdf.PdfWriter()

        with open(front_page_file_name, 'rb') as file_front_read:
            front_page_file_base_name = os.path.basename(front_page_file_name)
            merge_file_base_name = re.sub(FRONT_PAGE_FILE, '.pdf', front_page_file_base_name, flags=re.IGNORECASE)
            merge_file_name = os.path.join(output_directory, merge_file_base_name)
            back_page_file_name = re.sub(FRONT_PAGE_FILE, BACK_PAGE_FILE, front_page_file_name, flags=re.IGNORECASE)

            if not os.path.exists(back_page_file_name):
                print('Error: Back page file ' + back_page_file_name + ' does not exist')
            else:
                with open(back_page_file_name, 'rb') as file_back_read:
                    self.__pdf_front = pypdf.PdfReader(file_front_read)
                    self.__pdf_back = pypdf.PdfReader(file_back_read)

                    if len(self.__pdf_front.pages) != len(self.__pdf_back.pages):
                        print("Error: Front and back have different page numbers for " + front_page_file_name)
                    else:
                        self._merge_pdf()

                        with open(merge_file_name, 'wb') as file_merge_write:
                            self.__pdf_merge.write(file_merge_write)

        return merge_file_name + ' completed.'

    def _merge_pdf(self):
        for page in itertools.chain.from_iterable(
                itertools.zip_longest(
                    self.__pdf_front.pages,
                    reversed(self.__pdf_back.pages),
                )
        ):
            if page:
                self.__pdf_merge.add_page(page)
