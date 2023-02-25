from django.shortcuts import render, HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
import PyPDF2
import sumy
import nltk
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

LANGUAGE = "english"


def PaperUploadView(request):
    if request.method == 'POST':
        form = UploadPaperForm(request.POST,request.FILES)
        file = request.FILES['file']
        rp = Research_Papers(paper=file)
        rp.save()
        reader = PyPDF2.PdfReader(file)
        # Get the first page of the PDF document
        first_page = reader.pages[0]

        # Extract the text from the first page
        text = first_page.extract_text()

        # Find the start and end indices of the abstract
        start_index = text.find('Abstract')
        end_index = text.find('\nI.', start_index)

        # Extract the abstract text

        abstract = text[start_index:end_index].replace('\n', ' ')
        # Print the abstract
        
        sentences = abstract.split(". ")

        abst = []
        for sentence in sentences:
            abst.append(sentence + ".")
        
        abt = ' '.join(abst)
        parser = PlaintextParser.from_string(abt,Tokenizer(LANGUAGE))
        summarizer = LsaSummarizer()
        testsummary = summarizer(parser.document,sentences_count=4)
        summary = ""
        for sentence in testsummary:
            summary+=str(sentence)
    
        return render(request, 'project/summary.html',{'summary':summary, 'abstract':abt})
    else:
        form = UploadPaperForm()
    return render(request, 'project/upload.html', {'form':form})


def singup(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        pswd = data['pwd']
        email = data['email']
        
        user = User.objects.create_user(username=username, password=pswd, email=email)
        user.save()
        return render(request, 'project/upload.html',{'msg':'Welcome!'})
    return render(request,'project/signup.html')

def login(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        pswd = data['pwd']
        user = authenticate(request, username=username,password=pswd)
        
        if user is not None:
            auth_login(request,user)
            return render(request, 'project/upload.html', {'msg':'Welcome!'})
        return render(request, 'project/login.html', {'msg':'Invalid Credentials!'})
    return render(request, 'project/login.html')


# def summary(request,file):
#     filename = file
#     pdfFileobj = open(filename, 'rb')
#     pdfReader = PyPDF2.PdfFileReader(pdfFileobj)
#     pagedata = pdfReader.getPage(0)
#     return render(request, 'project/summary.html',{'data':pagedata})





# Define the text to be summarized
text = 'This is some example text that we want to summarize. We will use the TextRank algorithm to identify the most important sentences in the text.'

