from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
import json

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/medidesk'
mongo = PyMongo(app)

@app.errorhandler(404)
def not_found(error=None):
    jsonify
    response = jsonify({
        
        'message' : 'Resource not found ' + request.url,
        'status' : 404
    })
    response.status_code = 404
    return response    

@app.route('/turns/<id>',methods=['POST'])
def create_turn(id):

    cit=mongo.db.Cita.find_one({'_id':int(id)})
    especialidad = cit['especialidad']
    dni=cit['dni_paciente']
    fec_cita=cit['fecha_cita']
    dni_=int(dni)
    per=mongo.db.Persona.find_one({'_id':dni_}) 
    per_nombre = per['nombre']
    per_apellidos = per['apellidos']

    if especialidad == 1:
        s=mongo.db.Audiometria.insert_one({"fecha":fec_cita ,"cita":{"nombre": per_nombre,"apellido": per_apellidos,"dni": dni  },"estado": "A","front": 0})
        return "Se insertó correctamente"

    elif especialidad == 2:
        s=mongo.db.Laboratorio.insert_one({"fecha":fec_cita ,"cita":{"nombre": per_nombre,"apellido": per_apellidos,"dni": dni  },"estado": "A","front": 0})
        return "Se insertó correctamente"

    elif especialidad == 3:
        s=mongo.db.Oftalmologia.insert_one({"fecha":fec_cita ,"cita":{"nombre": per_nombre,"apellido": per_apellidos,"dni": dni  },"estado": "A","front": 0})
        return "Se insertó correctamente"
  
    elif especialidad == 4:
        s=mongo.db.Psicologia.insert_one({"fecha":fec_cita ,"cita":{"nombre": per_nombre,"apellido": per_apellidos,"dni": dni  },"estado": "A","front": 0})
        return "Se insertó correctamente"

    elif especialidad == 5:
        s=mongo.db.Radiologia.insert_one({"fecha":fec_cita ,"cita":{"nombre": per_nombre,"apellido": per_apellidos,"dni": dni  },"estado": "A","front": 0})
        return "Se insertó correctamente"

    elif especialidad == 6:
        s=mongo.db.Espirometria.insert_one({"fecha":fec_cita ,"cita":{"nombre": per_nombre,"apellido": per_apellidos,"dni": dni  },"estado": "A","front": 0})
        return "Se insertó correctamente"

    elif especialidad == 7:
        s=mongo.db.Odontologia.insert_one({"fecha":fec_cita ,"cita":{"nombre": per_nombre,"apellido": per_apellidos,"dni": dni  },"estado": "A","front": 0})
        return "Se insertó correctamente"

    else:
        return not_found()

@app.route('/turns/<esp>',methods=['PUT'])
def delete_turn(esp):

    def audiometria():
        
        mongo.db.Audiometria.update_one({'estado':'E'},{"$set":{"estado":"A"}})
        cita = mongo.db.Audiometria.find_one({'estado': 'P'})
        mongo.db.Audiometria.update_one({'_id':ObjectId(cita['_id'])},{"$set":{"estado":"E"}})
    
    def laboratorio():
        
        mongo.db.Laboratorio.update_one({'estado':'E'},{"$set":{"estado":"A"}})
        cita = mongo.db.Laboratorio.find_one({'estado': 'P'})
        mongo.db.Laboratorio.update_one({'_id':ObjectId(cita['_id'])},{"$set":{"estado":"E"}})
    
    def oftalmologia():
        
        mongo.db.Oftalmologia.update_one({'estado':'E'},{"$set":{"estado":"A"}})
        cita = mongo.db.Oftalmologia.find_one({'estado': 'P'})
        mongo.db.Oftalmologia.update_one({'_id':ObjectId(cita['_id'])},{"$set":{"estado":"E"}})

    def psicologia():

        mongo.db.Psicologia.update_one({'estado':'E'},{"$set":{"estado":"A"}})
        cita = mongo.db.Psicologia.find_one({'estado': 'P'})
        mongo.db.Psicologia.update_one({'_id':ObjectId(cita['_id'])},{"$set":{"estado":"E"}})
        # cita2 = mongo.db.Psicologia.find_one({'estado': 'E'})
        # response = json_util.dumps(cita2)
        # return response
    
    def radiologia():
        
        mongo.db.Radiologia.update_one({'estado':'E'},{"$set":{"estado":"A"}})
        cita = mongo.db.Radiologia.find_one({'estado': 'P'})
        mongo.db.Radiologia.update_one({'_id':ObjectId(cita['_id'])},{"$set":{"estado":"E"}})
    
    def espirometria():
        
        mongo.db.Espirometria.update_one({'estado':'E'},{"$set":{"estado":"A"}})
        cita = mongo.db.Espirometria.find_one({'estado': 'P'})
        mongo.db.Espirometria.update_one({'_id':ObjectId(cita['_id'])},{"$set":{"estado":"E"}})
    
    def odontologia():
        
        mongo.db.Odontologia.update_one({'estado':'E'},{"$set":{"estado":"A"}})
        cita = mongo.db.Odontologia.find_one({'estado': 'P'})
        mongo.db.Odontologia.update_one({'_id':ObjectId(cita['_id'])},{"$set":{"estado":"E"}})
    
    especialidades = {
        1:audiometria,
        2:laboratorio,
        3:oftalmologia,
        4:psicologia,
        5:radiologia,
        6:espirometria,
        7:odontologia
    }

    especialidades.get(int(esp), "Error")()

    return {"message": "Actualizado"}

@app.route('/turns/<id>',methods=['GET'])  
def get_turns(id):
    especialidad = mongo.db.Especialidad.find({'_id':int(id)},{'_id':0,'nombre':1})
    response = json_util.dumps(especialidad)
    value = []
    for item in json.loads(response):
        value.append(item['nombre'])
    nombre = value[0]
    if(nombre == 'Audiometria'):
        citas = mongo.db.Audiometria.find({'estado':'P'})
        response = json_util.dumps(citas)
        return Response(response, mimetype="application/json")
    elif(nombre == 'Laboratorio'):
        citas = mongo.db.Laboratorio.find({'estado':'P'})
        response = json_util.dumps(citas)
        return Response(response, mimetype="application/json")
    elif(nombre == 'Oftalmologia'):
        citas = mongo.db.Oftalmologia.find({'estado':'P'})
        response = json_util.dumps(citas)
        return Response(response, mimetype="application/json")
    elif(nombre == 'Psicologia'):
        citas = mongo.db.Psicologia.find({'estado':'P'})
        response = json_util.dumps(citas)
        return Response(response, mimetype="application/json")
    elif(nombre == 'Radiologia'):
        citas = mongo.db.Radiologia.find({'estado':'P'})
        response = json_util.dumps(citas)
        return Response(response, mimetype="application/json")
    elif(nombre == 'Espirometria'):
        citas = mongo.db.Espirometria.find({'estado':'P'})
        response = json_util.dumps(citas)
        return Response(response, mimetype="application/json")
    elif(nombre == 'Odontologia'):
        citas = mongo.db.Odontologia.find({'estado':'P'})
        response = json_util.dumps(citas)
        return Response(response, mimetype="application/json")   

if __name__ == "__main__":
    app.run(debug=True)

# app = Flask(__name__)
# app.config['MONGO_URI']='mongodb://localhost/medidesk'

# mongo = PyMongo(app)

# @app.route('/citas', methods=['POST'])
# def create_user():
#     # Receiving data
#     id = request.json['_id']
#     especialidad = request.json['especialidad']
#     dni = request.json['dni']

#     if id and especialidad and dni:
#         # hashed_password = generate_password_hash(password)
#         mongo.db.Citas.insert(
#             {'_id': id, 'especialidad': especialidad, 'dni': dni}
#         )
#         response = {
#             'id': id,
#             'especialidad': especialidad,
#             'dni': dni
#         }
#         return response
#     else:
#         return not_found()

#     return {'message': 'received'}

# @app.route('/citas', methods=['GET'])
# def get_citas():
#     citas = mongo.db.Citas.find()
#     response = json_util.dumps(citas)
#     return Response(response, mimetype = 'application/json')

# @app.route('/citas/<id>', methods=['GET'])
# def get_cita(id):
    
#     cita = mongo.db.Citas.find_one({'_id': int(id)})
#     response = json_util.dumps(cita)
#     return Response(response, mimetype = 'application/json')

# @app.route('/citas/<id>', methods=['DELETE'])
# def delete_cita(id):
#     mongo.db.Citas.delete_one({'_id': int(id)})
#     response = jsonify({'message': 'Cita ' + id + ' was Deleted successfully'})
#     return response

# @app.route('/citas/<id>', methods=['PUT'])
# def update_cita(id):
#     id = request.json['_id']
#     especialidad = request.json['especialidad']
#     dni = request.json['dni']
#     print(id)
#     if id and especialidad and dni:
#         # hashed_password = generate_password_hash(password)
#         mongo.db.Citas.update_one({'_id': int(id)}, {'$set':{
#             'especialidad': especialidad,
#             'dni': dni         
#         }})
#         response = jsonify({'message': 'Cita ' + id + ' was Updated successfully'})
#         return response

# @app.errorhandler(404)
# def not_found(error=None):
#     response = jsonify({
#         'message': 'Resource Not Found: ' + request.url,
#         'status': 404
#     })
#     response.status_code = 404
#     return response

# if __name__ == "__main__":
#     app.run(debug=True) 