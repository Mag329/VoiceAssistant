<h1 align='center'>VoiceAssistant</h1>
<h2 align='center'>Голосовой ассистент на Python</h2>

### Что реализовано
| Функция | Статус |
| --- | --- |
| Управление устройствами через http | Да |
| Управление устройствами через mqtt | Нет |
| Установка таймера | Да |
| Навык рандома | Да |
| Управление через Telegram бота | Нет |
| Список покупок | Да |
| Радио | Нет |
| Сценарии умного дома | Нет |
  
[Доска Weeek](https://app.weeek.net/ws/490187/shared/board/MWJjBgMaJ1wmItv4FBOIdlRoU5UwLRVt)
<br>

### Установка
1. Клонирование репозитория
```
git clone https://github.com/Mag329/VoiceAssistant_RUTTS.git
```
2. Установка зависимостей
```
pip install -r /path/to/requirements.txt
```
3. Установите модель Vosk  
https://alphacephei.com/vosk/models
<br/><br/>
5. Распакуйте и переименуйте в `model`
<br/><br/>
6. Запуск
```
python3 main.py
```

<br>

Код распознования команд взят из [видео Хауди Хо](https://www.youtube.com/watch?v=XTeGvaDaraI)  
Реализация таймера взята из [голосового ассистента Ирина](https://github.com/janvarev/Irene-Voice-Assistant) от janvarev  
Некоторые идеи позаимствованы из голосового ассистента [Ирина](https://github.com/janvarev/Irene-Voice-Assistant) и [Васисуалий](https://github.com/Oknolaz/vasisualy/tree/master)  

### Использовано
![Python](https://img.shields.io/badge/Python-blue?style=for-the-badge)  
![Flask](https://img.shields.io/badge/Flask-lightgray?style=for-the-badge)  
![Vosk](https://img.shields.io/badge/Vosk-green?style=for-the-badge)  
![RUTTS](https://img.shields.io/badge/RUTTS-DD0031?style=for-the-badge)  
![HTML](https://img.shields.io/badge/HTML-orange?style=for-the-badge)  
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge)
