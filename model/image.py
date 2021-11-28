from app import db


image_tag = db.Table('image_tag',
                     db.Column('image_id', db.Integer, db.ForeignKey('image.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                     )


class ImageModel(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    image_name = db.Column(db.String(128), nullable=False)
    owner_id = db.Column('owner_id', db.Integer, db.ForeignKey("users.id"), nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    altitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    tags = db.relationship("Tag", secondary=image_tag, backref=db.backref('tag_id', lazy='dynamic'))


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    tags = db.relationship("ImageModel", secondary=image_tag, backref=db.backref('image_id', lazy='dynamic'))
