from flask import Flask, Blueprint, jsonify
from app import app
from app.models import Webapi
from flask_restplus import Api, Resource, fields

# app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
app.register_blueprint(blueprint)
app.config["SWAGGER_UI_JSONEDITOR"] = True


a_language = api.model(
    "Language",
    {"status": fields.String("Status."), "language": fields.String("The language.")},
)
a_language_post = api.model("Language", {"language": fields.String("the language.")})

languages = []
a = None
# python = {"language": "python", "id": 1, "status": "success"}
# languages.append(python)


@api.route("/language")
class Language(Resource):
    @api.marshal_with(a_language, envelope="Data")
    def get(self):
        objects = Webapi.objects()
        dic = {}
        r = []
        for i in objects:
            dic['language'] = i['language']
            dic['id'] = i['lang_id']
            dic['status'] = i['status']
            r.append(dic)
            dic = {}
        return r

    @api.expect(a_language_post)
    def post(self):
        data = Webapi(language=api.payload['language'], 
                    lang_id = str(len(Webapi.objects())+1),
                    status = 'Success')
        data.save()
        return {"result": "Language added"}, 201


# if __name__ == "__main__":
#     app.run(debug=True)
