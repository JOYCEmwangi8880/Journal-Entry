from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base

DATABASE_URL = 'sqlite:///journal.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    entries = relationship('JournalEntry', back_populates='user')

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    entries = relationship('JournalEntry', back_populates='category')

class JournalEntry(Base):
    __tablename__ = 'journal_entries'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    user = relationship('User', back_populates='entries')
    category = relationship('Category', back_populates='entries')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def create_journal_entry():
    title = input('Enter title: ')
    content = input('Enter content: ')
    username = input('Enter your username: ')
    category_name = input('Enter category: ')

    session = Session()
    
    # Check if the user exists, if not, add the user
    user = session.query(User).filter_by(username=username).first()
    if user is None:
        email = input('Enter email for the user: ')
        user = User(username=username, email=email)
        session.add(user)
        session.commit()
        print(f'User {username} added successfully.')

    # Check if the category exists, if not, add the category
    category = session.query(Category).filter_by(name=category_name).first()
    if category is None:
        description = input('Enter a description for the category:')
        category = Category(name=category_name, description=description)
        session.add(category)
        session.commit()
        print('Category added successfully.')

    session.close()

def view_journal_entries():
    username = input('Enter your username: ')
    session = Session()
    user = session.query(User).filter_by(username=username).first()

    if user:
        entries = session.query(JournalEntry).filter_by(user=user).all()
        if entries:
            print(f'Journal entries for user {username}:')
            for entry in entries:
                print(f'Title: {entry.title}\nContent: {entry.content}\nCategory: {entry.category.name}\n')
        else:
            print(f'No journal entries found for user {username}.')
    else:
        print(f'User {username} not found.')

    session.close()

def update_journal_entry():
    title = input('Enter title of the entry to update: ')
    new_title = input('Enter new title: ')
    new_content = input('Enter new content: ')

    session = Session()
    entry = session.query(JournalEntry).filter_by(title=title).first()

    if entry:
        entry.title = new_title
        entry.content = new_content
        session.commit()
        print(f'Journal entry updated successfully.')
    else:
        print(f'Journal entry with title {title} not found.')

    session.close()

def delete_journal_entry():
    title = input('Enter title of the entry to delete: ')
    session = Session()
    entry = session.query(JournalEntry).filter_by(title=title).first()

    if entry:
        session.delete(entry)
        session.commit()
        print(f'Journal entry deleted successfully.')
    else:
        print(f'Journal entry with title {title} not found.')

    session.close()

def list_journal_entries():
    # This method could be used by an admin to list all journal entries
    session = Session()
    entries = session.query(JournalEntry).all()

    if entries:
        print("All Journal Entries:")
        for entry in entries:
            print(f'Title: {entry.title}\nContent: {entry.content}\nCategory: {entry.category.name}\n')
    else:
        print("No journal entries found.")

    session.close()

def print_entries(session):
    entries = session.query(JournalEntry).all()
    if entries:
        print("All Journal Entries:")
        for entry in entries:
            print(f'Title: {entry.title}\nContent: {entry.content}\nCategory: {entry.category.name}\n')
    else:
        print("No journal entries found.")

if __name__ == '__main__':
    while True:
        print("\nOptions:")
        print("1. Create Journal Entry")
        print("2. View Journal Entries")
        print("3. Update Journal Entry")
        print("4. Delete Journal Entry")
        print("5. List Journal Entries (Admin)")
        print("6. Exit")

        try:
            choice = int(input("Enter your choice (1-6): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            create_journal_entry()
        elif choice == 2:
            view_journal_entries()
        elif choice == 3:
            update_journal_entry()
        elif choice == 4:
            delete_journal_entry()
        elif choice == 5:
            list_journal_entries()
        elif choice == 6:
            break
        else:
            print("Invalid. Please enter a number between 1 and 6.")
