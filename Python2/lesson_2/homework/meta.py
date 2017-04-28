
__author__ = 'Чепелев Антон'


class OopMagic(type):

    def __new__(cls, cls_name, cls_bases, cls_dict):
        if cls_name == 'BlackPirate':
            cls_dict['id'] = 'Pirates Yarrr'

        attr = {key: value for key, value in
                cls_dict.items() if not key.startswith("__") and
                type(value) is list}
        if not len(attr):
            return type.__new__(cls, cls_name, cls_bases, cls_dict)

        for key, value in attr.items():
            del cls_dict[key]
            cls_dict[cls_name + '_' + key] = value

        return type.__new__(cls, cls_name, cls_bases, cls_dict)


class Journal(metaclass=OopMagic):
    lst = [1, 2, 3]


class BlackPirate(metaclass=OopMagic):
    pass


print(hasattr(Journal, 'lst'))
print(hasattr(Journal, 'Journal_lst'))
print(hasattr(BlackPirate, 'id'))
