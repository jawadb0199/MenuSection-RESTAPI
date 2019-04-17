import os

from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

path = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(path, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)


# MenuSection Model
class MenuSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name: str) -> None:
        self.name = name


# MenuSection Schema
class MenuSectionSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'name')


menu_section_schema = MenuSectionSchema(strict=True)
menu_sections_schema = MenuSectionSchema(many=True, strict=True)


@app.route('/menusection', methods=['POST'])
def add_menu_section():
    """
    Add new menu section (POST). Request body must contain JSON field 'name'.

    :return: Response Object. JSON shows if post successful and object that was
    :raises: KeyError: 'name' if request body does not contain 'name' field
    """
    name = request.json['name']

    new_menu_section = MenuSection(name)

    db.session.add(new_menu_section)
    db.session.commit()

    result = menu_section_schema.dump(new_menu_section)
    return jsonify(success=True, MenuSection=result.data)


@app.route('/menusection', methods=['GET'])
def get_menu_sections():
    """
    Get all menusections (GET).

    :return: Response object. JSON shows if get successful and menu sections
    """
    all_menu_sections = MenuSection.query.all()

    result = menu_sections_schema.dump(all_menu_sections)
    return jsonify(success=True, MenuSection=result.data)


@app.route('/menusection/<id>', methods=['GET'])
def get_menu_section(id: int):
    """
    Get menu section by id (GET)

    :param id: id of menu section in db
    :return: Response object. JSON shows get successful and menu section if id exists
    """
    menu_section = MenuSection.query.get(id)
    if not menu_section:
        return jsonify(success=False, MenuSection="No MenuSection with id={}".format(id))

    result = menu_section_schema.dump(menu_section)
    return jsonify(success=True, MenuSection=result.data)


@app.route('/menusection/<id>', methods=['POST'])
def update_menu_section(id: int):
    """
    Update menu section by id (POST). Request body must contain JSON field 'name'.

    :param id: id of menu section to be updated
    :return: Response object. JSON shows if update successful and updated menu section if id exists
    :raises: KeyError: 'name' if request body does not contain 'name' field
    """
    menu_section = MenuSection.query.get(id)
    if not menu_section:
        return jsonify(success=False, MenuSection="No MenuSection with id={}".format(id))

    name = request.json['name']
    menu_section.name = name

    db.session.commit()

    result = menu_section_schema.dump(menu_section)
    return jsonify(success=True, MenuSection=result.data)


@app.route('/menusection/<id>', methods=['DELETE'])
def delete_menu_section(id: int):
    """
    Delete menu section by id (DELETE).

    :param id: id of menu section to be deleted
    :return: Response Object. JSON shows if delete successful.
    """
    menu_section = MenuSection.query.get(id)
    if not menu_section:
        return jsonify(success=False, MenuSection="No MenuSection with id={}".format(id))

    db.session.delete(menu_section)
    db.session.commit()

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(port=5000)
