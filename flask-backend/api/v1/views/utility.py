"""
Utility functions to reduce DRY codes
"""


def check_attributes(class_name, obj_attrs):
    """
    check required atrributes for POST request of the specified class
    """

    required_class_attrs = {
                            'User': {'firstname', 'lastname', 'email',
                                     'password', 'username'},
                            'Resource': {'description', 'title', 'content'},
                            'Rack': {'description', 'name', 'library_id',
                                     'public'}
                        }

    required_attrs = required_class_attrs.get(class_name)

    diff = required_attrs - obj_attrs
    msg = str(diff).replace('{', '').replace('}', '').replace("'", '')

    if diff and len(diff) > 1:
        msg = msg + ' are'

    if diff:
        return {'error': '{} missing'.format(msg)}
    else:
        return 'OK'
