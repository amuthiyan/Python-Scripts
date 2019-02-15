WTF_CSRF_ENABLED = True
SECRET_KEY = 'asm'

#configuring path for database
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'webapp.db')
