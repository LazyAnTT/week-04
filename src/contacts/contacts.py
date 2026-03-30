import sys
import os
import json


def load_contacts(contacts_file="contacts.json"):
    """Load contacts from the JSON file. If the file does not exist, return an empty list."""
    if not os.path.exists(contacts_file):
        return []
    with open(contacts_file, "r", encoding="utf-8") as contacts:
        return json.load(contacts)


def save_contacts(contacts_list, contacts_file="contacts.json"):
    """Save the contacts list to the JSON file."""
    with open(contacts_file, "w", encoding="utf-8") as file:
        json.dump(contacts_list, file, ensure_ascii=False, indent=2)


def add_contact(contacts_list):
    """Add a new contact to the contacts list."""
    name = input("Ievadiet kontakta vārdu: ")
    phone = input("Ievadiet tālruņa nr.: ")
    contacts_list.append({"name": name, "phone": phone})
    print(f"Kontakts '{name}' ir pievienots.")


def list_contacts(contacts_list):
    """Display all contacts."""
    if not contacts_list:
        print("Kontaktu saraksts ir tukšs.")
        return

    print("\nKontaktu saraksts:")
    for i, contact in enumerate(contacts_list, start=1):
        print(f"{i}. {contact['name']} - {contact['phone']}")


def search_contacts(contacts_list, query):
    """Search contacts by full or partial name."""
    query = query.lower()
    found_contacts = []

    for contact in contacts_list:
        if query in contact["name"].lower():
            found_contacts.append(contact)

    if not found_contacts:
        print(f"Kontakti ar vārda daļu '{query}' netika atrasti.")
        return

    print(f"Atrastie kontakti priekš '{query}':")
    for i, contact in enumerate(found_contacts, start=1):
        print(f"{i}. {contact['name']} - {contact['phone']}")


if __name__ == "__main__":
    contacts_list = load_contacts()

    if len(sys.argv) < 2:
        print("Lietošana:")
        print("  python contacts.py list")
        print("  python contacts.py add")
        print("  python contacts.py search name")
        sys.exit()

    command = sys.argv[1]

    if command == "list":
        list_contacts(contacts_list)

    elif command == "add":
        add_contact(contacts_list)
        save_contacts(contacts_list)

    elif command == "search":
        if len(sys.argv) < 3:
            print("Lūdzu norādiet meklējamo vārdu vai tā fragmentu.")
            print("Piemērs: python contacts.py search mar")
            sys.exit()
        query = sys.argv[2]
        search_contacts(contacts_list, query)

    else:
        print("Nezināma komanda.")
