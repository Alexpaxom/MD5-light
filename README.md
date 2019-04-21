<h4>1. Скачать проект</h4>
<h4>2. Развернуть все зависимости</h4>
<p>Для этого в терминале переходим в корневой каталог и выполняем</p>
<p>pip install -r requirements txt</p>
<p>Нам также понадобится брокер сообщений RabbitMQ. Сервер RabbitMQ должен запуститься автоматически.</p>
<p>sudo apt-get install rabbitmq-server</p>
<h4>3. Запустить django</h4>
<p>Для этого выполним команду:</p>
<p>python manage.py runserver</p>
<h4>4. Запускаем очередь заданий celery</h4>
<p>Для этого нам необходимо открыть еще одно окно терминала, и перейти в корневой каталог:</p>
<p>celery -A md5_light worker --max-tasks-per-child N -l info</p>
<p>Где N нужно заменить на количество потоков обрабатывающих очередь загрузок. Не рекомендуется в данный момент ставить больше 2, а лучше 1 т. к. мы работаем с sqlite, а она не рассчитана на это.</p>
