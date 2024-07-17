# Nutrition App
### To keep your diet less boring and give you full control over what you eat.

This application is for people who want to keep track of their calorie intake and manage their diet.

## Getting started

Go to your project root directory and use commands such as:
```
python -m venv venv
source venv/Scripts/activate
pip install .[dev]
```

>if "source venv/Scripts/activate" doesn't work try out another Pycharm envioronment

You can run the application by creating an instance of App class:
[application](nutrition_app/app/application.py)

```python
from nutrition_app.app.application import App

app = App()
app.register(username="your_username", password="your_password", email="your_email")
app.verify(username="your_username", email="your_email", code="verification_code")
app.login(username="your_username", password="your_password")
app.create_user(name= "your_name", surname="your_surname", age=18, weight=80, height= 180, gender="male")
```





