

# <div align="center">Простая Онлайн Галерея (ПОГ) <img src="https://github.com/Kramedart86/PhotoGallery/assets/111295359/526b98d8-5ab6-4c73-b5c4-daf55ff7ee91" width="75" height="50"></div>

## <div align="center">Описание</div>

Проект "онлайн фотогалерея", который в дальнейшем можно будет легко расширить и улучшить. 

>  _В проекте применялся следующий стек: python, html, css, js, sqlite3, flask_

На сайте есть возможность добавления изображений, прохождение по некоторым в превью режиме при помощи стрелок на клавиатуре, выход из модульного окна как через `Х` в верхнем правом углу, так и через клавишу `ESC` или по нажатию `ЛКМ` вне модального окна. 

Но не смотря на отсутствие удаления определенного изображения, есть функция очистки всей галереи. 
Это также демонстрирует возможность взаимодействия с базой данных: вставка и получение объекта из бд, а также удаление всех объектов из таблицы.
Имеется также внутренний счетчик, который показывает, сколько изображений было загружено в базу данных галлереи (посмотреть можно, например, через DB Browser).

В целом, при создании этого проекта возникли сложности с отображением изображений, особенно при добавлении одинаковых по названию, на главной странице после добавления, их выравниванием и форматом. Но добавленные изображения хранятся как локально, так и в самой бд.
Создание модульного окна добавления изображения вместо отдельной страницы прошло успешно. Однако добавить картинку как фон, или иконку вкладки не получилось. Зато удалось подбрать стиль для кнопок. Так же описание, которое является не обязательным раньше тоже отображалось на главной, но если текст был более ~20 символов, оно выходило за ячейку и накладывалось на описание другой картинки в ряд. Поэтому фича осталась для возможного допиливания, но убрана возможность увидеть текст.

Сама структура проекта выглядит следующим образом:

      PhotoGallery/
      ├── app.py
      ├── account.db
      ├── static/
          ├── images/
          ├── header3.jpg
          ├── icon.png
          ├── script.js
          └── styles.css
      └── templates/
          └── index.html
      └── requirements.txt


**ШАГИ:** 
1. Запустить командную строку/терминал от имени администратора.
2. Перейти к папке проекта
3. **(Для Windows)** необходимо ввести Set-ExecutionPolicy unrestricted и набрать `y`, если надо подтвердить
4. Создать виртуальное окружение командой `py -m venv venv` (Если команда `py` не распознаётся, нужно использовать `python`)
<details> 
  <summary>(для Windows)</summary>
     5. Активировать окружение через команду venv\Scripts\Activate.ps1 
</details>
<details> 
  <summary>(для Linux)</summary>
    5. Активировать окружение через команду venv\bin\activate
</details>

6. Установить библиотеки и зависимости через `pip install -r requirements.txt`
7. Выполнить команду `py app.py` (или `flask run --host=0.0.0.0`   Это позволит серверу принимать запросы не только с локальной машины, но и с других устройств локальной сети.)
8. Далее проверять работу на `localhost:5000` или по ip устройства (например, `<ваш_ip:5000>`). Логин и пароль админа и модератора для проверки прав: `admin / admin`, `user / user`. Для проверки обычных прав можно зарегистрировать своего пользователя.

> Чтобы выйти из виртуального окружения, наберите команду `deactivate`.

> #

## [30-04-2024] Список изменений (v 0.7.3):
* Исправлен overlay: на главном экране вновь можно удалять свои изображения
* Анимации: Шапка сайта теперь опускается до нужного уровня независимо от разрешения экрана
* Дизайн: обновлено модульное окно добавление изображения. Теперь есть возможность также перенести изображение в окно и добавить его

## [27-04-2024] Список изменений (v 0.7.0):
**Были тяжёлые дни, я наконец-то вышел из запоя и взялся вновь за работу. А впереди ещё праздничные выходные. Поэтому перед ними выкатывается проработанный проект со множеством изменений.** 
* Дизайн: появилось сайдбар меню
* Дизайн: отображение имени автора и названия изображения, которое автор мог написать при добавлении изображения
* Дизайн: изменен внешний вид сетки изображений
* Дизайн: изменен внешний вид модального окна изображения
* Дизайн: цвет акцента кнопок авторизации изменился на зелёный
* Анимации: При уменьшеной ширине экрана все основные элементы (добавление, удаление, очистка, поиск, меню профиля) переносятся в сайдбар меню
* Анимации: изменение поведения шапки. При скролле страницы она опускается до начала надписи "Простая Онлайн Галерея". Так основные элементы будут отображаться и при этом экономить основной контент
* Появился профиль для каждого пользователя, с возможностью просмотра личных изображений
* Появилось затеменение изображений при наведении
* Добавлена возможность просмотреть только изображения профиля
* Добавлена кнопка удаления всех пользовательских изображений. Это не то же самое, что очистка всей галереи (доступна только для админа)
* Поиск: теперь можно искать изображения и по названию, и по имени автора
* Мелкие изменения в футере: появилась ссылка на github проект
* Удалена база данных с изображениями. Теперь в базе account.db есть две необходимые таблицы: users и images

# <div align="center">Демонстрация проекта (v 0.7.0)</div>
### Поведение шапки сайта при скроллинге
https://github.com/Kramedart86/PhotoGallery/assets/111295359/9dad833e-506b-4c4d-8643-4eba6caffddb

### Нивигационная панель
https://github.com/Kramedart86/PhotoGallery/assets/111295359/4a9bd99c-0f02-475f-a5c1-5f95d0bfb601

### Описание изображений
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/e61c8b68-294f-41ce-bb9a-cd4ca2ab19c8)


### Профиль
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/aed86183-ddf1-4102-bbf5-d7947f4d4463)


## [21-04-2024] Список изменений (v 0.6.0):
* Заголовок теперь является кликабельным
* Добавлен поиск изображений по названию (описанию)
* В результатах поиска поведение модального окна (превью) точно такое же, как и на главной странице


# <div align="center">Скриншоты проекта (v 0.6.0)</div>
### Шапка главной страницы (гость)
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/31171765-c3ab-4d61-b38b-f13464136cc8)


## [21-04-2024] Список изменений (v 0.5.7):
* Добавлен выход по клику вне области модального окна для предпросмотрщика изображений
* Появилась возможность добавлять своё название изображения
* Теперь название отображается над изображением


## [20-04-2024] Список изменений (v 0.5.5):
* Добавлен шрифт Fira Code как основной


## [20-04-2024] Список изменений (v 0.5.4):
* Исправлена высота шапки сайта
* Изменен размер шрифта и положение приветственного сообщения
* Исправлено именование уже существующих файлов: счётчик приписывается к имени существующего файла в скобках
* Из `requirements.txt` убраны лишние зависимости


## [19-04-2024] Список изменений (v 0.5.0):
* Зафиксирована шапка сайта. Теперь при скролле она будет оставаться на месте
* Легкие изменения в дизайне скроллбара. Вместо дефолтного стиля теперь кастомный
* Изменен дизайн кнопок авторизации
* Дизайн кнопок подогнан под единый стиль цветов
* Мелкое изменение в дизайне модальных окон добавления изображения и авторизации
* Исправлено именование уже существующих файлов: счётчик приписывается к имени существующего файла корректно, не увеличивая длину имени
* Исправлено отображение изображений при попытке авторизоваться некорректным/несуществующим пользователем
* Поля регистрации `Имя пользователя` и  `пароль` теперь имеют обязательный атрибут - минимум 4 символа
* Мелкая оптимизация кода


# <div align="center">Скриншоты проекта (v 0.5.0)</div>

### Шапка страницы (гость)
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/5d75aaf5-6575-46e2-9ca4-1e7ba3478c93)

### Модульное окно входа (для регистрации аналогично)
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/47e4c7c3-b139-4527-a3d3-47d950d8aea9)

### Модульное окно добавления изображения
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/88f197b4-99d0-49f2-9d3f-0910fcdac7cc)


## [16-04-2024] Список изменений (v 0.4.2):
* Доработан дизайн
* Изменены модальные окна: авторизации, добавления изображения
* Добавлена возможность авторизации (регистрация, вход и выход из пользователя)
* Добавлена новая база данных для хранения имени и пароля пользователей
* Все пароли хранятся в зашифрованном виде
* Лёгкая оптимизация кода

# <div align="center">Скриншоты проекта (v 0.4.2)</div>

### Главная страница (гость)
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/b14dd9aa-b9ba-4ce1-b625-60036b7864dc)

### Главная страница (залогин)
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/b5a357fd-71c9-41a5-89bc-859a49b87add)

### Модульное окно входа
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/d31defe6-9062-4d0d-9c39-c971eba0f5be)

### Модульное окно регистрации
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/29f055d2-5da7-4777-932c-8805b58eeca5)

### Модульное окно добавления изображения 
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/df240f98-3c6e-47b1-be0a-c98099bcd59c)


## [15-04-2024] Список изменений (v 0.3.3):
* Исправлена ошибка, при которой в 3-м ряду у изображений не отображалась корректно кнопка `удалить`
* Исправлен цвет текста в шапке сайта


## [14-04-2024] Список изменений (v 0.3.1):
* Изменена шапка сайта
* Мелкое исправление кнопки `Добавить`
* В проект добавлен `requirements.txt` для установки необходимых библиотек и зависимостей

# <div align="center">Скриншоты проекта (v 0.3.1)</div>

### Шапка главной страницы
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/3a4ba064-ca90-4e29-ab7e-fccfb2d94081)


## [13-04-2024] Список изменений (v 0.3.0):
* Футер страницы теперь расположен внизу, а не закреплен за местом изображений
* Исправлена ошибка, при которой не удалялись два одинаковых изображения из бд и из папки `images/`
* Переход проекта в стадию beta


## [13-04-2024] Список изменений (v 0.2.5):
* Доработан дизайн
* Добавлен кастомный фавикон (иконка вкладки)
* Добавлена возможность удалять любые изображения, как из базы данных, так из папки images/
* При удалении любого изображения выскакивает предупреждающее окно, а не только при очистки всей галереи
* Исправлено, теперь при очистке всей галереи изображения удаляются из папки images/, а не только из базы данных
* Исправлен переключатель изображений в режиме модального окна - итерация происходит по всем изображениям в правильном порядке
* При добавлении изображения с уже существующим именем к названию добавляется уникальный id

_Не смотря на то, что удалось добавлять два одинаковых изображения, удаление одного из них ломает похожее(ие) изображение(я). Помогает полная очистка галереи._ :(


# <div align="center">Скриншоты проекта (v 0.2.5)</div>

### Главная страница
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/62af566f-4785-49c4-a7d9-70bc9165b9df)

### Иконка вкладки
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/73058bdc-8762-4178-a6a1-a4836d8779af)


## [12-04-2024] Список изменений (v 0.2.0):
* Обновлен дизайн проекта
* Исправлено отображение фоновой картинки в шапке сайта

# <div align="center">Скриншоты проекта (v 0.2.0)</div>

### Главная страница
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/013f1794-a9a4-4eb9-b9ad-c590039b4c8f)

### Модульное окно добавление изображения 
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/7a71261a-5b97-496e-8469-ffa394aaf89c)


## [10-04-2024] Список изменений (v 0.1.0):
* Добавлена кнопка "Очистить галерею"
* Добавлено модульное окно просмотра изображений
* Теперь имеется фоновый цвет вместо "голой" страницы

# <div align="center">Скриншоты проекта (v 0.1.0)</div>

### Главная страница
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/8c580699-1488-4a7f-9c51-25aa73f5daa0)

### Модульное окно добавление изображения 
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/e6adeb5e-1c46-4e00-a635-459ece9769dd)

### Модульное окно просмотра изображения

![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/46d166dd-ed26-4e25-bc3c-c46b2c801b99)
