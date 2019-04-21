from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMessage
from . import models

import requests
import shutil
import hashlib
import os



@shared_task
def runDownloadTask(taskId):
	# Получаем параметры задачи
	u_task = models.UserDowndloadTasks.objects.get(pk=taskId)

	# Пытаемся скачать файл
	r = requests.get(u_task.url, stream=True)
	if r.status_code == 200:

		# Создаем временный файл, куда будем сохранять внешний файл url
		temp_file_name = settings.MEDIA_ROOT + str(u_task.id)

		with open(temp_file_name, "wb") as file:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, file)

		# Считаем MD5-hash и пишем в нашу базу
		u_task.md5 = fmd5(temp_file_name)
		u_task.status = models.UserDowndloadTasks.DONE
		u_task.save()

		# Если пользователь ввел какой-то email пробуем на него отправить сообщение
		if(u_task.email != ""):
			send_message(u_task.email, "MD5 сумма успешно посчитана!", "Ссылка на файл: "+str(u_task.url)+" md5 - " + str(u_task.md5))

		# Удаляем временный файл
		if(os.path.exists(temp_file_name)):
			os.remove(temp_file_name)

	else:
		# Если не удалось скачать файл пишем это в нашу базу
		u_task.status = models.UserDowndloadTasks.FAIL
		u_task.save()


def fmd5(file_name):
	hash_md5 = hashlib.md5()
	with open(file_name, "rb") as f:
		for chunk in iter(lambda: f.read(settings.SIZE_CHANKS_FOR_HASHING), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def send_message(email, sub, body):
	mail = EmailMessage(sub, body, to=[email])
	mail.send(fail_silently=True)
