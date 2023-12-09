from PyPDF2 import PdfFileReader, PdfFileWriter

from parseFunctions import *

def main():
    file_path = 'testResume.pdf'
    pdf = PdfFileReader(file_path)

    resumeString = ""


    for page_num in range(pdf.numPages):
        pageObj = pdf.getPage(page_num)

        try:
            txt = pageObj.extractText() # string
            resumeString = resumeString + " " + txt
        except:
            pass

    count = keywordCounter(resumeString)
    mobileNumber = extract_mobile_number(resumeString, custom_regex=None)
    email = extract_email(resumeString)
    name = extract_name(resumeString)

    print(f"\nThis is the keyword count: {count}")
    print(f"\nThis is the phone number: {mobileNumber}")
    print(f"\nThis is the email: {email}")
    print(f"\nThis is the name: {name}")

if __name__ == "__main__":
    main()