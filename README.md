# Python Application Properties
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pre-commit: enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat)](https://github.com/pre-commit/pre-commit)


## What is this
This is a simple library to inject non-sensitive configurations like message templates, dictionaries, and lists with required settings into class variables.

## How to install
To install this library just enter:
```shell
pip intall py-app-properties
```

## How To Use
The main purpose of this library is to simplify work with an application config.

Let's assume that you have some email service that requires a couple of message templates (it could be also a dictionary with default HTTP headers and other kinds of mappings).
It'll look like this:
```python
class EmailService:
    CONFIRM_REGISTRATION_TEMPLATE = "Thanks for your registration!"
    RESET_PASSWORD_TEMPLATE = "To reset a password follow the link - {link}"
    # and other templates...
    
    def __init__(self, mail_sender: IMailSender) -> None:
        self._sender = mail_sender
    
    def send_confirm_registration_mail(self, username: str) -> None:
        self._sender.send_mail(username, self.CONFIRM_REGISTRATION_TEMPLATE)
    
    def send_reset_password_email(self, username: str, link: str) -> None:
        template = self.RESET_PASSWORD_TEMPLATE.format(link=link)
        self._sender.send_mail(username, template)
    # and other methods...
```
As you can see, there are some problems connected with storing message templates in class variables:
* Templates could have a big size and that decreases the readability of a whole class.
* It's also hard to maintain different versions of templates.

But if you have config file `my_config.yml` with the content below, you can "inject" variables to the `EmailService` class:
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
    # and other templates...
    
    def __init__(self, mail_sender: IMailSender) -> None:
        self._sender = mail_sender
    
    def send_confirm_registration_mail(self, username: str) -> None:
        self._sender.send_mail(username, self.CONFIRM_REGISTRATION_TEMPLATE)
    
    def send_reset_password_email(self, username: str, link: str) -> None:
        template = self.RESET_PASSWORD_TEMPLATE.format(link=link)
        self._sender.send_mail(username, template)
    # and other methods...
```
And that's all. Just one decorator and a file with application properties.
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

## About contributing
You will make this library better if you open issues or create pull requests with improvements [here](https://github.com/yar-kik/py-app-properties). Also, you can write me directly in a private message if you have some questions or recommendations.
