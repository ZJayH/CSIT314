# app.py

from flask import Flask
from config import Config
from extensions import db
from boundary.web_boundary import web_bp
from entities.profile_entity import ProfileEntity
from boundary.admin_account_boundary import admin_account_bp
from boundary.cleaner_boundary import cleaner_bp  # handles /api/admin/accounts
from boundary.homeowner_boundary import homeowner_bp
from flask_migrate import Migrate


migr = Migrate()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    migr.init_app(app, db)

    # 初始化扩展
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(web_bp)
    app.register_blueprint(admin_account_bp)
    app.register_blueprint(cleaner_bp)  # handles /api/admin/accounts
    app.register_blueprint(homeowner_bp)



    # 第一次运行时创建表
    with app.app_context():
        db.create_all()
        ProfileEntity.seed_defaults()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
