import os

import connexion

# Import formats for validation
import have_i_not_been_owned.api.formats

_cwd = os.path.abspath(os.path.dirname(__file__))

connexion_app = connexion.FlaskApp(__name__, specification_dir=os.path.join(_cwd, 'resources', 'schemas'))
connexion_app.add_api('openapi.yaml')

# Expose underlying Flask WSGI app for uWSGI, connexion, et. al
app = connexion_app.app

if __name__ == '__main__':
    connexion_app.run()
