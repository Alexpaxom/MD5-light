from django.db import models
import uuid

# Create your models here.

class FileStorage(models.Model):
	# хешь сумма файла ma5
	md5 = models.CharField(max_length=32)
	
	# указатель на файл
	file = models.FileField(upload_to='%Y-week-%W')

class UserTasks(models.Model):
	# Все возможные состояния обработки файла
	NOT_EXIST = 'NE'
	SUCCESS = 'SC'
	FAIL = "FL"
	IN_WORK = "WK"

	FILE_STATUS = (
		(NOT_EXIST, 'Not exist'),
		(SUCCESS, 'Success'),
		(FAIL, 'Fail'),
		(IN_WORK, 'In work'),
	)

	# уникальный идентификатор задачи
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	# состояние обработки
	status = models.CharField(max_length=2, choices=FILE_STATUS, default=IN_WORK)

	# email пользователя
	email = models.CharField(max_length=100)

	# указатель на файл в таблице FileStorage
	file = models.ForeignKey(FileStorage, on_delete=models.CASCADE, default=None, blank=True, null=True) 

	# ссылка на файл
	url = models.TextField()