import random   #Random oneri icin modul
import json #Saveler icin modul
import os   #Save islemi ve silme icin modul

DATA_FILE = "media_data.json"   # Kaydedilen bilgiler

def load_data(path=DATA_FILE):  #Kullanci bilgilerini yukleme
    if not os.path.exists(path):
        return {"user_name": None, "liked": [], "not_liked": [], "watchlist": []}   #kaydedilen bilgi olmadiginda degisken ve liste atamalari
    try:
        with open(path, "r", encoding="utf-8") as f:        #kaydedilen bilgi var mi kontrolu
            data = json.load(f)
        data.setdefault("user_name", None)
        data.setdefault("liked", [])
        data.setdefault("not_liked", [])
        data.setdefault("watchlist", [])
        return data
    except (json.JSONDecodeError, OSError) as e:    #dosyayi okuyamadiginda sifirdan baslamasi
        print(f"Warning: could not read {path} ({e}). Starting fresh.")
        return {"user_name": None, "liked": [], "not_liked": [], "watchlist": []}

def save_data(data, path=DATA_FILE):        #Bilgilere kaydetme fonksiyonu
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def reset_app():    #Bilgileri sifirlama fonksiyonu
    print("\nThis action will permanently erase all data, This cannot be undone. Are you sure?")
    confirm = input("Type 'RESET' to confirm (anything else cancels): ").strip()
    if confirm != "RESET":
        print("Reset cancelled. Nothing was deleted.")
        return False
    if os.path.exists(DATA_FILE):
        try:
            os.remove(DATA_FILE)
            print(f"Deleted '{DATA_FILE}'.")
        except OSError as e:
            print(f"Could not delete '{DATA_FILE}': {e}")
            return False
    else:
        print("No data file found — nothing to delete.")
    print("Application was reset. Restart the program to begin fresh.")
    return True

def name_get(state):        ## Isim soran fonksiyon, eger zaten kaydedilen isim var ise sormayi geciyor
    if state.get("user_name"):
        return state["user_name"]
    while True:
        user_name = input("Greeting Sir or Madame, What is your name?\n").strip()
        if user_name:
            state["user_name"] = user_name
            return user_name
        print("Your name cannot be empty, Please enter a valid name")

GENRES = [
    "Action",
    "Comedy",
    "Drama",
    "Fantasy",
    "Horror",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "Documentary",
    "Animation",
]       ##Mumkun turleri liste olarak call
def choose_genre(): ##Tur secme fonksiyonu
    for i, genre in enumerate(GENRES, start=1): #Butun Turleri listeleme
        print(f"{i}. {genre}")
    while True:
        raw = input(f"Choose a genre from (1-{len(GENRES)}): ").strip()
        if raw.isdigit():
            choice = int(raw)   #kullanici inputunu raw halden sayiya cevirme
            if 1<= choice <= len(GENRES):
                return GENRES [choice - 1]
        print(f"That is not a valid choice. Enter a number from 1 to {len(GENRES)}")

def choose_media_type(): ##Dizi veya Film secme fonksiyonu
    print("What type of media have you watched?")
    print("1. Film")
    print("2. Series")
    while True:
        raw = input("Choose from (1-2) ").strip()
        if raw == "1":
            return "Film"
        if raw == "2":
            return "Series"
        print("Invalid Choice. Please enter, 1 for Movies, 2 for Series")
def get_media_entry():      ##Yeni Medya girdisi alma fonksiyonu, onceki tur ve tarz fonksiyonunu cagiriyor ve ad, yonetmen, yil sorduktan sonra sevilip sevilmedigini kayit ediyor
    print("\n--- Please Add the Media You have Watched ---")
    genre = choose_genre()
    media_type = choose_media_type()
    title = input("Name: ").strip()
    while not title:
        print("Name cannot be empty.")
        title = input("Name: ").strip()
    year = input("Year: ").strip()
    while not year.isdigit():
        print("The year has to be a valid number")
        year = input("Year: ").strip()
    year = int(year)
    director = input("Name of the director: ").strip()
    while not director:
        print("Director`s name cannot be empty.")
        director = input("Name of the director: ").strip()
    
    while True:
        enjoyed_raw = input("Did you enjoy it? (y/n): ").strip().lower()
        if enjoyed_raw in ("y", "yes"):
            enjoyed = True
            break
        if enjoyed_raw in ("n", "no"):
            enjoyed = False
            break
        print ("Please answer (y)es or (n)o. ")
    return {
        "media_type": media_type,
        "genre": genre,
        "title": title,
        "year": year,
        "director": director,
        "enjoyed": enjoyed,
    }
def show_list(label, items):    #Listeyi gostermek icin
    print(f"\n--- {label} ---")
    if not items:
        print("(There is nothing here yet)")    #Listede bir item olmadigi kosulu icin
        return
    for i, m in enumerate(items, start=1):
        print(f"{i}. [{m['media_type']}] {m['title']} ({m['year']}) — {m['genre']}, dir. {m['director']}")
def add_watchlist_entry(watchlist):     #Izlenmek istenen medyayi listesine entry kaydetme fonksiyonu
    print("\n--- Add to Watchlist ---")
    media_type = choose_media_type()
    genre = choose_genre()
    title = input("Name: ").strip()
    while not title:
        print("Name cannot be empty.")
        title = input("Name: ").strip()
    watchlist.append({"media_type": media_type, "genre": genre, "title": title})
    print(f"Added '{title}' to your watchlist.")

def show_watchlist(watchlist):      ##Izlenmek istenen medyayi listesini gosterme fonksiyonu
    print("\n--- Watchlist ---")
    if not watchlist:
        print("(There is nothing here yet)")
    else:
        for i, m in enumerate(watchlist, start=1):
            print(f"{i}. [{m['media_type']}] {m['title']} — {m['genre']}")

    # Liste goruntulendiginde yeni item istemek icin
    answer = input("\nAdd something new to the watchlist? (y/n): ").strip().lower()
    if answer in ("y", "yes"):
        add_watchlist_entry(watchlist)

def recommend_from_watchlist(watchlist):       #RAndom bir filmi izleme listesinden oneri
    if not watchlist:
        print("\nYour watchlist is empty — add something first (option 4).")
        return
    pick = random.choice(watchlist)
    print(f"\nAlfred recommends: [{pick['media_type']}] {pick['title']} — {pick['genre']}")

def export_lists(data):     #Listeleri kullanici istedigi takdirde text olarak yazdirmak icin

    default_name = "media_export.txt"
    path = input(f"Export filename [{default_name}]: ").strip() or default_name

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("Alfred Media Tracker Export\n")
            f.write("=" * 40 + "\n\n")

            f.write("LIKED:\n")
            if data["liked"]:
                for m in data["liked"]:
                    f.write(f"  [{m['media_type']}] {m['title']} ({m['year']}) "
                            f"— {m['genre']}, dir. {m['director']}\n")
            else:
                f.write("  (none)\n")

            f.write("\nNOT LIKED:\n")
            if data["not_liked"]:
                for m in data["not_liked"]:
                    f.write(f"  [{m['media_type']}] {m['title']} ({m['year']}) "
                            f"— {m['genre']}, dir. {m['director']}\n")
            else:
                f.write("  (none)\n")

            f.write("\nWATCHLIST:\n")
            if data["watchlist"]:
                for m in data["watchlist"]:
                    f.write(f"  [{m['media_type']}] {m['title']} — {m['genre']}\n")
            else:
                f.write("  (none)\n")

        total = len(data["liked"]) + len(data["not_liked"]) + len(data["watchlist"])
        print(f"Exported {total} entries to '{path}'.")
    except OSError as e:    #yazma error exception handle
        print(f"Could not write '{path}': {e}")

def menu_display(name):     #Ana display itemleri
    print(f"\n========== Alfred Media Tracker Butler -- {name} ==========")
    print("1. Add a watched film or series")
    print("2. View the media you enjoyed")
    print("3. View the media you haven't enjoyed")
    print("4. View watchlist you can watch next")
    print("5. Make Alfred recommend a random media from your watchlist")
    print("6. Export your lists to a text file")
    print("7. Reset the application (erase all data)")
    print("8. Exit the Application")
    print("===========================================================")

def main_loop():           ##Ana Menu loop
    print("Welcome to the Alfred Media Tracker Software") ##Karsilama mesaji
    data = load_data()
    state = {"user_name": data["user_name"]}
    user_name = name_get(state)
    data["user_name"] = user_name
    print(f"Welcome to our abode, {user_name}. This is your personalized Media Tracker Application")

    print(f"Loaded {len(data['liked'])} liked, {len(data['not_liked'])} not-liked, {len(data['watchlist'])} watchlist entries from previous sessions.") #Onceden kaydedilenleri yukleme check i

    running = True

    while running:
        menu_display(user_name)
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":   #Yeni Medya Ekleme
            entry = get_media_entry()
            if entry["enjoyed"]:
                data['liked'].append(entry)
                print(f"Added '{entry['title']}' to LIKED.")
            else:
                data['not_liked'].append(entry)
                print(f"Added '{entry['title']}' to NOT LIKED.")
            save_data(data)
        elif choice == "2": #Sevilen medyayi gorme
            show_list("Liked Media", data['liked'])
        elif choice == "3": #Sevilmeyen Medyayi gorme
            show_list("Not-Liked Media", data['not_liked'])
        elif choice == "4": #Izleme listesini gosterme
            show_watchlist(data["watchlist"])
            save_data(data)
        elif choice == "5": #Izleme listesinden random bir item onerme
            recommend_from_watchlist(data["watchlist"])
        elif choice == "6": #Listeleri bir text e export secenegi
            export_lists(data)
        elif choice == "7":  #Uygulamayi sifirlar ve hic bilgi girmemis olarak devam eder
            if reset_app():
                running = False #Reser=t sonrasi uygulamayi kapatma
        
        elif choice == "8": #Uygulamadan normal cikma
            print(f"Goodbye, Sir/Madame {user_name}!")
            save_data(data)
            running = False
        else:
            print("Invalid choice. Please select 1-8.") #Gecersiz secenek

if __name__ == "__main__":  #Boilerplate
    main_loop()