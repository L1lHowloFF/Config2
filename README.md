# Config2
ДЗ по конфигу


## Этап 3. Основные операции
Цель: построен граф зависимостей (с учетом транзитивности) и выполнены основные операции над ним. Требования:

Получен граф зависимостей и реализован алгоритмом BFS без рекурсии.  
Корректно обработаны случаи наличия циклических зависимостей.  
Поддержан режим тестирования. Вместо URL реального репозитория, дана возможность пользователю указать путь к файлу описания графа репозитория, где пакеты называются большими латинскими буквами. Продемонстрирована функциональность этого этапа на различных случаях работы с тестовым репозиторием.  
Результат выполнения этапа сохранен в репозиторий стандартно оформленным коммитом.

# Описание функций и настроек
## Класс DependencyGraph:
### Основные функции
__init__(self) - инициализация графа  
build_graph_bfs(self, start_package, dependency_fetcher) - построение BFS  
detect_cycles(self) - обнаружение циклов  

## Класс DependencyFetcher:
### Основные функции
__init__(self, config) - инициализация  
get_dependencies(self, package_name) - получение зависимостей  
get_dependencies_from_github(self, package_name) - из GitHub  
parse_dependencies(self, cargo_toml_content) - парсинг  

## Класс TestRepository:
### Основные функции
__init__(self, test_file_path) - инициализация  
load_test_graph(self) - загрузка тестового графа  
get_dependencies(self, package) - получение зависимостей  

## main.py функции:
### Основные функции
print_graph_info(graph, start_package) - вывод информации о графе  
main() - полная версия для всех этапов

# Примеры использования
## Реальный режим

<img width="2051" height="1293" alt="image" src="https://github.com/user-attachments/assets/60649e4b-3e6d-449a-8aab-95d11a6a80ca" />  

## Режим тестировки

<img width="2078" height="1301" alt="image" src="https://github.com/user-attachments/assets/05c0bcc6-3b81-4e2e-bbb4-452ac0b53b1a" />
