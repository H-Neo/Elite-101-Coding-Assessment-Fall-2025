from library_books import library_books
from user_accounts import accounts
from datetime import datetime, timedelta

def update_books(books):
    with open("library_books.py", "w") as file:
        file.write("library_books = " + str(books))

def update_accounts(accounts):
    with open ("user_accounts.py", "w") as file:
        file.write("accounts = " + str(accounts))

# -------- Level 1 --------
# TODO: Create a function to view all books that are currently available

def view_books(books):
    for i in range(len(books)):
        print(f"\"{books[i]["title"]}\" by {books[i]["author"]}. Genre: {books[i]["genre"]}. ID: {books[i]["id"]}.")
    wait = input("")

# -------- Level 2 --------
# TODO: Create a function to search books by author OR genre
    #honestly, people are most likely going to search the book with author 
    #i've implemented search by title inside here too.
def search_book(books):
    try:
        query = input("Enter search query: ").strip().lower()
        if len(query) != 0:
            possible_books = 0
            for i in range(len(books)):
                if query in books[i]["genre"].lower() or query in books[i]["author"].lower() or query in books[i]["title"].lower():
                    print(f"\"{books[i]["title"]}\" by {books[i]["author"]}. Genre: {books[i]["genre"]}. ID: {books[i]["id"]}.")
                    possible_books += 1
            if possible_books == 0:
                print("No results found.")
        else:
            print("No input detected.")
        wait = input("")
    except:
        print("An error has occurred. Please check your inputs.")
# -------- Level 3 --------
# TODO: Create a function to checkout a book by ID
def checkout_book(books, accounts):
    try:
        print("Enter the book ID you would like to checkout:")
        print("[S] Search")
        book_id = input("").strip()
        if book_id.lower() == "s":
            search_book(library_books)
            return
        else:
            found = -1
            for i in range(len(books)):
                if books[i]["id"] == book_id:
                    found = i
                    break
        if found == -1:
            print("No book found with that ID.")
        elif not books[found]["available"]:
            print("That book is already checked out.")
        else:
            if books[found]["available"]:
                accounts[logged_in]["checkouts"].append(book_id)
                books[found]["available"] = False
                books[found]["due_date"] = (datetime.now() + timedelta(weeks=2)).strftime("%Y-%m-%d")
                books[found][("checkouts")] += 1
                update_books(books)
                update_accounts(accounts)
                print(f"Checked out {books[i]['title']}. Due date {books[found]['due_date']}")
            else:
                print("That book is already checked out.")
        wait = input("")
    except:
        print("An error has occurred. Please check your inputs.")

            
# -------- Level 4 --------
# TODO: Create a function to return a book by ID
# Set its availability to True and clear the due_date
def return_book(books):
    try:
        checked_out = accounts[logged_in]["checkouts"]
        if len(checked_out) == 0:
            print("You have no books checked out.")
            wait = input("")
            return
        print("Current checked out books:")
        index_and_book = []
        for i, book_id in enumerate(checked_out):
            for book in books:
                if book["id"] == book_id:
                    print(f"{i+1}. {book['title']} (ID: {book['id']})")
                    index_and_book.append((i, book))
        book_return = int(input("Enter the number of the book you want to return: "))
        if not 1 <= book_return <= len(accounts[logged_in]["checkouts"]):
            print("Invalid input.")
            wait = input("")
            return
        book_return -= 1
        checkout_index, checked_out_book = index_and_book[book_return]
        book_id = checked_out_book["id"]

        accounts[logged_in]["checkouts"].remove(book_id)
        for book in books:
            if book["id"] == book_id:
                book["available"] = True
                book["due_date"] = None

        update_books(books)
        update_accounts(accounts)
        print(f"Returned {checked_out_book["title"]}.")
        wait = input("")
    except:
        print("An error has occurred. Please check your inputs.")
    # TODO: Create a function to list all overdue books
# A book is overdue if its due_date is before today AND it is still checked out
def overdue_books(books):
    checked_out = accounts[logged_in]["checkouts"]
    if len(checked_out) == 0:
        print("You have no books checked out.")
        wait = input("")
        return
    print("Current checked out books:")
    now = datetime.now().date()
    overdue_list = []
    for i, book_id in enumerate(checked_out):
        for book in books:
            if book["id"] == book_id:
                due_date = book["due_date"]
                due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                print(f"{i+1}. {book['title']} (ID: {book['id']}) - Due: {due_date}")
                
                if (not book["available"]) and due_date < now:
                    overdue_list.append(book)
    print("Overdue Books:")
    if len(overdue_list) == 0:
        print("You have no overdue books.")
    else:
        for book in overdue_list:
            print(f"{book['title']} (ID: {book['id']}) - Due: {book['due_date']}")
    wait = input("")

# -------- Level 5 --------
# TODO: Convert your data into a Book class with methods like checkout() and return_book()
    # unfortunately I didn't have enough time to look into this
# TODO: Add a simple menu that allows the user to choose different options like view, search, checkout, return, etc.
    #menu is completed
#unfortunately I didn't have time to add a check to ensure there wouldn't be duplicates of book IDs or titles..
def add_book(books):
    print("Input the following info:")
    id = input("Enter book ID: ")
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    genre = input("Enter book genre: ")
    books.append({"id": id, "title": title, "author": author, "genre": genre, "available": True, "due_date": None, "checkouts": 0})
    update_books(books)
    wait = input("")

# - Sort and display the top 3 most checked-out books

def popular_books(books):
    print("Top 3 Most Checked Out Books:")
    sorted_books = books
    for i in range(len(sorted_books)):
        for j in range(0, len(sorted_books)-i-1):
            if sorted_books[j]["checkouts"] < sorted_books[j+1]["checkouts"]:
                sorted_books[j], sorted_books[j+1] = sorted_books[j+1], sorted_books[j]
    for i in range(min(3, len(sorted_books))):
        book = sorted_books[i]
        print(f"{i+1}. {book['title']} - {book['checkouts']} checkouts")
    wait = input("")


# - Partial title/author search
    #done through implementing it through search_book.
# - Save/load catalog to file (CSV or JSON)
    #didn't get to look into this
# - Anything else you want to build on top of the system!
    # !!!

def toggle_assistant(accounts):
    print("Which account would you like to toggle assistant authorization? ")
    for i, account in enumerate(accounts):
        print(f"{i+1}) {account['user']}")
    acc_num = int(input(""))-1
    if 1 <= acc_num <= len(accounts):
        if accounts[acc_num]["authorization"] == 0:
            accounts[acc_num]["authorization"] = 1
            update_accounts(accounts)
            print("Action completed. ")
        elif accounts[acc_num]["authorization"] == 1:
            accounts[acc_num]["authorization"] = 0
            update_accounts(accounts)
            print("Action completed. ")
        else:
            print("User authorization same or higher than current authorization.")
    else:
        print("Invalid user account.")
    wait = input("")
    
if __name__ == "__main__":
    try:
        running = True
        logged_in = -1
        auth = -1
        
        print("Welcome!")
        while logged_in == -1:
            print("1. Login")
            print("2. Create an account")
            print("3. Login as guest")
            user_choice = input("")
            if user_choice == "1":
                username = input("Username: ")
                password = input("Password: ")
                for i, user in enumerate(accounts):
                    if username == user["user"] and password == user["password"]:
                        logged_in = i
                        auth = user["authorization"]
                if logged_in == -1:
                    print("Invalid username or password!")
            elif user_choice == "2":
                has_acc = False
                while not has_acc:
                    username = input("Enter a username: ").lower()
                    valid_user = True
                    for i in accounts:
                        if i["user"].lower() == username:
                            valid_user = False
                    if not valid_user:
                        print("Username is taken!")
                        continue
                    else:
                        password = input("Enter a password: ")
                        has_acc = True
                        accounts.append({"user": username, "password": password, "authorization": 0, "checkouts": []})
                        #i think this is slightly different from what I learned, I looked at python doc and did remember how with open works when opening docs
                        with open ("user_accounts.py", 'w') as user_accounts:
                            user_accounts.write("accounts = " + str(accounts))
                        logged_in = len(accounts)-1
                        auth = 0
            elif user_choice == "3":
                break
            
        print("")
        while running:
            print("1. View all cataloged books")
            print("2. Search for a book/author/genre")
            if auth >= 0:
                print("3. Checkout a book")
                print("4. Return a book")
                print("5. View overdue books")
                print("6. View popular books") 
            else:
                print("3. View popular books") 
            if auth >= 1:
                print("7. Add a book to the catalog")
            if auth >= 2:
                print("8. Toggle assistant authorization")
            print("0. Exit")
            user_selection = input("")
            print("")
            if user_selection == "1":
                view_books(library_books)
            elif user_selection == "2":
                search_book(library_books)
        
            if auth >= 2:
                if user_selection == "3":
                    checkout_book(library_books, accounts)
                elif user_selection == "4":
                    return_book(library_books)
                elif user_selection == "5":
                    overdue_books(library_books)
                elif user_selection == "6":
                    popular_books(library_books)
                elif user_selection == "7":
                    add_book(library_books)
                elif user_selection == "8":
                    toggle_assistant(accounts)
                elif user_selection == "0":
                    print("Thank you for using NH Library Management.")
                    running = False
            elif auth >= 1:
                if user_selection == "3":
                    checkout_book(library_books, accounts)
                elif user_selection == "4":
                    return_book(library_books)
                elif user_selection == "5":
                    overdue_books(library_books)
                elif user_selection == "6":
                    popular_books(library_books)
                elif user_selection == "7":
                    add_book(library_books)
                elif user_selection == "0":
                    print("Thank you for using NH Library Management.")
                    running = False
            elif auth >= 0:
                if user_selection == "3":
                    popular_books(library_books)
            else:
                print("An unknown error has occurred. Please report to this issue to an administrator.")
                running = False
    except:
        print("An error has occurred. Please check your inputs.")