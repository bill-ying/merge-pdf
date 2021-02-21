import itertools

from pdf_scan import PdfScan


class LexmarkPdfScan(PdfScan):
    def _merge_pdf(self):
        for page in itertools.chain.from_iterable(
                itertools.zip_longest(
                    self.pdf_front.pages,
                    self.pdf_back.pages,  # Lexmark X5470
                )
        ):
            if page:
                self.pdf_merge.addPage(page)