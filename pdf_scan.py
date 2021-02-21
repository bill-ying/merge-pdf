import itertools
import os

import PyPDF2

FRONT_PAGE_FILE = '_front.pdf'
BACK_PAGE_FILE = '_back.pdf'


class PdfScan:
    pdf_merge = PyPDF2.PdfFileWriter()
    pdf_front = None
    pdf_back = None

    def merge_pdf(self, front_page_file_name):
        with open(front_page_file_name, 'rb') as file_front:
            merge_file_name = front_page_file_name.replace(FRONT_PAGE_FILE, '.pdf')
            back_page_file_name = front_page_file_name.replace(FRONT_PAGE_FILE, BACK_PAGE_FILE)

            if not os.path.exists(back_page_file_name):
                print('Error: Back page file ' + back_page_file_name + ' does not exist')
            else:
                with open(back_page_file_name, 'rb') as file_back:
                    self.pdf_front = PyPDF2.PdfFileReader(file_front)
                    self.pdf_back = PyPDF2.PdfFileReader(file_back)

                    if self.pdf_front.getNumPages() != self.pdf_back.getNumPages():
                        print("Error: Front and back have different page numbers for " + front_page_file_name)
                    else:
                        self._merge_pdf()

                        with open(merge_file_name, 'wb') as file_merge:
                            self.pdf_merge.write(file_merge)

        return

    def _merge_pdf(self):
        for page in itertools.chain.from_iterable(
                itertools.zip_longest(
                    self.pdf_front.pages,
                    reversed(self.pdf_back.pages),
                )
        ):
            if page:
                self.pdf_merge.addPage(page)