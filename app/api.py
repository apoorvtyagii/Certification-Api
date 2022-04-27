from flask import Flask, Blueprint, jsonify, session, redirect, url_for, flash
from app import app
from app.models import Certifications
from flask_restplus import Api, Resource, fields

# app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
app.register_blueprint(blueprint)
# app.config["SWAGGER_UI_JSONEDITOR"] = True

certificate = api.model(
    "certificate", {
        "certificate": fields.String("enter the name of your certificate...."),
        "experience": fields.String("experience in years...."),
        "certification_date": fields.String("year in which you had this certification done...."),
        "certificate_id": fields.String("certificate id...."),
        "status": fields.String("expired or not (white Expired/Not Expired)...."),
        }
    )
    
@api.route("/allmycertifications")
class Certis(Resource):
    @api.marshal_with(certificate, envelope="Data")
    def get(self): #catchable, idempotent(which changes nothing), safe
        try:
            if Certifications.objects.filter(user_email=session['user']):
                data = Certifications.objects(user_email=session['user'])
                dic = {}    
                r = []
                for i in data: 
                    dic['certificate'] = i['certificate']
                    dic['experience'] = i['experience']
                    dic['certification_date'] = i['certification_date']
                    dic['certificate_id'] = i['certificate_id']
                    dic['status'] = i['status']
                    r.append(dic)
                    dic = {}
                return r
            else:
                return {"result": "No content"}, 204
        except:
            return {"result": "Forbidden"}, 403 

    @api.expect(certificate)
    def post(self): #catchable, not idempotent, not safe
        try:
            if Certifications.objects.filter(certificate_id=str(api.payload['certificate_id'])):
                return {"result": "Certificate already exists, try PATCH if you want to update existing certificate detail"}, 403
                
            else:
                data = Certifications(
                                    certificate = str(api.payload['certificate']), 
                                    experience = str(api.payload['experience']),
                                    status = str(api.payload['status']),
                                    certification_date = str(api.payload['certification_date']),
                                    certificate_id = str(api.payload['certificate_id']),
                                    user_email = session['user'],
                                    )
                data.save()
                return {"result": "Language added"}, 201
        except:
            return {"result": "Forbidden"}, 403 
    
    @api.expect(certificate)
    def put(self): #not catchable, idempotent, not safe #for whole body updation
        try:
            if Certifications.objects.filter(certificate_id=str(api.payload['certificate_id'])):
                update_dic={
                            'certificate': str(api.payload['certificate']), 
                            'experience': str(api.payload['experience']),
                            'status': str(api.payload['status']),
                            'certification_date': str(api.payload['certification_date']),
                            'certificate_id': str(api.payload['certificate_id']),
                            'user_email': session['user'],
                            }
                data = Certifications.objects.get(certificate_id=str(api.payload['certificate_id']))
                data.update(**update_dic)
                return {"result": "certificate updated"}, 201
            else:
                data = Certifications(
                                    certificate = str(api.payload['certificate']), 
                                    experience = str(api.payload['experience']),
                                    status = str(api.payload['status']),
                                    certification_date = str(api.payload['certification_date']),
                                    certificate_id = str(api.payload['certificate_id']),
                                    user_email = session['user'],
                                    )
                data.save()
                return {"result": "certificate added"}, 201
        except:
            return {"result": "Forbidden"}, 403  
    
    @api.doc('update_specific_details_in_a_certificate')
    @api.expect(certificate)
    def patch(self): #not catchable, not idempotent, not safe #to change few attributes of an entity, send that attribute only which you want to update
        try:
            if Certifications.objects.filter(certificate_id=str(api.payload['certificate_id'])):
                data = Certifications.objects.get(certificate_id=str(api.payload['certificate_id']))
                update_dic={
                            'certificate': data.certificate, 
                            'experience': data.experience,
                            'status': data.status,
                            'certification_date': data.certification_date,
                            'certificate_id': data.certificate_id,
                            'user_email': session['user'],
                            }
                for i in api.payload:
                    if i in update_dic:
                        update_dic[i] = api.payload[i]
                data.update(**update_dic)
                return {"result": "certificate updated"}, 201
            else:
                return {"result": "certificate does not exist: No Content"}, 204
        except:
            return {"result": "Forbidden"}, 403 


@api.route('/<certificate_id>')
@api.response(404, 'certificate not found')
@api.param('certificate_id', 'The task identifier')
class Certi(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.doc('get_specific_certificate')
    @api.marshal_with(certificate)
    def get(self, certificate_id):
        if Certifications.objects.filter(user_email=session['user']):
            if Certifications.objects.filter(certificate_id=certificate_id):
                data = Certifications.objects(certificate_id=certificate_id)
                dic = {}    
                r = []
                for i in data: 
                    dic['certificate'] = i['certificate']
                    dic['experience'] = i['experience']
                    dic['certification_date'] = i['certification_date']
                    dic['certificate_id'] = i['certificate_id']
                    dic['status'] = i['status']
                    r.append(dic)
                    dic = {}
                return r
            else:
                return {"result": "No content"}, 204
        else:
            return {"result": "Forbidden"}, 403

    @api.doc('delete_specific_certificate')
    @api.response(204, 'certificate deleted')
    def delete(self, certificate_id):
        if Certifications.objects.filter(user_email=session['user']):
            if Certifications.objects.filter(certificate_id=certificate_id):
                data = Certifications.objects.get(certificate_id=certificate_id)
                data.delete()
                return '', 204
            else:
                return {"result": "No content"}, 204
        else:
            return {"result": "Forbidden"}, 403

    # @api.doc('update_specific_details_in_a_certificate')
    # @api.response(201, 'certificate updated')
    # def patch(self, certificate_id):
    #     if Certifications.objects.filter(user_email=session['user']):
    #         if Certifications.objects.filter(certificate_id=certificate_id):
    #             data = Certifications.objects.get(certificate_id=certificate_id)
    #             update_dic={
    #                         'certificate': data.certificate, 
    #                         'experience': data.experience,
    #                         'status': data.status,
    #                         'certification_date': data.certification_date,
    #                         'certificate_id': data.certificate_id,
    #                         'user_email': session['user'],
    #                         }
    #             for i in api.payload:
    #                 if i in update_dic:
    #                     update_dic['i'] = api.payload['i']
    #             data.update(**update_dic)
    #             # data.update(**update_dic)
    #             return "", 201
    #         else:
    #             return {"result": "certificate does not exist: No Content"}, 204
    #     else:
    #         return {"result": "Forbidden"}, 403