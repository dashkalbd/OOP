Розробіть програму для роботи з банківськими рахунками.
Вимоги:
1.Створіть клас BankAccount з атрибутами власника
рахунку та балансу.
2.Реалізуйте внесення та зняття коштів. Забороніть
зняття суми, більшої за доступний баланс.
3.Зробіть баланс внутрішнім атрибутом і організуйте
доступ до нього через властивість @property.
4.Створіть класи SavingsAccount і BusinessAccount,
успадковані від BankAccount.
5.Для ощадного рахунку реалізуйте нарахування
відсотків, а для бізнес-рахунку — комісію за
операцію.
6.Перевизначте метод зняття коштів у дочірніх класах
відповідно до їхньої поведінки.
7.Реалізуйте __str__(), щоб отримувати зрозумілий опис
рахунку.

# Point 1: father class with owner and balance
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        # Point 3: balance is an internal attribute
        self._balance = balance

    # Point 3: read-only access to the balance
    @property
    def balance(self):
        return self._balance

    # Point 2: deposit money
    def add_money(self, amount):
        self._balance = self._balance + amount
        print(f"Ви додали: {amount} грн\nНовий баланс: {self._balance} грн")

    # Point 2: withdraw money, not more than the balance
    def deduct_money(self, amount):
        if amount > self._balance:
            print(f"Недостатньо коштів: {amount} грн перевищує баланс {self._balance} грн")
            return
        self._balance = self._balance - amount
        print(f"Ви зняли: {amount} грн\nНовий баланс: {self._balance} грн")

    # Point 7: readable description of the account
    def __str__(self):
        return f"Рахунок: {self.owner}, баланс: {self._balance} грн"


# Point 4: savings account inherits from BankAccount
class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        # parent saves owner and balance
        super().__init__(owner, balance)
        # own attribute: interest rate in %
        self.interest_rate = interest_rate

    # Point 5: add interest to the balance
    def add_interest(self):
        interest = self._balance * self.interest_rate / 100
        self._balance = self._balance + interest
        print(f"Нараховано відсотки: {interest} грн\nНовий баланс: {self._balance} грн")

    # Point 6: own withdraw rule - max 5000 at once
    def deduct_money(self, amount):
        if amount > 5000:
            print("З ощадного рахунку можна зняти не більше 5000 грн за раз")
            return
        # the normal withdraw from the parent does the rest
        super().deduct_money(amount)

    # Point 7: description with interest rate
    def __str__(self):
        return f"Ощадний рахунок: {self.owner}, баланс: {self._balance} грн, ставка {self.interest_rate}%"


# Point 4: business account inherits from BankAccount
class BusinessAccount(BankAccount):
    def __init__(self, owner, balance, commission):
        # parent saves owner and balance
        super().__init__(owner, balance)
        # own attribute: commission per withdrawal
        self.commission = commission

    # Point 5 + 6: withdraw takes amount plus commission
    def deduct_money(self, amount):
        total = amount + self.commission
        print(f"Комісія: {self.commission} грн")
        # the normal withdraw from the parent, with the total
        super().deduct_money(total)

    # Point 7: description with commission
    def __str__(self):
        return f"Бізнес-рахунок: {self.owner}, баланс: {self._balance} грн, комісія {self.commission} грн"


# Test: basic account
bank1 = BankAccount("Софія", 20000)
print(bank1)
bank1.add_money(500)
bank1.deduct_money(2000)

# Test: savings account
print()
savings1 = SavingsAccount("Іван", 10000, 5)
print(savings1)
savings1.add_interest()
savings1.add_money(500)
savings1.deduct_money(6000)
savings1.deduct_money(3000)

# Test: business account
print()
business1 = BusinessAccount("ТОВ Ромашка", 2000, 10)
print(business1)
business1.add_money(1000)
business1.deduct_money(500)

# Test point 3: balance can be read, but not changed directly
print()
print("Баланс до спроби:", business1.balance)

try:
    business1.balance = 1000000
except AttributeError:
    print("Помилка: змінити баланс напряму не можна")

print("Баланс після спроби:", business1.balance)