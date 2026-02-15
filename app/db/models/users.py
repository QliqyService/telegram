from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.services.postgresql import LifeCycleMixin, SQLAlchemyBase



class User(SQLAlchemyBase, LifeCycleMixin):
    """User ORM model"""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(sa.String(255), nullable=False, unique=True, index=True)
    phone: Mapped[int | None] = mapped_column(sa.BigInteger, nullable=True)
    first_name: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(sa.String, nullable=True)

    is_active: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=True, index=True)
    is_superuser: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False)
    is_verified: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False, server_default=sa.true())
