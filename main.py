  class Hesap:
    def __init__(self, hesap_turu, hesap_adi, bakiye):
        self._hesap_turu = hesap_turu
        self._hesap_adi = hesap_adi
        self.bakiye = bakiye

    @property
    def bakiye(self):
        return self.bakiye

    @bakiye.setter
    def bakiye(self, deger):
        if deger < 0:
            raise ValueError("\n>>>>>>Account balance cannot be negative.<<<<<<<<<<<")
        self.bakiye = deger

    def hesabi_kapat(self):
        raise NotImplementedError("This method must be defined in subclasses.")

class SavingAccount(Hesap):
    def hesabi_kapat(self):
        self.bakiye -= self.bakiye * 0.10
        return self.bakiye

class NormalAccount(Hesap):
    def hesabi_kapat(self):
        print(f"Hesap Adı: {self._account_name}, Bakiye: {self.bakiye}")
        return self.bakiye

class Transaction:
    def __init__(self, hesap, miktar):
        self.hesap = hesap
        self.miktar = miktar
    
    def para_dondur(self):
        return self.miktar

    @staticmethod
   
    def para_cek(func):
        def wrapper(*args, **kwargs):
            return -func(*args, **kwargs)
        return wrapper

    @staticmethod
    def para_ekle(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

def para_guncelle(hesap, transaction):
    hesap.bakiye += transaction.para_dondur()

def para_transferi(hesaplar, islem):
    try:
        hesap_adi = input("Enter the account holder name: ")
        miktar = float(input("Enter the amount to be transferred: "))
        if hesap_adi in hesaplar:
            miktar = hesaplar[hesap_adi]
            if islem == "cek":
                transaction_miktari = Transaction.para_cek(lambda: miktar)()
            elif islem == "ekle":
                transaction_miktari = Transaction.para_ekle(lambda: miktar)()
            else:
                print("Invalid transaction type.")
                return

            transaction = Transaction(miktar, transaction_miktari)
            para_guncelle(miktar, transaction)
            print(f"New Balance: {miktar.balance}")
        else:
            print("Account not found.")
    except ValueError as e:
        print(e)

def hesap_olustur(hesaplar):
    try:
        hesap_adi = input("Enter account holder name: ")
        hesap_turu = input("Enter the acoount type (Saving/Normal): ")
        miktar = float(input("Enter starting balance: "))
        if hesap_turu == "Saving":
            hesap = SavingAccount("Saving", hesap_adi, miktar)
        else:
            hesap = NormalAccount("Normal", hesap_adi, miktar)
        hesaplar[hesap_adi] = hesap
        print("Account created.")
    except ValueError as e:
        print(e)

def hesabi_kapat(hesaplar):
    hesap_adi = input("Enter the Accont Holder name: ")
    if hesap_adi in hesaplar:
        final_amount = hesaplar[hesap_adi].hesabi_kapat()
        print(f"Available balance: {final_amount}")
        del hesaplar[hesap_adi]
    else:
        print("Account not found.")

def kaydet(hesaplar):
    with open('hesaplar.txt', 'w') as f:
        for hesap_adi, hesap in hesaplar.items():
            f.write(f"{hesap_adi},{hesap._hesap_turu},{hesap.bakiye}\n")

def yukle(hesaplar):
    try:
        with open('hesaplar.txt', 'r') as f:
            for line in f:
                hesap_adi, hesap_turu, bakiye = line.strip().split(',')
                bakiye = float(bakiye)
                if hesap_turu == "Saving":
                    hesaplar[hesap_adi] = SavingAccount(hesap_turu, hesap_adi, bakiye)
                else:
                    hesaplar[hesap_adi] = NormalAccount(hesap_turu, hesap_adi, bakiye)
        print("Accounts loaded.")
    except FileNotFoundError:
        print("Log file not found.")

def hesaplari_goster(hesaplar):
    if not hesaplar:
        print("There is no registered account.")
    else:
        for hesap_adi, hesap in hesaplar.items():
            print(f"{hesap_adi} : {hesap.bakiye}")

def islem_menusu(hesaplar):
    while True:
        print("\n>>>>>>Menu<<<<<<")
        print("1.Create a Account")
        print("2. Close account.")
        print("3. Save and load")
        print("4. Money withdraw")
        print("5. Load Money")
        print("6. Show all the accounts")
        print("7. Exit")

        secim = input("Enter the choice: ")
        if secim == "1":
            hesap_olustur(hesaplar)
        elif secim == "2":
            hesabi_kapat(hesaplar)
        elif secim == "3":
            kaydet(hesaplar)
            yukle(hesaplar)
        elif secim == "4":
            para_transferi(hesaplar, "cek")
        elif secim == "5":
            para_transferi(hesaplar, "ekle")
        elif secim == "6":
            hesaplari_goster(hesaplar)
        elif secim == "7":
            break
def main():
    hesaplar = {}  # Hesapları tutmak için boş bir sözlük
    islem_menusu(hesaplar)

if __name__ == "__main__":
    main()
