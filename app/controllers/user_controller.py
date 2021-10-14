from flask import request, jsonify, current_app
from http import HTTPStatus
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import sqlalchemy
from app.exc import user_error as UserErrors
import psycopg2

from app.models.user_model import UserModel
from app.models.anime_model import AnimeModel
from app.services import user_service as Users
from app.services.imgur_service import upload_image


def create():
    try:
        new_user = Users.create_user(request.json)

        session = current_app.db.session

        session.add(new_user)
        session.commit()

        return jsonify(new_user), HTTPStatus.CREATED
    except TypeError as e:
        return {'msg': str(e)}, HTTPStatus.BAD_REQUEST

    except sqlalchemy.exc.IntegrityError as e:
    
        if type(e.orig) == psycopg2.errors.NotNullViolation:
            return {'msg': str(e.orig).split('\n')[0]}, HTTPStatus.BAD_REQUEST
        
        if type(e.orig) == psycopg2.errors.UniqueViolation:
            return {'msg': 'User already exists'}, HTTPStatus.BAD_REQUEST

    except UserErrors.InvalidUsernameError:
         return {"msg": "Username already exists"}, HTTPStatus.BAD_REQUEST


def get_user(id: int):
    try:        
        found_user = UserModel.query.get(id)
        if found_user == None:
            return jsonify([])
        return jsonify({
            'username': found_user.username,
            'avatar_url': found_user.avatar_url
        })

    except (sqlalchemy.exc.NoResultFound, UserErrors.InvalidPasswordError):
        return {'msg': 'User not found'}, HTTPStatus.BAD_REQUEST


@jwt_required()
def get_users():
    return jsonify(UserModel.query.all()), HTTPStatus.OK


def login():
    data = request.json
    try:
        found_user: UserModel = UserModel.query.filter_by(email=data['email']).one()
        found_user.verify_password(data['password'])

        access_token = create_access_token(identity=found_user)

        return {'access_token': access_token}, HTTPStatus.OK

    except (sqlalchemy.exc.NoResultFound, UserErrors.InvalidPasswordError):
        return {'msg': 'Incorrect email or password'}, HTTPStatus.BAD_REQUEST


@jwt_required()
def update():
    data = request.json
    try:
        found_user = get_jwt_identity()
        data.pop('password')
        UserModel.query.filter_by(id=found_user['id']).update(data)
        
        session = current_app.db.session
        session.commit() 

        output = UserModel.query.get(found_user['id'])

        return jsonify(output), HTTPStatus.OK
    except sqlalchemy.exc.InvalidRequestError as e:
        return {'msg': e.args[0].split('\"')[-2] + ' is invalid'}, HTTPStatus.BAD_REQUEST


@jwt_required()
def update_password():
    data = request.json
    try:
        found_user = UserModel.query.get(get_jwt_identity()['id'])
        found_user.verify_password(data['password'])
        found_user.password = data['newPassword']

        session = current_app.db.session

        session.add(found_user)
        session.commit()

        return {'msg': 'Password updated'}, HTTPStatus.OK
    except sqlalchemy.exc.InvalidRequestError as e:
        return {'msg': e.args[0].split('\"')[-2] + ' is invalid'}, HTTPStatus.BAD_REQUEST
    
    except (sqlalchemy.exc.NoResultFound, UserErrors.InvalidPasswordError):
        return {'msg': 'Incorrect password'}, HTTPStatus.BAD_REQUEST
    
    except KeyError as e:
        return {'msg': f'{str(e.args[0])} is missing'}


@jwt_required()
def delete_self():
    found_user = get_jwt_identity()

    user_to_delete: UserModel = UserModel.query.get(found_user['id'])

    session = current_app.db.session
    session.delete(user_to_delete)
    session.commit()

    return {"msg": "User deleted"}, HTTPStatus.OK


@jwt_required()
def delete(id: int):
    try:
        Users.verify_admin()

        user_to_delete: UserModel = UserModel.query.get(id)

        session = current_app.db.session
        session.delete(user_to_delete)
        session.commit()

        return {"msg": "User deleted"}, HTTPStatus.OK        
    except UserErrors.InvalidPermissionError as e:
        return e.message, HTTPStatus.UNAUTHORIZED

    except sqlalchemy.exc.NoResultFound:
        return {'msg': 'User not found'}, HTTPStatus.BAD_REQUEST


@jwt_required()
def promote():
    data = request.json
    try:
        Users.verify_admin()

        UserModel.query.filter_by(email=data['email']).update({'permission': 'mod'})

        session = current_app.db.session
        session.commit() 

        return '', HTTPStatus.OK
    except UserErrors.InvalidPermissionError as e:
        return e.message, HTTPStatus.UNAUTHORIZED


@jwt_required()
def demote():
    data = request.json
    try:
        Users.verify_admin()

        UserModel.query.filter_by(email=data['email']).update({'permission': 'user'})

        session = current_app.db.session
        session.commit() 

        return '', HTTPStatus.OK
    except UserErrors.InvalidPermissionError as e:
        return e.message, HTTPStatus.UNAUTHORIZED


@jwt_required()
def get_mods():
    all_users = UserModel.query.all()

    output = [user for user in all_users if user.permission == 'mod']

    return jsonify(output)


@jwt_required()
def post_favorite(anime_id: int):
    found_user = get_jwt_identity()

    try:
        anime = AnimeModel.query.get(anime_id)
        user = UserModel.query.get(found_user['id'])

        if anime in user.favorites:
            raise UserErrors.InvalidFavoriteError

        user.favorites.append(anime)

        session = current_app.db.session
        session.commit() 

        return '', HTTPStatus.OK
    except UserErrors.InvalidFavoriteError:
        return {'msg': f'User has already favorited {anime.name}'}, HTTPStatus.BAD_REQUEST


@jwt_required()
def get_favorites():
    args = request.args
    try:
        page = 1 if 'page' not in args else int(args['page'])
        size = 10 if 'size' not in args else int(args['size'])

        found_user = get_jwt_identity()
        query = UserModel.query.get(found_user['id'])

        paginated = []
        for index, item in enumerate(query.favorites):
            if index >= (page-1) * size and index < page * size:
                paginated.append(item)

        output = [{'id': anime.id, 'name': anime.name} for anime in paginated]

        return jsonify(output), HTTPStatus.OK
    except ValueError:
        return {'msg': 'Arguments should be integers'}, HTTPStatus.BAD_REQUEST


@jwt_required()
def delete_favorite(anime_id: int):
    try:
        found_user = get_jwt_identity()

        anime = AnimeModel.query.get(anime_id)
        user = UserModel.query.get(found_user['id'])

        index = user.favorites.index(anime)
        user.favorites.pop(index)

        session = current_app.db.session
        session.commit() 

        return '', HTTPStatus.OK
    except ValueError:
        return {'msg': f'The user did not favorite {anime.name}'}, HTTPStatus.BAD_REQUEST


@jwt_required()
def update_avatar():
    found_user = get_jwt_identity()
    image_url  = upload_image(request.files['image'])
    
    UserModel.query.filter_by(id=found_user['id']).update({'avatar_url': image_url})

    session = current_app.db.session
    session.commit()

    return {"avatar_url": image_url}, HTTPStatus.OK

    