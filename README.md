![pog](https://github.com/Kramedart86/PhotoGallery/assets/111295359/526b98d8-5ab6-4c73-b5c4-daf55ff7ee91)
# Простая Онлайн Галлерея (ПОГ)

## Описание

Это проект онлайн-фотогаллереи, который в дальнейшем можно будет легко расширить и улучшить. 

>  _В проекте применялся следующий стек: python, html, css, js, jquery, sqlite3_

На сайте есть возможность добавления изображений, прохождение по некоторым при помощи стрелок на клавиатуре, выход из модульного окна как через кнопку `Х` в верхнем правом углу, так и через клавишу `ESC` или по нажатию `ЛКМ` вне модального окна. 

Но не смотря на отсутствие удаления определенного изображений, есть функция очистки всей галлереи. 
Это также демонстрирует возможность взаимодействия с базой данных: вставка и получение объекта из бд, а также удаление всех объектов из таблицы.
Имеется также внутренний счетчик, который показывает, сколько изображений было загружено в базу данных галлереи (посмотреть можно в самой бд, например через DB Browser).

В целом, при создании этого проекта возникали сложности с отображением изображений на главной странице после добавления, их выравниванием и форматом. 
Создание модульного окна добавления изображения вместо отдельной страницы прошло более-менее успешно. Однако добавить картинку на фон не получилось. Удалось достичь эффекта затемнения и подборку нужного стиля для кнопок. Так же описание, которое является не обязательным раньше тоже отображалось на главной, но если текст был более ~20 символов, оно выходило за ячейку и накладывалось на описание другой картинки в ряд. Поэтому фича осталась для возможного допиливания, но убрана возможность увидеть текст.

Все добавленные изображения хранятся локально. Если добавить несколько изображений с одинаковыми именами, то они не будут добавлены в локальное хранилище.

Сама структура проекта выглядит следующим образом:

      PhotoGallery/
      │
      ├── app.py
      ├── gallery.db
      ├── static/
      │   ├── images/
      │   ├── header2.png
      │   ├── script.js
      │   └── styles.css
      └── templates/
          └── index.html

## [12-04-2024] Список изменений:
* Обновлен дизайн проекта
* Исправлено отображение фоновой картинки в шапке сайта

# Скриншоты проекта (v 0.1.0)

### Главная страница
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/8c580699-1488-4a7f-9c51-25aa73f5daa0)

### Модульное окно добавление изображения 
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/e6adeb5e-1c46-4e00-a635-459ece9769dd)

### Модульное окно просмотра изображения

![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/46d166dd-ed26-4e25-bc3c-c46b2c801b99)

# Скриншоты проекта (v 0.2.0)

### Главная страница
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/013f1794-a9a4-4eb9-b9ad-c590039b4c8f)

### Модульное окно добавление изображения 
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/7a71261a-5b97-496e-8469-ffa394aaf89c)


## [13-04-2024] Список изменений:
* Доработан дизайн
* Добавлен кастомный фавикон (иконка вкладки)
* Добавлена возможность удалять любые изображения, как из базы данных, так из папки images/
* При удалении любого изображения выскакивает предупреждающее окно, а не только при очистки всей галереи
* Исправлено, теперь при очистке всей галереи изображения удаляются из папки images/, а не только из базы данных
* Исправлен переключатель изображений в режиме модального окна - итерация происходит по всем изображениям в правильном порядке

# Скриншоты проекта (v 0.2.5)

### Главная страница
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/62af566f-4785-49c4-a7d9-70bc9165b9df)

### Иконка вкладки
![image](https://github.com/Kramedart86/PhotoGallery/assets/111295359/73058bdc-8762-4178-a6a1-a4836d8779af)

