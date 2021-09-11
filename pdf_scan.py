import itertools
import os
import re

import PyPDF2

FRONT_PAGE_FILE = '_front.pdf'
BACK_PAGE_FILE = '_back.pdf'


class PdfScan:
    count = 0

    _pdf_merge = None
    _pdf_front = None
    _pdf_back = None

    def merge_pdf(self, front_page_file_name):
        self._pdf_merge = PyPDF2.PdfFileWriter()

        with open(front_page_file_name, 'rb') as file_front_read:
            front_page_file_base_name = os.path.basename(front_page_file_name)
            merge_file_base_name = re.sub(FRONT_PAGE_FILE, '.pdf', front_page_file_base_name, flags=re.IGNORECASE)
            output_directory = os.path.join(os.path.dirname(front_page_file_name), 'output')

            if not os.path.exists(output_directory):
                os.mkdir(output_directory)

            merge_file_name = os.path.join(output_directory, merge_file_base_name)
            back_page_file_name = re.sub(FRONT_PAGE_FILE, BACK_PAGE_FILE, front_page_file_name, flags=re.IGNORECASE)

            if not os.path.exists(back_page_file_name):
                print('Error: Back page file ' + back_page_file_name + ' does not exist')
            else:
                with open(back_page_file_name, 'rb') as file_back_read:
                    self._pdf_front = PyPDF2.PdfFileReader(file_front_read)
                    self._pdf_back = PyPDF2.PdfFileReader(file_back_read)

                    if self._pdf_front.getNumPages() != self._pdf_back.getNumPages():
                        print("Error: Front and back have different page numbers for " + front_page_file_name)
                    else:
                        self._merge_pdf()

                        with open(merge_file_name, 'wb') as file_merge_write:
                            self._pdf_merge.write(file_merge_write)

                        self.count += 1

        return

    def _merge_pdf(self):
        for page in itertools.chain.from_iterable(
                itertools.zip_longest(
                    self._pdf_front.pages,
                    reversed(self._pdf_back.pages),
                )
        ):
            if page:
                self._pdf_merge.addPage(page)
