# 🍆 BattleCode

# Навигация
1. [Start](#start)
2. [Установка WSL](#установка-wsl)
3. [Docker Desktop](#установка-docker-desktop)
4. [](#установка-visual-studio-code)


## Start


 1. [WSL](https://learn.microsoft.com/ru-ru/windows/wsl/install)
 2. Установить `python-pip` --> `pipx` --> `uv` & `ruff`
 3. Установить [Docker Desktop](https://www.docker.com/products/docker-desktop/)
 4. Установить [Visual Studio Code](https://code.visualstudio.com/)


 ## Установка WSL


### 1. В терминале винды от имени админа:

 ```bash
 wsl --install Ubuntu-24.04
 ```
После установки нужно будет ввести имя пользователя и пароль, *пароль нужно запомнить*

### 2. Обновление
Выполнить эту команду в терминале WSL для обновления системы:
```bash
sudo apt update && sudo apt upgrade
```



## Установка Python

### 1. Установка **Python3.12**
Нам нужно установить python версии 3.12

```bash
sudo apt install python3.12

```


### 2. Установка **PIP**
Для установки стандартного менеджера пакетов 
```bash
sudo apt -y install python3-pip
```

### 3. Установка **uv** и **ruff**
#### Устанока менеджера пакетов uv и линтера ruff

Через pipx
```bash

sudo apt update
sudo apt install pipx
pipx ensurepath
```

#### Установка uv & ruff
```bash
# install uv
pipx install uv

# update uv
uv self update

# enable shell autocompletion

echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc

# install ruff via uv
uv tool install ruff@latest
```


## Установка Docker Desktop
Нужно зайти на сайт Docker и нажать по кнопке *Скачать AMD64 версию*


[Прямая ссылка](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module)


## Установка Visual Studio Code
Почему нужно юзать vsc: [\*видео\*](https://youtu.be/oyB9YWMEq8Y?si=NNDoWuS5bHmyRj_V)


### Полезные плагины для VSC
+ [WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
Для поддержки WSL


+ [Windsurf Plugin (Codeium)](https://marketplace.visualstudio.com/items?itemName=Codeium.codeium)
Ai-помощник

+ [САМАЯ ЛУЧШАЯ ТЕМА TOKYO NIGHT](https://marketplace.visualstudio.com/items?itemName=enkia.tokyo-night)

+ [Django](https://marketplace.visualstudio.com/items?itemName=batisteo.vscode-django)
Плагин для подсказки template-функций для Django html



