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

class Certifications(Document):
    certificate = StringField(max_length=50)
    experience = StringField(max_length=50)
    certification_date = StringField(max_length=50)
    certificate_id = StringField(max_length=50, required=True)
    status = StringField(max_length=50)
    user_email = EmailField(max_length=50)

    def to_json(self):
        return {
            'certificate': self.certificate,
            'experience': self.experience,
            'certification_date': self.certification_date,
            'certificate_id': self.certificate_id,
            'status': self.status,
            'user_email': self.user_email,
        }