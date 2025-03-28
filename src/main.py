from typing import cast

from sqlalchemy import URL, create_engine, select
from sqlalchemy.orm import Session

from src.models import User

_session: Session | None


def create_session(url: URL) -> None:
    global _session
    engine = create_engine(url, echo=True)
    _session = Session(engine)


def get_session() -> Session:
    global _session
    if _session is None:
        raise ValueError("Session not created")
    return _session


def get_users(names: list[str]) -> list[User]:
    stmt = select(User).where(User.name.in_(names))

    session = get_session()
    return cast("list[User]", session.scalars(stmt))


def print_users(names: list[str]) -> None:
    for user in get_users(names):
        print(f"User: {user.id} - {user.name}")


if __name__ == "__main__":
    create_session(
        URL.create(
            "postgresql+psycopg",
            username="root",
            password="password",  # noqa: S106
            host="127.0.0.1",
            port=5432,
            database="postgres",
        )
    )
    print_users(["spongebob", "sandy"])
