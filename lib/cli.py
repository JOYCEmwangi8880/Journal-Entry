from Journal import Base, User, JournalEntry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///journal.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def add_user():
    username = input('Enter username: ')
    email = input('Enter email: ')
    session = Session()
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    print(f'User {username} added successfully.')

    # Print the contents of the users table
    users = session.query(User).all()
    print("Users in the database:")
    for user in users:
        print(f'ID: {user.id}, Username: {user.username}, Email: {user.email}')


def add_entry():
    title = input('Enter title: ')
    content = input('Enter content: ')
    username = input('Enter username: ')
    
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        entry = JournalEntry(title=title, content=content, user=user)
        session.add(entry)
        session.commit()
        print(f'Journal entry added successfully for user {username}.')
    else:
        print(f'User {username} not found. Please add the user first.')

def view_entries():
    username = input('Enter username: ')
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        entries = session.query(JournalEntry).filter_by(user=user).all()
        if entries:
            print(f'Journal entries for user {username}:')
            for entry in entries:
                print(f'Title: {entry.title}\nContent: {entry.content}\n')
        else:
            print(f'No journal entries found for user {username}.')
    else:
        print(f'User {username} not found.')

def edit_entry():
    title = input('Enter title of the entry to edit: ')
    new_title = input('Enter new title: ')
    new_content = input('Enter new content: ')
    
    session = Session()
    entry = session.query(JournalEntry).filter_by(title=title).first()
    
    if entry:
        entry.title = new_title
        entry.content = new_content
        session.commit()
        print(f'Journal entry edited successfully.')
    else:
        print(f'Journal entry with title {title} not found.')

def delete_entry():
    title = input('Enter title of the entry to delete: ')
    session = Session()
    entry = session.query(JournalEntry).filter_by(title=title).first()
    
    if entry:
        session.delete(entry)
        session.commit()
        print(f'Journal entry deleted successfully.')
    else:
        print(f'Journal entry with title {title} not found.')

if __name__ == '__main__':
    while True:
        print("\nOptions:")
        print("1. Add User")
        print("2. Add Journal Entry")
        print("3. View Journal Entries")
        print("4. Edit Journal Entry")
        print("5. Delete Journal Entry")
        print("6. Exit")

        try:
            choice = int(input("Enter your choice (1-6): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            add_user()
        elif choice == 2:
            add_entry()
        elif choice == 3:
            view_entries()
        elif choice == 4:
            edit_entry()
        elif choice == 5:
            delete_entry()
        elif choice == 6:
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
