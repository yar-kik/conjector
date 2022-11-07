# Python Application Properties
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pre-commit: enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat)](https://github.com/pre-commit/pre-commit)


## How To Use
The main purpose of this library is to simplify work with an application configs.

Let's assume that you have some email service which requires a couple message templates.
It'll look like:
```python
class EmailService:
    CONFIRM_REGISTRATION_TEMPLATE = "Thanks for your registration!"
    RESET_PASSWORD_TEMPLATE = "To reset a password follow the link - {link}"
    # and another templates...
    
    def __init__(self, mail_sender: IMailSender) -> None:
        self._sender = mail_sender
    
    def send_confirm_registration_mail(self, username: str) -> None:
        self._sender.send_mail(username, self.CONFIRM_REGISTRATION_TEMPLATE)
    
    def send_reset_password_email(self, username: str, link: str) -> None:
        template = self.RESET_PASSWORD_TEMPLATE.format(link=link)
        self._sender.send_mail(username, template)
    # and another methods...
```
As you can see, there are some problems connected with storing message templates in class variables:
* Templates could have a big size and that decrease readability of a whole class.
* It's also hard to maintain different versions of templates.

But if you have config file `my_config.yml` with content below, you can "inject" variables to the `EmailService` class:
```yaml
email_templates:
  confirm_registration_template: Thanks for your registration!
  reset_password_template: To reset a password follow the link - {link}
  # and so on...
```
```python
@properties(filename="my_config.yml", root="email_templates")
class EmailService:
    CONFIRM_REGISTRATION_TEMPLATE: str
    RESET_PASSWORD_TEMPLATE: str
    # and another templates...
    
    def __init__(self, mail_sender: IMailSender) -> None:
        self._sender = mail_sender
    
    def send_confirm_registration_mail(self, username: str) -> None:
        self._sender.send_mail(username, self.CONFIRM_REGISTRATION_TEMPLATE)
    
    def send_reset_password_email(self, username: str, link: str) -> None:
        template = self.RESET_PASSWORD_TEMPLATE.format(link=link)
        self._sender.send_mail(username, template)
    # and another methods...
```
And that's all. Just one decorator and some file with application properties.
You can even inject all necessary data into dataclass object:
```python
@properties(filename="my_config.yml", root="email_templates")
@dataclass(init=False)
class EmailTemplates:
    confirm_registration_template: str
    reset_password_template: str
```
`init=False` is required if you don't want to pass and override params during instance initialization.

## Available features
* Supporting `.yaml` and `.json` extensions of configs.
* Accessing nested configs using `root` variable:
```yaml
# "config.yaml"
some:
  very:
    nested:
      variable:
        key: value
```
```python
@propeties(filename="config.yaml", root="some.very.nested.variable")
class Config:
    key: str
```
* Overriding default values with `override_default=True`
* Type casting for primitive types. Nested types will be added soon.
* Case ignoring by default is true. You can switch off this option.
