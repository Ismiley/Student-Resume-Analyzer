from ast import keyword
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem import WordNetLemmatizer 
import re
import spacy
from spacy.matcher import Matcher


def keywordCounter(resumeString):

    lemmatizer = WordNetLemmatizer()

    resumeKeywordsList = nltk.word_tokenize(resumeString)
    resumeKeywordsList = [lemmatizer.lemmatize(w) for w in resumeKeywordsList]
    # ignore case for resumeString
    resumeKeywordsList = [token.lower() for token in resumeKeywordsList]

    # generate list of keywords
    # pass in file with keywords (split by .split())
    # create dictionary of keywords

    # CCO keywords
    keywords = "Circulate Clarify Collaborate Communicate Compose Correspond Demonstrate Document Edit Engage Entertain Exhibit Explain Express Illustrate Interpret Interview Investigate Lecture Optimize Partner Perform Pitch Plan Present Promote Proofread Publicize Relate Relay Report Review Revise Summarize Syndicate Translate Transcribe Advise Correct Counsel Demonstrate Display Encourage Enlist Ensure Grade Guide Influence Instruct Introduce Lecture Mentor Program Provide Rate Steer Suggest Support Teach Test Train Tutor Advertise Advocate Attend Coordinate Convince Dispense Disseminate Distribute Fundraise Influence Launch Lobby Persuade Publicize Publish Recruit Screen Sell Service Target Accommodate Adapt Anticipate Assure Bargain Care Coach Collaborate Confer Confront Consult Converse Cooperate Critique Develop Encourage Familiarize Form Foster Fulfill Implement Inform Interact Intervene Join Listen Litigate Mediate Motivate Negotiate Participate Partner Provide Recommend Reconcile Rehabilitate Represent Resolve Share Suggest Accelerate Accomplish Achieve Act Administer Allocate Approve Assign Assess Attain Benchmark Chair Commend Compromise Consolidate Control Delegate Direct Enforce Entrust Expedite Govern Head Hire Improvise Initiate Institute Judge Lead Maintain Manage Moderate Monitor Officiate Order Oversee Prescreen Preside Prioritize Produce Prohibit Refer Regulate Run Start Streamline Strengthen Supervise Acquire Analyze Classify Collate Collect Compile Conduct Data Deliver Detect Determine Discover Dissect Evaluate Explore Examine Formulate Gather Identify Inspect Investigate Locate Model Obtain Pinpoint Prepare Prioritize Research Specify Survey Test Trace Track Verify Abstract Account Add Appraise Audit Budget Calculate Collect Compute Decrease Determine Divide Estimate File Finance Formulate Increase Insure Inventory Invest Market Maximize Minimize Multiply Process Project Purchase Record Reduce Solve Quantify Appraise Apply Arrange Balance Catalog Categorize Connect Coordinate Define Edit Establish Facilitate File Group Incentivize Issue Modify Orchestrate Organize Overhaul Place Prepare Program Qualify Reorganize Rewrite Schedule Assemble Build Customize Design Enlarge Format Function Generate Improve Install Manufacture Navigate Operate Propose Refinish Renovate Repair Restore Update Upgrade Construct Landscape Produce Shape Utilize Adjust Compose Develop Devise Guide Implement Innovate Invent Present Activate Complete Conserve Contract Create Discover Draft Draw Engineer Execute Expand Generate Inaugurate Launch Modify Mold Reconstruct Synthesize Transform Unite Act Apply Anticipate Change Check Contribute Cover Decide Define Diagnose Effect Eliminate Emphasize Establish Facilitate Forecast Found Navigate Offer Perform Propose Refer Referee Register Reinforce Resolve Respond Retrieve Save Select Serve Set Simplify Study Take Travel Use Win"
    wordList = nltk.word_tokenize(keywords)

    
    wordList = [lemmatizer.lemmatize(w) for w in wordList]
    

    # ignore case for keywords
    wordList = [token.lower() for token in wordList]

    # convert words into lamentized list --> roots of words

    # Logic: word not in the dict, give it a value of 1. if key already present, +1.
    
    wordFreq = {}
    for word in wordList:
        if word not in wordFreq:
            wordFreq[word] = 1
        else:
            wordFreq[word] += 1
    count = 0
    for word in resumeKeywordsList:
        if word in wordList:
            count += wordFreq[word]
            #print(word + " ")

    return count





def extract_email(text):
    '''
    Helper function to extract email id from text
    :param text: plain text extracted from resume file
    '''
    email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None


def extract_name(nlp_text):


    # load pre-trained model
    nlp = spacy.load('en_core_web_sm')

    # initialize matcher with a vocab
    matcher = Matcher(nlp.vocab)

    nlp_text = nlp(nlp_text)
    
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME', [pattern])
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text


def extract_mobile_number(text, custom_regex=None):

    if not custom_regex:
        mob_num_regex = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                        [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'''
        phone = re.findall(re.compile(mob_num_regex), text)
    else:
        phone = re.findall(re.compile(custom_regex), text)
    if phone:
        number = ''.join(phone[0])
        return number
