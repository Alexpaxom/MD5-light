from django.shortcuts import render
from django.http import HttpResponse
#from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.core.files import File
from . import models

# Отключаем проверку csrf, для того что бы работали примеры из задания
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def calc_api(request):
	if("url" in request.POST):
		print("url:" + request.POST["url"])
		if("email" in request.POST):
			print("email:" + request.POST["email"])
	elif("id" in request.GET):
		print("id:" + request.GET["id"])

		with open('tmp/test.txt', 'r') as file:
			print(models.FileStorage.IN_WORK)
			django_file = File(file)
			file_storage = models.FileStorage()
			file_storage.md5 = ""
			file_storage.file.save("no_name1.txt", django_file)
			file_storage.status = models.FileStorage.IN_WORK

			file_storage.save()
			print("file_id: " + str(file_storage.id))
	else:
		return HttpResponseBadRequest("")

	return HttpResponse("")
