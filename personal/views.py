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
		url = ''
		response = requests.post(url)
		print(response.content)
	# # Get the name of the uploaded file
	# file = request.FILES['file']
	# print file.name
	# handle_uploaded_file(file)
	# filename='/home/toobler/Documents/AjinToobler/python/mysite/personal/Files/'+str(file.name)
	
	# print count_pages(filename)
	# count= count_pages(filename)
	# temp=str(2)
	# pagecount = range(0,count)
	# for count in pagecount:
	# 	with Image(filename='/home/toobler/Documents/AjinToobler/python/mysite/personal/Files/'+str(file.name)+"["+str(count)+"]") as img:
	# 		 img.save(filename='/home/toobler/Documents/AjinToobler/python/mysite/personal/temp/temp'+str(count)+".jpg")

	# 	print(pytesseract.image_to_string(PIL.Image.open('/home/toobler/Documents/AjinToobler/python/mysite/personal/temp/temp'+str(count)+".jpg"), lang=language))
		
		# os.remove("/home/toobler/Documents/selftestocr/temp"+str(count)+".jpg")
		# solr insertion code
		# solr = pysolr.Solr('http://localhost:8984/solr/DocumentSearch/', timeout=10)
		# solr.add([
		#     {
		#         "pdfid": "doc_1",
		#         "title": "A test document",
		#         "author": "A test document",
		#         "publication": "A test document",
		#         "year":	" A test document",
		#         "synopsis": " A test document",
		#         "page_no": pagecount ,
		#         "totalpages": count ,
		#         "url": "A test document",
		#         "subjects": "A test document",
		#         "language": language,
		#         "origpath": "A test document",
		#         "Category": document_Type ,
		#         "format": "pdf",

		#     },
		# ])
	
	return render(request,'personal/homee.html')

