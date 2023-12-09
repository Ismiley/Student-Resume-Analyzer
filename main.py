import glob

class Resume:
    def __init__(self, resume_name, path):
        self.resume_name = resume_name
        self.path        = path
        self.rushee_name = ""
        self.file_name   = ""
        self.string      = ""

def convert_to_python_string(resume):
    # convert a pdf file to a string
    return None

def get_rushees_name(resume):
    # Figure out how to safely get a rushee's name based on the resume file
    return ""

if __name__ == "__main__":
    resumes = []
    for path in glob.glob("resumes/*"):
        resume_name = path.split("/")[-1]
        resume      = Resume(resume_name, path)

        resume.string      = convert_to_python_string(resume)
        resume.rushee_name = get_rushees_name(resume)

