from api.helpers import requires_auth
from config import app, db
from database.organization import Organization
from database.role import Role, Roles
from database.user import User, UserSchema
from database.session import Session
from flask import jsonify, request
from sqlalchemy import or_


@app.route('/organization/board/<path:org_id>', methods=['GET'])
def show_board(org_id):
    """ Search in role, if role  = 1 is admins, else skip. Print all admins out"""
    all_roles = Role.query.filter(Role.organization_id == org_id,
                                     or_(Role.role == Roles.ADMIN, Role.role == Roles.CHAIRMAN)).all()
    result = []
    for eachRole in all_roles:
        user_name = User.query.filter(User.user_id == eachRole.user_id).first()
        data = {
            'name': user_name.name,
            'email': user_name.email,
            'role': str(eachRole.role).split(".")[1]
        }
        result.append(data)
        print("DEBUG", result)
    return jsonify({"success": True, "board": result})


@app.route('/organization/make_admin/<path:org_id>', methods=['POST'])
@requires_auth
def make_admin(org_id):
    sessionObj = request.session
    current_role = Role.query.filter_by(organization_id=org_id, user_id=sessionObj.user_id).first()
    print("DEBUG....")
    print(current_role)
    if not current_role:
        return jsonify(message='You do not allow to do anything', success=False)
    else:
        # Check if the user is chairman or admin.
        if current_role.role == Roles.CHAIRMAN:
            input_data = request.json
            new_role_email = input_data['email']
            new_user = User.query.filter_by(email=new_role_email).first()
            # check if the new_user is already in board
            board_role = Role.query.filter(Role.user_id == new_user.user_id,
                                           Role.organization_id == org_id,
                                           Role.role != Roles.MEMBER).first()
            # 1 ADMIN -> board_role not None
            # 2 CHAIRMAN -> board_role not None
            # MEMBER or out side -> can able to make admin
            if board_role:
                return jsonify(message='New user is already on board', success=False)

            new_admin = Role(user_id=new_user.user_id,
                             organization_id=org_id,
                             role=Roles.ADMIN)
            result = {'message': new_user.name + " is our new Admin",
                      'success': True}
            db.session.add(new_admin)
            db.session.commit()
            return jsonify(result)
        else:
            return jsonify(message='You do not allow to make admin', success=False)


@app.route('/admins/remove_admin/<path:org_id>', methods=['DELETE'])
@requires_auth
def remove_admin(org_id):
    sessionObj = request.session
    current_role = Role.query.filter_by(organization_id=org_id, user_id=sessionObj.user_id).first()
    print("DEBUG....")
    print(current_role)
    if not current_role:
        return jsonify(message='You do not allow to do anything', success=False)
    else:
        # Check if the user is chairman or admin.
        if current_role.role == Roles.CHAIRMAN:
            input_data = request.json

            new_role_email = input_data['email']
            wanted_user = User.query.filter_by(email=new_role_email).first()
            user_role = Role.query.filter(Role.user_id==wanted_user.user_id,
                                          Role.organization_id==org_id).first()
            if user_role.role == Roles.ADMIN:
                db.session.delete(user_role)
                db.session.commit()
                return jsonify(message=wanted_user.name + ' is no longer an admin', success=True)
            else:
                return jsonify(message='This user is not an admin', success=False)

        else:
            return jsonify(message='You do not allow to remove admin', success=False)
