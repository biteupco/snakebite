import colander

# generic helpers for colander schemas


class CommaList(object):
    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        return [item.strip() for item in cstruct.split(',') if item]


class CommaIntList(CommaList):

    def deserialize(self, node, cstruct):
        return map(int, super(CommaIntList, self).deserialize(node, cstruct))

    @staticmethod
    def is_int_list(node, list):
        error_msg = ('%r is not a valid comma separated list of integers or a single '
           'integer.' % list)

        for item in list:
            if not isinstance(item, int):
                raise colander.Invalid(node, error_msg)
