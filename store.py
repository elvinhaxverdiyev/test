import random
import json
from datetime import datetime
from filter import filter_by_cake_type, filter_by_price_range, filtered_by_start_with_letter
from creat_qr import create_stock_qr_code

class Store:
    def __init__(self, name, since):
        self.name = name
        self.since = since
        self.kassa = 0
        self.sales = []
        self.product_reviews = {} 
        try:
            with open("cakes.json", "r", encoding="utf-8") as json_file:
                self.stock = json.load(json_file)
        except FileNotFoundError:
            print("Tortlar uçun 'cakes.json' fayli tapilmadi.")
            self.stock = {}
        except json.JSONDecodeError:
            print("Tortlarin melumatlarini oxuyarken xeta bas verdi.")
            self.stock = {}
        except Exception as e:
            print(f"Fayl oxumaqda xeta bas verdi: {e}")
            self.stock = {}


    def show_stock(self):
        """Stock-u ekrana yazir"""
        if not self.stock:
            print("Stockda hec bir mehsul yoxdur.")
            return
        print("Stockdaki mehsullar:")
        print("-" * 30)
        for cake, price in self.stock.items():
            print(f"{cake}: {price} AZN")
        print("-" * 30)

    def generate_stock_qr(self):
        """Stock melumatlarini QR kod olaraq yaradir"""
        create_stock_qr_code(self.stock)

    def sell_item(self, customer, item_name, count=1):
        """Satilan mehsulu kassa və musteri balansini yenileyir"""
        try:
            if item_name in self.stock:
                price = self.stock[item_name]
                total_price = price * count
                if customer.balance >= total_price:
                    # Musteri balansı yeterincedirse
                    customer.balance -= total_price
                    self.kassa += total_price
                    self.sales.append(f"{customer.name} {count} dene {item_name} aldi, toplam: {total_price} AZN")
                    customer.purchase_history.append(f"{item_name} - {total_price} AZN")
                    print(f"{customer.name} {count} dene {item_name} aldi. Total: {total_price} AZN")
                else:
                    print(f"{customer.name}, yetersiz balans.")
            else:
                print(f"{item_name} stockda yoxdur.")
        except Exception as e:
            print(f"Satis emeliyyati zamani xeta bas verdi: {e}")

    def show_kassa(self):
        """Kassa məblegini ekranda gosterir"""
        print(f"Kassadaki toplam gelir: {self.kassa} AZN")

    def save_sales_to_file(self):
        """Satislari fayla yazir"""
        try:
            with open("sales_report.txt", "w", encoding="utf-8") as file:
                file.write("Satis raportu:\n")
                file.write("-" * 40 + "\n")
                for sale in self.sales:
                    file.write(sale + "\n")
                file.write("-" * 40 + "\n")
                file.write(f"Kassaya gelen toplam gelir: {self.kassa} AZN\n")
            print("Satislar bu fayla qeyd edildi -> 'sales_report.txt'.")
        except Exception as e:
            print(f"Satis melumatlarini fayla yazarken xeta bas verdi: {e}")

    def show_filtered_cakes(self, cake_type=None, min_price=None, max_price=None, start_letter=None):
        """Tortlari filterleyen funksiya"""
        filtered_cakes = self.stock

        if cake_type:
            # Tort novu ile filtr etmek
            filtered_cakes = filter_by_cake_type(filtered_cakes, cake_type)
            print(f"\n{cake_type.capitalize()} Cakes:")

        if min_price is not None and max_price is not None:
            # Qiymete gore filtr etmek
            filtered_cakes = filter_by_price_range(filtered_cakes, min_price, max_price)
            print(f"\nBu araliqdaki tortlar {min_price} ve {max_price} AZN:")

        if start_letter:
            # İlk herf ile filtr etmek
            filtered_cakes = filtered_by_start_with_letter(filtered_cakes, start_letter)
            print(f"\nBaslayan herfi '{start_letter.upper()}' olan tortlar:")

        if not filtered_cakes:
            print("Uygun tort tapilmadi.")
            return

        for cake, price in filtered_cakes.items():
            print(f"{cake}: {price} AZN")
    
    def add_review(self, product_name, rating, review_text):
        """Mehsul ucun rey elave edir"""
        try:
            if product_name not in self.stock:
                raise ValueError(f"{product_name} magazada movcud deyil!")
            
            if not (1 <= rating <= 5):
                raise ValueError("Deyerlendirme 1-den 5-e qeder olmalidir.")
            
            # Mehsulun reyleri ile elaqeli melumatı elave edirik
            if product_name not in self.product_reviews:
                self.product_reviews[product_name] = []
            self.product_reviews[product_name].append({"rating": rating, "review": review_text})
            print(f"{product_name} ucun rey ve qiymetlendirme elave edildi.")
        
        except ValueError as e:
            print(f"Xəta: {e}")  # Deyer səhvlerini idare edir
        except Exception as e:
            print(f"Xəta bas verdi: {e}")  # Ümumi sehvler

    def show_reviews(self, product_name):
        """Mehsul ucun olan reyleri gosterir"""
        try:
            if product_name not in self.product_reviews:
                raise ValueError(f"{product_name} ucun hec bir rey yoxdur.")
            print(f"{product_name} ucun olan reyler:")
            for review in self.product_reviews[product_name]:
                print(f"Rating: {review['rating']} | Review: {review['review']}")
        except ValueError as e:
            print(f"Xeta: {e}")
        except Exception as e:
            print(f"Xeta bas verdi: {e}")
