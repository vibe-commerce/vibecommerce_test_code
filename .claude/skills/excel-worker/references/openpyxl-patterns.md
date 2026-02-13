# openpyxl: паттерны и справочник

## Форматирование

### Шрифты

```python
from openpyxl.styles import Font

cell.font = Font(bold=True)                          # жирный
cell.font = Font(size=14, bold=True)                  # заголовок
cell.font = Font(color='FF0000')                      # красный текст
cell.font = Font(name='Arial', size=11)               # шрифт и размер
```

### Заливка

```python
from openpyxl.styles import PatternFill

cell.fill = PatternFill('solid', fgColor='FFFF00')    # жёлтый фон
cell.fill = PatternFill('solid', fgColor='D9E1F2')    # светло-голубой
cell.fill = PatternFill('solid', fgColor='E2EFDA')    # светло-зелёный
```

### Выравнивание

```python
from openpyxl.styles import Alignment

cell.alignment = Alignment(horizontal='center', vertical='center')
cell.alignment = Alignment(wrap_text=True)             # перенос текста
```

### Границы

```python
from openpyxl.styles import Border, Side

thin = Side(style='thin')
cell.border = Border(top=thin, bottom=thin, left=thin, right=thin)
```

### Ширина колонок и высота строк

```python
ws.column_dimensions['A'].width = 15
ws.column_dimensions['B'].width = 30
ws.row_dimensions[1].height = 25       # высота строки заголовка
```

### Автоподбор ширины (приблизительный)

```python
for col in ws.columns:
    max_length = 0
    col_letter = col[0].column_letter
    for cell in col:
        if cell.value:
            max_length = max(max_length, len(str(cell.value)))
    ws.column_dimensions[col_letter].width = min(max_length + 2, 50)
```

## Числовые форматы

```python
cell.number_format = '#,##0'           # 1 234
cell.number_format = '#,##0.00'        # 1 234.56
cell.number_format = '0.0%'            # 15.3%
cell.number_format = 'YYYY-MM-DD'      # 2026-02-12
cell.number_format = 'DD.MM.YYYY'      # 12.02.2026
cell.number_format = '#,##0 ₽'        # 1 234 ₽
cell.number_format = '$#,##0'          # $1,234
cell.number_format = '@'               # текст (для ID, артикулов)
```

## Работа с листами

```python
wb = load_workbook('file.xlsx')

# Список листов
print(wb.sheetnames)  # ['Sheet1', 'Sheet2']

# Выбор листа
ws = wb['Sheet1']
ws = wb.active

# Создание нового листа
ws_new = wb.create_sheet('Итого')
ws_new = wb.create_sheet('Первый', 0)  # вставить в начало

# Копирование листа
ws_copy = wb.copy_worksheet(wb['Sheet1'])

# Удаление листа
del wb['Sheet2']

# Переименование
ws.title = 'Новое имя'
```

## Работа с диапазонами

```python
# Объединение ячеек
ws.merge_cells('A1:D1')
ws.unmerge_cells('A1:D1')

# Заморозка строк/колонок (аналог Freeze Panes)
ws.freeze_panes = 'A2'    # заморозить первую строку
ws.freeze_panes = 'B1'    # заморозить первую колонку
ws.freeze_panes = 'B2'    # заморозить и строку, и колонку

# Автофильтр
ws.auto_filter.ref = 'A1:E100'
```

## Формулы: частые паттерны

```python
# Сумма
ws['B10'] = '=SUM(B2:B9)'

# Среднее
ws['C10'] = '=AVERAGE(C2:C9)'

# Условная сумма
ws['D10'] = '=SUMIF(A2:A9,"DONE",D2:D9)'

# Подсчёт
ws['E10'] = '=COUNTA(E2:E9)'
ws['F10'] = '=COUNTIF(F2:F9,">0")'

# Процент
ws['G2'] = '=F2/E2'  # + number_format = '0.0%'

# Ссылка на другой лист
ws['A1'] = "='Лист2'!B5"

# ЕСЛИ
ws['H2'] = '=IF(G2>0.1,"Рост","Падение")'

# ВПР (VLOOKUP)
ws['I2'] = '=VLOOKUP(A2,Справочник!A:C,3,FALSE)'
```

## Известные ограничения openpyxl

openpyxl при открытии и сохранении файла может **безвозвратно повредить**:

| Элемент | Риск | Что делать |
|---------|------|-----------|
| VBA макросы | Теряются при `.xlsx` | Использовать `keep_vba=True`, сохранять как `.xlsm` |
| Графики (charts) | Могут исчезнуть | Предупредить пользователя, работать с копией |
| Изображения/shapes | Теряются при save | Предупредить, НЕ сохранять файл с картинками |
| Pivot tables | Становятся невалидными | Только чтение, не модифицировать |
| Условное форматирование | Частичная поддержка | Проверять после сохранения |
| Внешние ссылки | Могут сломаться | Проверять перед и после |
| Именованные диапазоны | Могут повредиться | Осторожно с INDEX/MATCH |
| Комментарии | Проблемы при повторном save | Минимизировать операции save |
| Формат `.xls` | НЕ поддерживается | Конвертировать в `.xlsx` сначала |

### Рекомендация при сложных файлах

```python
# Проверить перед модификацией
wb = load_workbook('file.xlsx')
has_charts = any(ws._charts for ws in wb.worksheets)
has_images = any(ws._images for ws in wb.worksheets)
is_macro = str(wb.path or '').endswith('.xlsm')

if has_charts or has_images:
    print("ВНИМАНИЕ: файл содержит графики/изображения, openpyxl может их потерять")
```

## Частые ошибки формул

| Ошибка | Причина | Исправление |
|--------|---------|-------------|
| `#REF!` | Невалидная ссылка на ячейку | Проверить что ячейка существует |
| `#DIV/0!` | Деление на ноль | Добавить `=IF(B2=0,0,A2/B2)` |
| `#VALUE!` | Неверный тип данных в формуле | Проверить типы ячеек |
| `#N/A` | Значение не найдено (VLOOKUP) | Обернуть в `IFERROR` |
| `#NAME?` | Нераспознанное имя формулы | Проверить написание функции |

### Защитный паттерн

```python
# Безопасное деление
ws['C2'] = '=IF(B2=0,0,A2/B2)'

# VLOOKUP с обработкой ошибки
ws['D2'] = '=IFERROR(VLOOKUP(A2,Ref!A:B,2,FALSE),"")'
```

## Большие файлы

```python
# Чтение — read_only режим (экономит память)
wb = load_workbook('big_file.xlsx', read_only=True)
for row in ws.iter_rows(values_only=True):
    process(row)
wb.close()  # обязательно закрыть

# Запись — write_only режим
wb = Workbook(write_only=True)
ws = wb.create_sheet()
for data in large_dataset:
    ws.append(data)
wb.save('output.xlsx')
```
