from mongoengine import Document, StringField, EmailField


class User(Document):
    name = StringField(max_length=50)
    email = EmailField(required=True)
    password = StringField(max_length=50)

    def to_json(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password
        }

class Webapi(Document):
    language = StringField(max_length=50)
    lang_id = StringField(max_length=50, required=True)
    status = StringField(max_length=50)

    def to_json(self):
        return {
            'language': self.language,
            'lang_id': self.lang_id,
            'status': self.status
        }