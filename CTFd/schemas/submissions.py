from sqlalchemy.sql.expression import union_all
from marshmallow import fields, post_load, validate, ValidationError
from marshmallow_sqlalchemy import field_for
from CTFd.schemas.challenges import ChallengeSchema
from CTFd.models import ma, Submissions
from CTFd.utils import string_types


class SubmissionSchema(ma.ModelSchema):
    challenge = fields.Nested(ChallengeSchema, only=['name', 'category', 'value'])

    class Meta:
        model = Submissions
        include_fk = True
        dump_only = ('id', )

    views = {
        'admin': [
            'provided',
            'ip',
            'challenge_id',
            'challenge',
            'user',
            'team',
            'date',
            'type',
            'id'
        ],
        'user': [
            'challenge_id',
            'challenge',
            'user',
            'team',
            'date',
            'type',
            'id'
        ]
    }

    def __init__(self, view=None, *args, **kwargs):
        if view:
            if isinstance(view, string_types):
                kwargs['only'] = self.views[view]
            elif isinstance(view, list):
                kwargs['only'] = view

        super(SubmissionSchema, self).__init__(*args, **kwargs)
