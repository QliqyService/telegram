from app.services.postgresql import LifeCycleMixin, SQLAlchemyBase


class Comment(SQLAlchemyBase, LifeCycleMixin):
    __tablename__ = "comments"
