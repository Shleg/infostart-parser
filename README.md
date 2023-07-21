# Домашнее задание по семинару 1
## Выполненные действия:
- инициализирован репозиторий командой `git init` в папке с проектом парсера сайта infostart.ru, добавлены в отслеживание необходимые файлы, создан и настроен файл .gitignore
- создан файл README.md и добавлен в отслеживание командой `git add README.md`
- создан коммит перед отправкой изменений на Github `git commit -m 'Ready to push to Github'`
- создан удаленный репозиторий git-homework на GitHub с файлом README.md
- к локальному репозиторию подключен удаленный репозиторий с помощью команды `git remote add origin git@github.com:Shleg/git-homework.git`
- выполнена команда `git push -u origin main` и получена ошибка fatal: refusing to merge unrelated histories, которая говорит о том, что  Git пытается выполнить слияние двух веток, которые, по его мнению, не имеют общей истории. 
- выполнена команда `git pull origin main --allow-unrelated-histories
`. Это позволит Git объединить истории коммитов, которые ранее считались неродственными.
