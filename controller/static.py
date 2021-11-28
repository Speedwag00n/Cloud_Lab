import datetime
import os
import random

import flask_login
from PIL import Image
from flask import render_template, Blueprint, redirect, url_for, flash, request, send_file
from flask_login import login_required

from app import db
from form.image import AddImageForm, EditImageForm
from model.image import ImageModel, Tag

static_bp = Blueprint(
    'static_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@static_bp.route('/images', methods=['GET', 'POST'])
@login_required
def get_images():
    title = 'Your images gallery'
    user_id = flask_login.current_user.id
    images = db.session.query(ImageModel).filter(ImageModel.owner_id == user_id).all()
    return render_template('index.html', images=images, title=title)


@static_bp.route('/images/<tag_name>', methods=['GET'])
@login_required
def get_images_by_tag(tag_name):
    title = 'Found images by tag "{}"'.format(tag_name)
    user_id = flask_login.current_user.id
    images = db.session.query(ImageModel).filter(ImageModel.owner_id == user_id).filter(ImageModel.tags.any(Tag.name == tag_name)).all()

    return render_template('index.html', images=images, title=title)


@static_bp.route('/images/view/<image_id>', methods=['GET'])
@login_required
def get_image_info(image_id):
    title = 'Image information'
    user_id = flask_login.current_user.id
    image = db.session.query(ImageModel).get(image_id)

    if image:
        return render_template('image_full_info.html', image_info=image, title=title)
    else:
        return redirect(url_for('static_bp.get_images'))


@static_bp.route('/images/download/<image_id>', methods=['GET'])
@login_required
def download_image(image_id):
    image = db.session.query(ImageModel).get(image_id)
    from app import instance_path
    user_name = flask_login.current_user.username
    target_path = os.path.join(instance_path, 'images', user_name)

    extension = image.image_name.split(".")[-1]
    image_name = image.name + '.' + extension

    return send_file(os.path.join(target_path, image.image_name), as_attachment=True, download_name=image_name)


@static_bp.route('/images/raw/<image_id>', methods=['GET'])
@login_required
def show_image(image_id):
    image = db.session.query(ImageModel).get(image_id)
    from app import instance_path
    user_name = flask_login.current_user.username
    target_path = os.path.join(instance_path, 'images', user_name)

    extension = image.image_name.split(".")[-1]
    image_name = image.name + '.' + extension

    return send_file(os.path.join(target_path, image.image_name), download_name=image_name)


@static_bp.route('/images/add', methods=['GET', 'POST'])
@login_required
def add_image():
    title = "Upload new image"

    form = AddImageForm()

    if form.validate_on_submit():
        image = ImageModel(name=form.name.data)

        if form.tags.data:
            processed_tags = __prepare_tags__(form.tags.data)

            if processed_tags is not None:
                image.tags = processed_tags
            else:
                return render_template('add_image.html', form=form, image_id=image.id, title=title)
        else:
            image.tags = []

        image.owner_id = flask_login.current_user.id
        image.creation_date = datetime.datetime.now()

        user_name = flask_login.current_user.username
        extension = form.image.data.filename.split(".")[-1]
        random_hash = random.getrandbits(124)
        image_name = str(random_hash) + '.' + extension

        from app import instance_path
        target_path = os.path.join(instance_path, 'images', user_name)

        if not os.path.exists(target_path):
            os.makedirs(target_path)
        form.image.data.save(os.path.join(target_path, image_name))

        image.image_name = image_name

        pil_image = Image.open(request.files['image'])

        image.width = pil_image.width
        image.height = pil_image.height

        gps_data = pil_image._getexif()[34853]

        image.altitude = float(gps_data[6])
        image.latitude = (float(gps_data[2][0] + gps_data[2][1] / 60 + gps_data[2][2] / 3600)) * (1 if gps_data[1] == 'N' else -1)
        image.longitude = (float(gps_data[4][0] + gps_data[4][1] / 60 + gps_data[4][2] / 3600)) * (1 if gps_data[3] == 'E' else -1)

        db.session.add(image)
        db.session.commit()

        return redirect(url_for('static_bp.get_images'))

    return render_template('add_image.html', form=form, title=title)


@static_bp.route('/images/edit/<image_id>', methods=['GET', 'POST'])
@login_required
def edit_image(image_id):
    title = 'Edit image'
    image = db.session.query(ImageModel).get(image_id)
    form = EditImageForm()

    if request.method == 'GET':
        form.name.data = image.name
        form.tags.data = ' '.join([tag.name for tag in image.tags])
    else:
        if form.validate_on_submit():
            image.name = form.name.data

            if form.tags.data:
                processed_tags = __prepare_tags__(form.tags.data)

                if processed_tags is not None:
                    image.tags = processed_tags
                else:
                    return render_template('edit_image.html', form=form, image_id=image.id, title=title)
            else:
                image.tags = []

            db.session.add(image)
            db.session.commit()

            return redirect(url_for('static_bp.get_image_info', image_id=image.id))

    return render_template('edit_image.html', form=form, image_id=image.id, title=title)


def __prepare_tags__(tags_string):
    processed_tags = []

    tags = tags_string.split()

    for tag_name in tags:
        if tag_name in processed_tags:
            flash("All specified tags must be unique")
            return None
        if len(tag_name) < 2:
            flash("To short tag '{}'".format(tag_name))
            return None

        tag_in_db = db.session.query(Tag).filter(Tag.name == tag_name).all()

        if tag_in_db:
            tag = tag_in_db[0]
        else:
            tag = Tag(name=tag_name)
            db.session.add(tag)

        processed_tags.append(tag)

    return processed_tags


@static_bp.route('/images/delete/<image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    user_id = flask_login.current_user.id
    db.session.query(ImageModel).filter(ImageModel.owner_id == user_id).filter(ImageModel.id == image_id).delete()
    db.session.commit()

    return redirect(url_for('static_bp.get_images'))
