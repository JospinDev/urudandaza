import json
import os
from datetime import datetime

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {'products': [], 'sales': []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def kubika(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def rondeza_ikidandaza(data, name):
    return next((p for p in data['products'] if p['izina'].lower() == name.lower()), None)

def afisha_ibidandaza(data):
    if not data['products']:
        print("Nta bidandazwa bihari.")
        return
    for p in data['products']:
        print(f"{p['id']:>3} | {p['izina']:<15} | {p['igiciro']:,} Fbu | {p['igitigiri']}")

def gushiramwo_ikidandazwa(data):
    izina = input("Izina ry'ikidandazwa: ").strip()
    if rondeza_ikidandaza(data, izina):
        print("Ico kidandazwa kiramaze kubaho.")
        return
    try:
        igiciro = int(input("Igiciro: "))
        igitigiri = int(input("Igitigiri: "))
        new_id = len(data['products']) + 1
        data['products'].append({
            'id': new_id,
            'izina': izina,
            'igiciro': igiciro,
            'igitigiri': igitigiri
        })
        kubika(data)
        print("Kidandazwa cashizweho.")
    except ValueError:
        print("Injiza imibare y'ukuri.")

def gufuta_ikidandazwa(data):
    afisha_ibidandaza(data)
    try:
        pid = int(input("Id y'ikidandazwa ushaka gukura: "))
        data['products'] = [p for p in data['products'] if p['id'] != pid]
        kubika(data)
        print("Kidandazwa cakuweho.")
    except ValueError:
        print("Id siyo.")

def update_product(data):
    afisha_ibidandaza(data)
    try:
        pid = int(input("Id ushaka guhindura: "))
        for p in data['products']:
            if p['id'] == pid:
                izina = input("Izina rishasha: ").strip()
                if izina and rondeza_ikidandaza(data, izina) and p['izina'].lower() != izina.lower():
                    print("Izina rirakoreshejwe.")
                    return
                igiciro = int(input("Igiciro gishasha: "))
                igitigiri = int(input("Igitigiri gishasha: "))
                p['izina'] = izina
                p['igiciro'] = igiciro
                p['igitigiri'] = igitigiri
                kubika(data)
                print("Kidandazwa cahahinduwe.")
                return
        print("Id ntibonywe.")
    except ValueError:
        print("Injiza id y'ukuri.")

def kugurisha_ikidandazwa(data):
    afisha_ibidandaza(data)
    try:
        pid = int(input("Id y'ikidandazwa: "))
        quantity = int(input("Igitigiri: "))
        for p in data['products']:
            if p['id'] == pid:
                if p['igitigiri'] < quantity:
                    print("Nta gitigiri gihagije.")
                    return
                p['igitigiri'] -= quantity
                now = datetime.now()
                data['sales'].append({
                    'date': now.strftime('%d/%m %Hh%M'),
                    'izina': p['izina'],
                    'quantity': quantity,
                    'total': p['igiciro'] * quantity
                })
                kubika(data)
                print("Kudandaza birarangiye.")
                return
        print("Id ntibonywe.")
    except ValueError:
        print("Injiza id n'igitigiri vy'ukuri.")

def kuraba_ivyadandajwe(data):
    if not data['sales']:
        print("Nta vyadandajwe birabaho.")
        return
    total = 0
    for s in data['sales']:
        print(f"{s['date']} {s['izina']:<10} x{s['quantity']} : {s['total']:,} Fbu")
        total += s['total']
    print(f"{'':<30}Vyose hamwe : {total:,} Fbu")

def kuraba_raporo(data):
    total_sales = len(data['sales'])
    total_amount = sum(s['total'] for s in data['sales'])
    out_of_stock = sum(1 for p in data['products'] if p['igitigiri'] == 0)
    total_items = sum(p['igitigiri'] for p in data['products'])

    print(f"Mumaze kudandaza incuro         {total_sales}")
    print(f"Mumaze kudandaza amahera   {total_amount:,}")
    print(f"Ibidandazwa vyaheze              {out_of_stock}")
    print(f"Ibidandazwa vyose hamwe         {total_items}")

def main():
    data = load_data()

    while True:
        print("""
URUDANDAZA
==========
1. Kuraba ibidandazwa
2. Gushiramwo ikidandazwa
3. Guhanagura ikidandazwa
4. Guhindura ibiranga ikidandazwa
5. Kudandaza
6. Kuraba ivyadandajwe
7. Kuraba raporo
0. Guhagarika
        """)
        choice = input("Hitamwo: ").strip()
        if choice == '1':
            afisha_ibidandaza(data)
        elif choice == '2':
            gushiramwo_ikidandazwa(data)
        elif choice == '3':
            gufuta_ikidandazwa(data)
        elif choice == '4':
            update_product(data)
        elif choice == '5':
            kugurisha_ikidandazwa(data)
        elif choice == '6':
            kuraba_ivyadandajwe(data)
        elif choice == '7':
            kuraba_raporo(data)
        elif choice == '0':
            print("Murakoze gukoresha URUDANDAZA!")
            break
        else:
            print("Ico wahisemwo ntakiriho.")

if __name__ == '__main__':
    main()
