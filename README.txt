Аналитический проект BA+SA
==========================

Проверенные исходные файлы
--------------------------

  Fullstack-.pdf
  Task 3. UML diagram.drawio

Состав проекта
--------------

Задание 1:

  task_1_bpmn/equipment_request_process.bpmn
  BPMN 2.0 модель процесса обработки заявки на ИТ-оборудование.

  task_1_bpmn/equipment_request_bpmn.svg
  Читаемая схема того же процесса в BPMN-стиле.

  task_1_bpmn/questions_and_assumptions.txt
  Вопросы и допущения по текущему as-is процессу.

Задание 2:

  task_2_marketplace_publication/user_story_and_use_cases.txt
  Пользовательская история, участники, варианты использования, бизнес-правила,
  поля данных и критерии приемки для публикации товара из кабинета продавца
  на витрину маркетплейса.

  task_2_marketplace_publication/publication_process.svg
  Схема процесса публикации товара.

Задание 3:

  task_3_registration_api/registration_api_openapi.yaml
  REST API описание для кнопки Register на форме регистрации пользователя.

  task_3_registration_api/backend_registration_algorithm.txt
  Подробный алгоритм backend-обработки регистрации пользователя.

  task_3_registration_api/registration_algorithm.svg
  Читаемая activity-style схема алгоритма регистрации.

  task_3_registration_api/registration_ui_cases.txt
  Интерпретация полей и ошибочных состояний по предоставленным экранам draw.io.

Проверка
--------

Из папки Analytics:

  python3 tests/validate_deliverables.py

Ожидаемый результат:

  All deliverables passed validation.

Примечание
----------

В исходном интерфейсе регистрации видны поля First Name, Last Name, UserName,
Password и CAPTCHA. Поле email на форме отсутствует, поэтому в спецификации API
username используется как уникальный идентификатор входа.
