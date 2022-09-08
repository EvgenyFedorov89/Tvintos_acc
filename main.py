import input_data
import output_data
import inventory
import balance
import powders
import production


# Исходные данные по составам смесей (константы)
TV04_composition = {'WC': 0.893, 'Co': 0.1, 'Cr3C2': 0.007}
TV05_composition = {'WC': 0.913, 'Co': 0.08, 'Cr3C2': 0.007}


# Вызов функций ввода данных и сохранение их результатов в переменные
date = input_data.date_input('Введите дату: ')          # Дата внесения данных (str)
components_got = input_data.from_warehouse_input()      
WC = components_got['WC']                               # Количество WC, принятого со склада (float)
Co = components_got['Co']                               # Количество Co, принятого со склада (float)
Cr3C2 = components_got['Cr3C2']                         # Количество Cr3C2, принятого со склада (float)
TV04 = input_data.TV04_made_input()                     # Количество смеси TV04, запущенной в работу (float)
TV05 = input_data.TV05_made_input()                     # Количество смеси TV05, запущенной в работу (float)
pressing = input_data.pressing_input()                  # Перечень и количество напрессованных деталей (dict)
verification = input_data.verification_input()          # Перечень и количество забракованных деталей (dict)
to_warehouse = input_data.to_warehouse_input()          # Перечень и количество сданных на склад деталей (dict)


# Вызов функций обновления базы данных
output_data.write_from_warehouse(date, WC, Co, Cr3C2)   # Вносим кол-во полученных со склада материалов в таблицу 'from_warehouse'
output_data.write_milling(date, TV04, TV05)             # Вносим кол-во запущенных смесей в таблицу 'milling' 
output_data.write_components(date, TV04, TV05, TV04_composition, TV05_composition) # Вносим кол-во израсх. комп. в таб. 'components'
output_data.write_pressing(date, pressing)              # Вносим кол-во напрессованных деталей в таблицу 'pressing'
output_data.write_verification(date, verification)      # Вносим кол-во забракованных деталей в таблицу 'verification'
output_data.write_warehouse(date, to_warehouse)         # Вносим кол-во сданных на склад деталей в таблицу 'to_warehouse'


# Вызов функции инвентаризации
inventory.to_inventory_tables()

