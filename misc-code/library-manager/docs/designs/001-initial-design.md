# Requirements

- Checkout a book
- Add a book
- Remove a book
- Manage multiple copies of a book

# Entities

- Cataloge Items
    - id
    - isbn #
    - num_avail
    - num_out
    - title
    - author
- Users
    - id
    - name
- Checkouts
    - book_id
    - user_id

## Book table design
- Option 1
    - Book table record has one book per record and each book record has
        num_avail and num_out to enable faster distributed updates on
        checkouts / checkins
    - CON: need to remember to use select for update
- Option 2
    - Book table has a record for each book at the library - checkins and
        checkouts update the book record
    - CON: more books in the database, need to compare and set

# Checkout / Checkin

Checkout:
    BEGIN transaction
    check if book is availale (num_out < num_avail) -> select for update
    Add record to check_out table
    END transaction

# Services structure

- Service: Users
    - auth
    - user management
- Service: Items
    - item management
    - checkout
- Service: Conference rooms
    - booking

