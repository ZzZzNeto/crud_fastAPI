from fastapi import Request
from app.models.library import Book

def create_register_log(b = Book):
    with open("app/log.txt", "a") as log:
        log.write(f"   Object created\n\n   id: {b.id}\n   title: {b.title}\n   author: {b.author}\n\n")

def update_old_register_log(old = Book):
    with open("app/log.txt", "a") as log:
        log.write(f"   Object updated\n\n   OLD -\n      id: {old.id}\n      title: {old.title}\n      author: {old.author}\n\n")
    
def update_new_register_log(new = Book):
    with open("app/log.txt", "a") as log:
        log.write(f"   NEW -\n      id: {new.id}\n      title: {new.title}\n      author: {new.author}\n\n")