
from sqlalchemy import Column, Integer, String, ForeignKey,\
    create_engine, select, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

association_table = Table(
    'association_table', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('book_id', Integer, ForeignKey('books.id'))
)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(60), nullable=False)
    author = Column(String(30), nullable=False)
    reviews = relationship('Reviews', backref='book', lazy=True)
    readers = relationship('User', secondary=association_table, back_populates='books',
                           lazy=True)
    film = relationship('Film', back_populates='book', uselist=False, lazy=True)

    def __repr__(self):
        return self.title


class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    text = Column(String(2000), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'От {self.reviewer}'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    reviews = relationship('Reviews', backref='reviewer', lazy=True)
    books = relationship('Book', secondary=association_table,
                         back_populates='readers', lazy=True)

    def __repr__(self):
        return self.name

class Film(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    producer = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('Book', back_populates='film', uselist=False, lazy=True)

engine = create_engine('postgresql://postgres:enigma12@localhost:5432/postgres', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


book1 = session.query(Book).filter_by(title='Робинзон Крузо').first()
film1 = Film(name='Невероятные приключения Робинзона', producer='Квентин Тарантино', book_id=book1.id)
film2 = Film(name='Не правильный фильм', producer='Не Квентин Тарантино', book_id=book1.id)
session.add(film1)
session.add(film2)
session.commit()
