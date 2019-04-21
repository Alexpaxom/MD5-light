from django.db import models
import uuid


class UserDowndloadTasks(models.Model):
	# Все возможные состояния обработки файла
	DONE = 'DN'
	FAIL = "FL"
	RUNNING = "RN"

	FILE_STATUS = (
		(DONE, 'done'),
		(FAIL, 'fail'),
		(RUNNING, 'running'),
	)

	# уникальный идентификатор задачи
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	# состояние обработки
	status = models.CharField(max_length=2, choices=FILE_STATUS, default=RUNNING)

	# email пользователя
	email = models.CharField(max_length=100)

	# хешь сумма файла ma5
	md5 = models.CharField(max_length=32)

	# ссылка на файл
	url = models.TextField()