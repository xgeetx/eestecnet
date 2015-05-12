from django.contrib.auth.models import User
from django.db.models import ForeignKey
from guardian.shortcuts import assign_perm

from common.models import Applicable
from common.util import Reversable


__author__ = 'Sebastian Wozny'
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your models here.
class BaseTeam(Applicable, Reversable):
    owner = ForeignKey('accounts.Account', editable=False)
    def save(self, **kwargs):
        """
        When an Event is first created two groups should always be created:
        Official participants and organizers. Organizers need the right to modify the event.
        """
        if self.pk:
            result = super(BaseTeam, self).save(**kwargs)
        else:
            result = super(BaseTeam, self).save(**kwargs)
            self.packages.create(name=self.name + '_organizers')
            self.packages.create(name=self.name + '_members')
            self.packages.create(name=self.name + '_alumni')
            from apps.accounts.models import Participation

            Participation.objects.create(confirmed=True, group=self.board,
                                         user=self.owner)
            label = self._meta.object_name
            assign_perm('change_' + label.lower(), self.board, self)
            assign_perm('delete_' + label.lower(), self.board, self)
            assign_perm('view_' + label.lower(), self.board, self)

        return result
    @property
    def organizers(self):
        return self.packages.get(name=self.name + '_organizers')

    @property
    def board(self):
        return self.packages.get(name=self.name + '_organizers')

    @property
    def members(self):
        return self.packages.get(name=self.name + '_members')
class Commitment(BaseTeam):
    pass
class InternationalTeam(BaseTeam):
    pass
