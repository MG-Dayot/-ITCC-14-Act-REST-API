from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

# Database model
class PetModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Pet(name = {self.name}, species = {self.species}, age = {self.age})"
    

pet_args = reqparse.RequestParser()
pet_args.add_argument('name', type=str, required=True, help='Pet name cannot be blank')
pet_args.add_argument('species', type=str, required=True, help='Species must be identified')
pet_args.add_argument('age', type=int, required=True, help='Age cannot be blank')

petFields = {
    'id':fields.Integer,
    'name':fields.String,
    'species':fields.String,
    'age':fields.Integer,
}

class Pets(Resource):
    @marshal_with(petFields)
    def get(self):
        pets = PetModel.query.all()
        return pets
    
    @marshal_with(petFields)
    def post(self):
        args = pet_args.parse_args()
        pet = PetModel(name=args['name'], species=args['species'], age=args['age'])
        db.session.add(pet)
        db.session.commit()
        pets = PetModel.query.all()
        return pets, 201

class Pet(Resource):
    @marshal_with(petFields)
    def get(self, id):
        pet = PetModel.query.filter_by(id=id).first()
        if not pet:
            abort(404, "Pet not found")
        return pet
    
    @marshal_with(petFields)
    def patch(self, id):
        args = pet_args.parse_args()
        pet = PetModel.query.filter_by(id=id).first()
        if not pet:
            abort(404, "Pet not found")
        pet.name = args['name']
        pet.species = args['species']
        pet.age = args['age']
        db.session.commit()
        return pet
    
    @marshal_with(petFields)
    def delete(self, id):
        pet = PetModel.query.filter_by(id=id).first()
        if not pet:
            abort(404, "Pet not found")
        db.session.delete(pet)
        db.session.commit()
        pets = PetModel.query.all()
        return pets
    
api.add_resource(Pets, '/api/pets')
api.add_resource(Pet, '/api/pets/<int:id>')

if __name__ == '__main__':
    app.run(debug = True)