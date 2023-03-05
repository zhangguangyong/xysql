from sqlalchemy import create_engine, Column, BIGINT, String
from sqlalchemy.orm import sessionmaker

from xysql.crud import Base, Crud
from urllib.parse import quote_plus

user = 'root'
# 特殊字符使用 quote_plus 编码
password = quote_plus('46CP^7#si@DD')

engine = create_engine(
    f'mysql+pymysql://{user}:{password}@localhost:3306/test',
    echo=True
)

SessionLocal = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'user'
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    name = Column(String)


class UserDao(Crud[User]):
    def __init__(self):
        super().__init__(cls=User)


def test():
    dao = UserDao()
    s = SessionLocal()
    dao.create(s, {'name': '张三'})
    s.commit()


if __name__ == '__main__':
    test()
    pass
