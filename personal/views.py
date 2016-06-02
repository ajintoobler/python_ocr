import requests
import Image
import PIL.Image
import pytesseract
import re
import os
import tempfile
import subprocess
import pysolr
from wand.image import Image
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from personal import db
# front page
def index(request):

    return render(request,'personal/login.html')

# login
def login(request):
	
	result=db.login_view(request)
	if result == "true":
		return render(request,'personal/home.html')
	else:
		return render(request,'personal/login.html')

# submit contianer
# def insert(request):
# 	type=request.POST.get('type')
# 	Identifier=request.POST.get('Identifier')
# 	language=request.POST.get('ocr_languages')
# 	document_Type=request.POST.get('document_Type')
# 	subjects=request.POST.get('subjects')
# 	title=request.POST.get('title')
# 	print title
# 	return render(request,'personal/home.html')


#count number of pages in pdf Document
rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)
def count_pages(filename):
    data = file(filename,"rb").read()
    return len(rxcountpages.findall(data))

# upload files from client
def handle_uploaded_file(f):
    with open('/home/toobler/Documents/AjinToobler/python/mysite/personal/Files/'+str(f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@csrf_exempt
def insert(request):
	filename=''
	count=''
	type=request.POST.get('type')
	Identifier=request.POST.get('Identifier')
	language=request.POST.get('ocr_languages')
	document_Type=request.POST.get('document_Type')
	subjects=request.POST.get('subjects')
	title=request.POST.get('title')

	#insert container into fedora repository
	if type=="Container":
		url = 'http://localhost:8080/fcrepo-webapp-4.5.0/rest/'
		response = requests.post(url)
		print(response.content)
	else:
		# Get the name of the uploaded file
		file = request.FILES['file']
		print file.name
		handle_uploaded_file(file)
		filename='/home/toobler/Documents/AjinToobler/python/mysite/personal/Files/'+str(file.name)
	
		#insert file into fedora repository
		url = 'http://localhost:8080/fcrepo-webapp-4.5.0/rest/'
		files = {'file': open('/home/toobler/Documents/AjinToobler/python/mysite/personal/Files/'+str(file.name), 'rb')}
		response=requests.post(url, files=files)
		print(response.content)
		savedFileUrl=response.content

		
		
		totalPages=count_pages(filename)
		count= count_pages(filename)
		temp=str(2)
		pagecount = range(0,count)
		for count in pagecount:
			currentPage=count+1
			with Image(filename='/home/toobler/Documents/AjinToobler/python/mysite/personal/Files/'+str(file.name)+"["+str(count)+"]") as img:
				 img.save(filename='/home/toobler/Documents/AjinToobler/python/mysite/personal/temp/temp'+str(count)+".jpg")

			print(pytesseract.image_to_string(PIL.Image.open('/home/toobler/Documents/AjinToobler/python/mysite/personal/temp/temp'+str(count)+".jpg"), lang=language))
			tessaract_ocr=pytesseract.image_to_string(PIL.Image.open('/home/toobler/Documents/AjinToobler/python/mysite/personal/temp/temp'+str(count)+".jpg"), lang=language)
			#Remove Each PDF page image 
			os.remove('/home/toobler/Documents/AjinToobler/python/mysite/personal/temp/temp'+str(count)+".jpg")
			# solr insertion code
			solr = pysolr.Solr('http://localhost:8983/solr/DocumentSearch/', timeout=10)
			solr.add([
			    {
			        "pdfid": "doc_1",
			        "title": "A test document",
			        "author": "A test document",
			        "publication": "A test document",
			        "year":	" A test document",
			        "synopsis": " A test document",
			        "page_no": currentPage ,
			        "totalpages": totalPages ,
			        "url": "A test document",
			        "subjects": subjects,
			        "language": " A test document",
			        "origpath": savedFileUrl,
			        "Category": document_Type ,
			        "format": "pdf",
			        "content": tessaract_ocr,

			    },
			])
	
	return render(request,'personal/homee.html')

