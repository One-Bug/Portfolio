from project import mail_format, mail_checker, password_checker


def test_mail_format():
    assert mail_format('a') == False
    assert mail_format('jose@gmail.com') == True
    assert mail_format('j@gmail') == False


def test_mail_checker():
    assert mail_checker('a') == False
    assert mail_checker('asdf@asdf.com') == True
    assert mail_checker('some@gmail.com') == False


def test_password_checker():
    assert password_checker('a') == False
    assert password_checker('password123') == False
    assert password_checker('Passw@rd123') == True
