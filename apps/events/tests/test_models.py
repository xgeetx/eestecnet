from django.core.urlresolvers import reverse_lazy

from django.test import TestCase

from apps.accounts.factories import ParticipationFactory, AccountFactory
from apps.events.serializers import BaseEventSerializer, ExchangeSerializer, \
    TrainingSerializer, WorkshopSerializer
from apps.events.factories import BaseEventFactory, ParticipationConfirmationFactory, \
    ExchangeFactory, TrainingFactory, WorkshopFactory, WorkshopParticipationFactory
from common.models import Confirmable, Confirmation
from common.util import RESTCase, AuditCase


__author__ = 'Sebastian Wozny'
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class TestBaseEvent(RESTCase, TestCase, AuditCase):
    def setUp(self):
        self.object = BaseEventFactory()
        super(TestBaseEvent, self).setUp()
        self.serializer_class = BaseEventSerializer

    def test_applications_work(self):
        k = AccountFactory(email="asdj@sadjo.de")
        p = ParticipationFactory(user=k, group=self.object.officials)
        self.assertFalse(p.user in self.object.participants)
        self.assertFalse(p in self.object.participations)
        self.assertTrue(p.user in self.object.applicants)
        self.assertTrue(p in self.object.applications)
        for c in p.confirmation_set.all():
            c.confirm()
        self.assertFalse(p.user in self.object.applicants)
        self.assertFalse(p in self.object.applications)
        self.assertTrue(p.user in self.object.participants)
        self.assertTrue(p in self.object.participations)
    def test_organizers_can_modify_event(self):
        p = ParticipationFactory(group=self.object.organizers)
        self.assertTrue(p.user.has_perm('change_baseevent', self.object))

    def test_list_events(self):
        self.assert_retrieve(reverse_lazy('baseevent-list'))

    def test_participation_has_application(self):
        p = ParticipationFactory(group=self.object.officials)
        self.assertTrue(p.application)

    def test_participation_has_feedback(self):
        p = ParticipationFactory(group=self.object.officials)
        self.assertTrue(p.feedback)

    def test_applicant_can_modify_application(self):
        p = ParticipationFactory(group=self.object.officials)
        self.assertTrue(p.user.has_perm('change_response', p.application))

    def test_participant_can_modify_feedback(self):
        p = ParticipationFactory(group=self.object.officials)
        self.assertTrue(p.user.has_perm('change_response', p.feedback))


class TestParticipationConfirmation(TestCase):
    def setUp(self):
        self.p = ParticipationConfirmationFactory()
        super(TestParticipationConfirmation, self).setUp()

    def test_polymorphic(self):
        self.assertTrue(self.p in Confirmable.objects.all())
        self.assertTrue(self.p in Confirmation.objects.all())

    def test_accept_participant(self):
        for c in self.p.confirmation_set.all():
            c.confirm()
        self.assertTrue(self.p.confirmed)


class TestExchange(RESTCase, TestCase, AuditCase):
    def setUp(self):
        self.object = ExchangeFactory()
        self.serializer_class = ExchangeSerializer
        super(TestExchange, self).setUp()


class TestTraining(RESTCase, TestCase, AuditCase):
    def setUp(self):
        self.object = TrainingFactory()
        self.serializer_class = TrainingSerializer
        super(TestTraining, self).setUp()


class TestWorkshop(RESTCase, TestCase, AuditCase):
    def setUp(self):
        self.object = WorkshopFactory()
        self.serializer_class = WorkshopSerializer
        super(TestWorkshop, self).setUp()

    def test_organizers_can_modify_event(self):
        p = WorkshopParticipationFactory(group=self.object.organizers)
        self.assertTrue(p.user.has_perm('change_workshop', self.object))