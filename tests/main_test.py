from textwrap import dedent
from unittest.mock import MagicMock, patch

from sqlalchemy.dialects import postgresql

from src import main, models


@patch("src.main.get_session", autospec=True)
def test_get_users(mock_get_session: MagicMock) -> None:
    mock_get_session().scalars.return_value = [
        models.User(id=1, name="spongebob", fullname="Spongebob Squarepants"),
        models.User(id=2, name="sandy", fullname="Sandy Cheeks"),
    ]

    users = main.get_users(["spongebob", "sandy"])

    stmt = mock_get_session().scalars.call_args[0][0]
    compiled_stmt = stmt.compile(
        dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
    )
    query = str(compiled_stmt).replace(" \n", "\n")
    assert query == dedent(
        """\
        SELECT user_account.id, user_account.name, user_account.fullname
        FROM user_account
        WHERE user_account.name IN ('spongebob', 'sandy')"""
    )
    assert len(users) == 2
    assert users[0].name == "spongebob"
    assert users[1].name == "sandy"


from _pytest.capture import CaptureFixture


@patch(
    "src.main.get_users",
    autospec=True,
    return_value=[
        models.User(id=1, name="spongebob", fullname="Spongebob Squarepants"),
        models.User(id=2, name="sandy", fullname="Sandy Cheeks"),
    ],
)
def test_print_users(mock_get_users: MagicMock, capsys: CaptureFixture) -> None:
    main.print_users(["spongebob", "sandy"])
    out, err = capsys.readouterr()
    out_lines = out.split("\n")
    assert out_lines[0] == "User: 1 - spongebob"
    assert out_lines[1] == "User: 2 - sandy"
    assert out_lines[2] == ""
    assert err == ""
    mock_get_users.assert_called_once_with(["spongebob", "sandy"])
