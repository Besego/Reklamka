while True:
    try:
        K = int(input("Введите число для создания таблицы умножения: "))
        break
    except ValueError:
        print("Ошибка: Введено не целое число. Пожалуйста, попробуйте снова.")

print(f"Таблица умножения для числа {K}:")
for i in range(1, 11):
    result = K * i
    print(f"{K} x {i} = {result}")