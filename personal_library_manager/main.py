import streamlit as st
import json

# File to store books
BOOKS_FILE = "books_data.json"

def load_books():
    try:
        with open(BOOKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_books(books):
    with open(BOOKS_FILE, "w") as file:
        json.dump(books, file, indent=4)

# Load existing books
books = load_books()

# UI
st.title("📚 Personal Library Manager")
st.subheader("Add a New Book")

# Input Fields
title = st.text_input("📖 Book Name")
author = st.text_input("✍️ Author")
year = st.text_input("📅 Year")
genre = st.text_input("🏷️ Genre")
read = st.checkbox("✅ Mark as Read")

# Ensure all fields are filled before adding
if st.button("➕ Add Book"):
    if title.strip() and author.strip() and year.strip() and genre.strip():
        new_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
        books.append(new_book)
        save_books(books)
        st.success(f"✅ '{title}' added successfully!")
        st.rerun()
    else:
        st.warning("⚠️ Please fill in all the fields before adding the book.")

# Display Books
st.subheader("📖 Your Book Collection")
if books:
    read_books = [book for book in books if book["read"]]
    unread_books = [book for book in books if not book["read"]]

    st.write("### ✅ Read Books")
    if read_books:
        for book in read_books:
            st.write(f"📘 **{book['title']}** | ✍️ {book['author']} | 📅 {book['year']} | 🏷️ {book['genre']}")
    else:
        st.info("No read books yet.")

    st.write("### ❌ Unread Books")
    if unread_books:
        for book in unread_books:
            st.write(f"📕 **{book['title']}** | ✍️ {book['author']} | 📅 {book['year']} | 🏷️ {book['genre']}")
    else:
        st.info("No unread books yet.")

    # Update Book Feature
    st.subheader("✏️ Update a Book")
    book_titles = [book["title"] for book in books]
    selected_book = st.selectbox("📌 Select a book to update", book_titles, key="update_book")

    if selected_book:
        book_index = next((i for i, book in enumerate(books) if book["title"] == selected_book), None)
        if book_index is not None:
            updated_title = st.text_input("📖 New Title", books[book_index]["title"])
            updated_author = st.text_input("✍️ New Author", books[book_index]["author"])
            updated_year = st.text_input("📅 New Year", books[book_index]["year"])
            updated_genre = st.text_input("🏷️ New Genre", books[book_index]["genre"])
            updated_read = st.checkbox("✅ Mark as Read", books[book_index]["read"], key=f"read_{book_index}")

            if st.button("💾 Update Book"):
                books[book_index] = {
                    "title": updated_title, 
                    "author": updated_author, 
                    "year": updated_year, 
                    "genre": updated_genre, 
                    "read": updated_read
                }
                save_books(books)
                st.success(f"✅ '{updated_title}' updated successfully!")
                st.rerun()

    # Remove a Book
    st.subheader("🗑 Remove a Book")
    book_to_remove = st.selectbox("📌 Select a book to remove", book_titles, key="remove_book")

    if st.button("❌ Remove Book"):
        books = [book for book in books if book["title"] != book_to_remove]
        save_books(books)
        st.success(f"❌ '{book_to_remove}' removed successfully!")
        st.rerun()
else:
    st.info("No books in your collection yet.")
