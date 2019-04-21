from django.http import JsonResponse
from . import models
from . import tasks

import uuid

# Отключаем проверку csrf, для того что бы работали примеры из задания
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def calc_md5(request):
	if("url" in request.POST):
		try:
			response = processCalcMD5(request.POST)
		except Exception:
			return JsonResponse({"message":"Internal server error!"}, status=500)
		else:
			return JsonResponse(response)
	else:
		return  JsonResponse({"message":"Bad request!"}, status=400)

@csrf_exempt
def get_status(request):
	if("id" in request.GET):
		try:
			response = processGetStatus(request.GET["id"])
		except Exception:
			return JsonResponse({"message":"Internal server error!"}, status=500)
		else:
			return JsonResponse(response)
	else:
		return JsonResponse({"message":"Bad request!"}, status=400)


def processCalcMD5(params):
	# Проверяем задал ли пользователь email
	u_email = ''
	if("email" in params):
		u_email = str(params["email"])
		print("email:" + params["email"])		
	
	# Добавляем задачу в БД
	u_task = models.UserDowndloadTasks(email=u_email, url=params["url"])
	u_task.save()

	# Добавляем задачу в очередь на обработку (celery)
	tasks.runDownloadTask.delay(u_task.id)
	
	return {"id":str(u_task.id)}

def processGetStatus(task_id):
	response = {"status":"undefined" }

	# Проверяем на валидность id
	if( validate_uuid4(task_id) ):
		task_uuid = uuid.UUID(task_id, version=4)
		
		# Ищем есть ли задача с таким id
		u_task = models.UserDowndloadTasks.objects.filter(pk=task_uuid)

		if(u_task):
			u_task = u_task[0]
			response["status"] = u_task.get_status_display()
			if(u_task.status == models.UserDowndloadTasks.DONE):
				response["url"] = u_task.url
				response["md5"] = u_task.md5
	return response


def validate_uuid4(str_uuid4):
	try:
		val_uuid = uuid.UUID(str_uuid4, version=4)
	except ValueError:
		return False

	return str(val_uuid) == str_uuid4