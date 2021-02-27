"# merge-pdf" 

Budget all-in-one printers with automatic document feeder usually scan the front and back pages separately.  Two PDF files are created when a double-sided document is scanned.  These two files can be combined into one PDF file by using this program.

For instance, a 20 pages document is typically scanned as following two PDF files:
1. Front page PDF, starts with pages 1, 3, 5...
2. Back page PDF, starts with pages 20, 18, 16...

To use this program, scanned files need to be renamed to filename_front.pdf and filename_back.pdf, and placed in input_directory. The merged file will be input_directory/output/filename.pdf.

The program depends on package PyPDF2.

Run the program with input_directory as argument:

Example:
- python merge-pdf input_directory

In rare cases, such as Lexmark X5470, the back page PDF starts with pages 2, 4, 6....  Add -l option when running the program.

Example
- python merge-pdf -l input_directory





