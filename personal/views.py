import tika 
from tika import parser 
import random
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
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from personal import db
# front page
def index(request):

    return render(request,'personal/adminLogin.html')

# login
def login(request):
	
	result=db.login_view(request)
	if result == "true":
		return render(request,'personal/adminHome.html')
	else:
		return render(request,'personal/adminLogin.html')

# redirect page
def redirect(request):
	
	return render(request,'personal/adminHome.html')
	
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
def handle_uploaded_file(f,current_dir):
    with open(current_dir+'/personal/Files/'+str(f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@csrf_exempt
def insert(request):
	filename=''
	count=''
	str1=''
	ocrMethod=request.POST.get('ocrMethod')
	type=request.POST.get('type')
	Identifier=request.POST.get('Identifier')
	language=request.POST.get('ocr_languages')
	document_Type=request.POST.get('document_Type')
	subjects=request.POST.get('subjects')
	title=request.POST.get('title')
	book_title=request.POST.get('book_title')
	author=request.POST.get('author')
	year=request.POST.get('year')
	description=request.POST.get('description')
	book_id=book_title+"_"+str(random.randint(1000, 9999))
	# get current directory
	current_dir=os.getcwd()
	print current_dir
	#insert container into fedora repository
	if type=="Container":
		url = 'http://localhost:8080/fcrepo-webapp-4.5.0/rest/'
		response = requests.post(url)
		print(response.content)
		savedContainerUrl=response.content
		result=db.insert_container(request,savedContainerUrl)
		return HttpResponseRedirect('/redirect/')
	else:
		# Get the name of the uploaded file
		file = request.FILES['file']
		print file.name
		handle_uploaded_file(file,current_dir)
		filename=current_dir+'/personal/Files/'+str(file.name)
	
		#insert file into fedora repository
		url = 'http://localhost:8080/fcrepo-webapp-4.5.0/rest/'
		files = {'file': open(current_dir+'/personal/Files/'+str(file.name), 'rb')}
		response=requests.post(url, files=files)
		print(response.content)
		savedFileUrl=response.content

		
		
		totalPages=count_pages(filename)
		count= count_pages(filename)
		temp=str(2)
		pagecount = range(0,count)
		if ocrMethod=="Tika_OCR":
			#tikka parser code
			parsed = parser.from_file(filename)
			cont=parsed["content"]
			contents = cont.replace("\n", " ");
			print(parsed["content"])
			# solr insertion for book
			solr = pysolr.Solr('http://localhost:8983/solr/DocumentSearch/', timeout=10)
			solr.add([
			    {
			        "pdfid": book_id,
			        "title": book_title,
			        "author": author,
			        "year":	year,
			        "synopsis": description,
			        "page_no": 'currentPage',
			        "totalpages": 'totalPages' ,
			        "subjects": subjects,
			        "language": language,
			        "origpath": savedFileUrl,
			        "Category": document_Type ,
			        "format": "pdf",
			        "content": contents,

			    },
			])
		else:	
			for count in pagecount:
				currentPage=count+1
				with Image(filename=current_dir+'/personal/Files/'+str(file.name)+"["+str(count)+"]") as img:
					 scaler = 3
					 img.resize(img.width * scaler, img.height * scaler)
					 img.save(filename=current_dir+'/personal/temp/temp'+str(count)+".jpg")

				print(pytesseract.image_to_string(PIL.Image.open(current_dir+'/personal/temp/temp'+str(count)+".jpg"), lang=language))
				tessaract_ocr=pytesseract.image_to_string(PIL.Image.open(current_dir+'/personal/temp/temp'+str(count)+".jpg"), lang=language)
				
				#Remove Each PDF page image 
				os.remove(current_dir+'/personal/temp/temp'+str(count)+".jpg")
				# Convert a Unicode string to a string
				unicode_contents=tessaract_ocr.decode('utf8')
				contents = unicode_contents.replace("\n", "");
				# solr insertion for book
				solr = pysolr.Solr('http://localhost:8983/solr/DocumentSearch/', timeout=10)
				solr.add([
				    {
				        "pdfid": book_id,
				        "title": book_title,
				        "author": author,
				        "year":	year,
				        "synopsis": description,
				        "page_no": currentPage ,
				        "totalpages": totalPages ,
				        "subjects": subjects,
				        "language": language,
				        "origpath": savedFileUrl,
				        "Category": document_Type ,
				        "format": "pdf",
				        "content": contents,

				    },
				])
	# result=db.insert_container(request,savedContainerUrl)
	return HttpResponseRedirect('/redirect/')
	
# show user search page 
def userSearchpage(request):
	return render(request,'personal/userSearchPage.html')
# solr search word
def userSearch(request):
	solr = pysolr.Solr('http://localhost:8983/solr/DocumentSearch/', timeout=10)

	# results = solr.search('page_no:"5"')
	searchWord=request.POST.get('searchWord')
	print searchWord
	params = {
  	  'facet': 'on',
  	  'facet_queries': {},
  	  'facet.field': 'language',
  	  'facet.field':'subjects'
	}
	results = solr.search(searchWord, **params)
	my_list = []
	# results = solr.search(searchWord)
	for result in results:
		print result
		my_list.append(result)
		
		print result['language']

	return render(request,'personal/userSearchResult.html',{'result':my_list})

#show user search Result page 
def userSearchResult(request):

    return render(request,'personal/userSearchResult.html')

def adminCollectionView(request):

    return render(request,'personal/adminCollectionView.html')
