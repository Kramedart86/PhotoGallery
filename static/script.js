$(document).ready(function(){
    // Находим все изображения с классом "image-item"
    $(".image-item img").click(function(){
        var imgSrc = $(this).attr("src"); // Получаем путь к изображению
        $("#previewImage").attr("src", imgSrc); // Устанавливаем путь к изображению в модальном окне
        $("#imagePreviewModal").css("display", "block"); // Открываем модальное окно
    });

    // Закрываем модальное окно по клику на крестик
    $(".close").click(function(){
        $("#imagePreviewModal").css("display", "none");
    });

    // Закрываем модальное окно при нажатии на клавишу ESC
    $(document).keydown(function(e) {
        if (e.keyCode == 27) { // Код клавиши ESC
            $("#imagePreviewModal").css("display", "none");
        }
    });

    // Обработчики событий для перемещения по изображениям с помощью стрелок на клавиатуре
    $(document).keydown(function(e) {
        if ($("#imagePreviewModal").css("display") == "block") { // Проверяем, открыто ли модальное окно
            var imgSrc = $("#previewImage").attr("src"); // Получаем путь к текущему изображению
            var images = $(".image-item img"); // Находим все изображения
            var currentIndex = images.index(images.filter('[src="' + imgSrc + '"]')); // Индекс текущего изображения

            switch(e.keyCode) {
                case 37: // Стрелка влево
                    currentIndex = (currentIndex - 1 + images.length) % images.length;
                    break;
                case 39: // Стрелка вправо
                    currentIndex = (currentIndex + 1) % images.length;
                    break;
                default:
                    return; // Если нажата не стрелка влево или вправо, выходим из обработчика
            }
            var newImgSrc = $(images[currentIndex]).attr("src"); // Получаем путь к новому изображению
            $("#previewImage").attr("src", newImgSrc); // Устанавливаем путь к новому изображению в модальном окне
        }
    });
});