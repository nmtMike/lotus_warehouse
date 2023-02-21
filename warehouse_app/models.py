from warehouse_app import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from flask_login import UserMixin
from sqlalchemy.orm import Session

url_object = URL.create(
    "postgresql",
    username="lotus",
    password="lotus",
    host="localhost",
    port="5433",
    database="lotusdb")

engine = create_engine(url_object, pool_pre_ping=True)
session = Session(engine)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost',backref='author',lazy=True)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"
    
class SanPham(db.Model):
    __tablename__ = 'san_pham'

    id_san_pham = db.Column(db.Integer, primary_key=True)
    ma_san_pham = db.Column(db.String(255), nullable=False)
    ten_san_pham = db.Column(db.String(255), nullable=False)
    don_vi_tinh = db.Column(db.String(255), nullable=False)
    nhom_vthh = db.Column(db.String(255), nullable=False)
    nha_san_xuat = db.Column(db.String(255))
    so_lo_ma_lo = db.Column(db.String(255), nullable=False)
    han_su_dung = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('ma_san_pham', 'so_lo_ma_lo', name='uq_ma_so_lo'),
    )


class DonHangXuat(db.Model):
    __tablename__ = 'don_hang_xuat'
    
    id_don_hang_xuat = db.Column(db.Integer, primary_key=True)
    ngay = db.Column(db.DateTime, nullable=False)
    ma_don_hang = db.Column(db.String(255), nullable=False, unique=True)
    ma_khach_hang = db.Column(db.String(255), nullable=False)
    dien_giai_chung = db.Column(db.String(400))
    dia_chi_giao_hang = db.Column(db.String(400))
    latest_status = db.Column(db.String(30), nullable=False)
    updator = db.Column(db.String(30), nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)


class ChiTietDonHangXuat(db.Model):
    __tablename__ = 'chi_tiet_don_hang_xuat'

    id_don_hang_xuat = db.Column(db.Integer, db.ForeignKey('don_hang_xuat.id_don_hang_xuat'), nullable=False)
    id_san_pham = db.Column(db.Integer, db.ForeignKey('san_pham.id_san_pham'), nullable=False)
    ma_kho_tinh_trang = db.Column(db.String(255), nullable=False)
    so_luong = db.Column(db.Float, nullable=False)
    id_chi_tiet_don_hang = db.Column(db.Integer, primary_key=True)

    don_hang_xuat = db.relationship('DonHangXuat', backref='chi_tiet_don_hang_xuat')
    san_pham = db.relationship('SanPham', backref='chi_tiet_don_hang_xuat')


class TransactionXuat(db.Model):
    __tablename__ = 'transaction_xuat'
    id_transaction_xuat = db.Column(db.Integer, primary_key=True)
    id_chi_tiet_don_hang = db.Column(db.Integer, db.ForeignKey('chi_tiet_don_hang_xuat.id_chi_tiet_don_hang'), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    updator = db.Column(db.String(255), nullable=False)
    updated_time = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return f"<TransactionXuat(id_transaction_xuat={self.id_transaction_xuat}, id_chi_tiet_don_hang={self.id_chi_tiet_don_hang}, status='{self.status}', updator='{self.updator}', updated_time='{self.updated_time}')>"
    

class Misa(db.Model):
    __tablename__ = 'misa'

    ngay = db.Column(db.TIMESTAMP)
    ma_don_hang = db.Column(db.String(255))
    dien_giai_chung = db.Column(db.String(255))
    ma_khach_hang = db.Column(db.String(255))
    ten_khach_hang = db.Column(db.String(255))
    ma_san_pham = db.Column(db.String(255))
    ten_san_pham = db.Column(db.String(255))
    dvt = db.Column(db.String(255))
    so_lo_ma_lo = db.Column(db.String(255))
    han_su_dung = db.Column(db.Date)
    nhom_VTHH = db.Column(db.String(255))
    ten_nhom_VTHH = db.Column(db.String(255))
    ma_kho = db.Column(db.String(255))
    ma_kho_tinh_trang = db.Column(db.String(255))
    ten_kho = db.Column(db.String(255))
    so_luong_xuat = db.Column(db.Float)
    so_luong_nhap = db.Column(db.Float)
    dia_chi_giao_hang = db.Column(db.String(255))
    updator = db.Column(db.String(255))
    updated_time = db.Column(db.TIMESTAMP)