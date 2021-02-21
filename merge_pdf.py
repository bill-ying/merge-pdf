import sys, os, glob, itertools

import PyPDF2

ODD_PAGE_FILE_NAME = '_front.pdf'
EVEN_PAGE_FILE_NAME = '_back.pdf'


def main():
    return_code = 0
    input_directory = sys.argv[1]

    if not os.path.exists(input_directory):
        print('Error: path ' + input_directory + ' does not exist')
        return_code = 1002
    else:
        file_name = os.path.join(input_directory, '*' + ODD_PAGE_FILE_NAME)
        pdf_file_list = glob.glob(file_name)

        if len(pdf_file_list) == 0:
            print('No files to process.')
        else:
            for odd_page_file in pdf_file_list:
                merge_pdf(odd_page_file)

    return return_code


def merge_pdf(odd_page_file):
    pdf_out = PyPDF2.PdfFileWriter()

    with open(odd_page_file, 'rb') as file_odd:
        output_file_name = odd_page_file.replace(ODD_PAGE_FILE_NAME, '.pdf')
        even_page_file = odd_page_file.replace(ODD_PAGE_FILE_NAME, EVEN_PAGE_FILE_NAME)

        if not os.path.exists(even_page_file):
            print('Error: Back page file ' + even_page_file + ' does not exist')
        else:
            with open(even_page_file, 'rb') as file_even:
                pdf_odd = PyPDF2.PdfFileReader(file_odd)
                pdf_even = PyPDF2.PdfFileReader(file_even)

                if pdf_odd.getNumPages() != pdf_even.getNumPages():
                    print("Error: Front and back have different page numbers for " + odd_page_file)
                else:
                    for p in itertools.chain.from_iterable(
                            itertools.zip_longest(
                                pdf_odd.pages,
                                # reversed(pdf_even.pages),
                                pdf_even.pages,  # Lexmark X5470 only
                            )
                    ):
                        if p:
                            pdf_out.addPage(p)

                    with open(output_file_name + ".pdf", 'wb') as f_out:
                        pdf_out.write(f_out)

    return


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: merge_pdf <path>')
        sys.exit(1001)

    sys.exit(main())
