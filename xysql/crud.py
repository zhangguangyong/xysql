from typing import TypeVar, Generic

from sqlalchemy import text
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()
T = TypeVar('T', bound=Base)
id_column = 'id'


class Crud(Generic[T]):
    def __init__(self, cls: T):
        self.cls = cls

    def get_by_id(self, s: Session, id_) -> T:
        """ 根据主键查询 """
        return s.query(self.cls).filter(getattr(self.cls, id_column) == id_).first()

    def get_by_ids(self, s: Session, ids: list) -> list[T]:
        """ 根据多个主键查询 """
        return s.query(self.cls).filter(getattr(self.cls, id_column).in_(ids)).all()

    def get_by_dict(self, s: Session, kv: dict = None) -> list[T]:
        """ 查询 """
        q = s.query(self.cls)
        if not kv:
            return q.all()

        for k in kv:
            if kv[k] is not None:
                q = q.filter(getattr(self.cls, k) == kv[k])
        return q.all()

    def create(self, s: Session, kv: dict):
        """ 新增 """
        s.add(self.cls(**kv))
        s.commit()

    def create_batch(self, s: Session, dicts: list[dict]):
        """ 批量新增 """
        s.bulk_insert_mappings(self.cls, dicts)
        s.commit()

    def update(self, s: Session, kv: dict):
        """ 根据主键更新 """
        params = {}
        for k in kv:
            if k == 'id' or kv[k] is None:
                continue
            params[getattr(self.cls, k)] = kv[k]
        s.query(self.cls).filter(getattr(self.cls, id_column) == kv[id_column]).update(params)

    def update_batch(self, s: Session, dicts: list[dict]):
        """ 批量更新 """
        s.bulk_update_mappings(self.cls, dicts)
        s.commit()

    def delete_by_id(self, s: Session, id_):
        """ 根据主键删除 """
        s.query(self.cls).filter(getattr(self.cls, id_column) == id_).delete_by_id()

    def delete_by_ids(self, s: Session, ids: list):
        """ 根据多个主键删除 """
        s.query(self.cls).filter(getattr(self.cls, id_column).in_(ids)).delete()

    def delete_by_dict(self, s: Session, kv: dict):
        """ 条件删除 """
        q = s.query(self.cls)
        for k in kv:
            if kv[k] is not None:
                q = q.filter(getattr(self.cls, k) == kv[k])
        q.delete()

    def select_by_sql(self, s: Session, sql: str, params: dict):
        """ sql查询 """
        rs = s.execute(text(sql), params).fetchall()
        if not rs:
            return []

        rows = []
        for row in rs:
            rows.append(dict(row._mapping))
        return rows
