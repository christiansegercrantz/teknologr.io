import datetime

from django.test import TestCase
from members.models import *
from ldap import LDAPError


class MemberTest(TestCase):
    def setUp(self):
        # Normal person
        self.member1 = Member.objects.create(
            given_names='Foo Bar Baz',
            preferred_name='Foo',
            surname='Tester',
            street_address='Otsvängen 22',
            postal_code='02150',
            city='Esbo',
        )
        # Only one given name
        # No preferred name set
        # Address is not in Finland
        self.member2 = Member.objects.create(
            given_names='Foo Bar Baz',
            surname='Tester',
            street_address='Dr. Martin Luther King Boulevard #78',
            postal_code='',
            city='Williemstad',
            country='CW',
            allow_publish_info=True,
        )
        # Preferred name is not the first name
        # Surname with prefixes
        # Address is incomplete
        self.member3 = Member.objects.create(
            given_names='Foo Bar Baz',
            preferred_name='Baz',
            surname='von der Tester',
            street_address='Otsvängen 22',
            allow_publish_info=True,
            dead=True,
        )

        MemberType.objects.create(
            begin_date=datetime.date(2020, 1, 1),
            type='OM',
            member=self.member2,
        )
        MemberType.objects.create(
            begin_date=datetime.date(2020, 1, 1),
            type='OM',
            member=self.member3,
        )

    def test_get_preferred_name(self):
        self.assertEqual(self.member1.get_preferred_name(), 'Foo')
        self.assertEqual(self.member2.get_preferred_name(), 'Foo')
        self.assertEqual(self.member3.get_preferred_name(), 'Baz')

    def test_get_given_names_with_initials(self):
        self.assertEqual(self.member1.get_given_names_with_initials(), 'Foo B B')
        self.assertEqual(self.member2.get_given_names_with_initials(), 'Foo B B')
        self.assertEqual(self.member3.get_given_names_with_initials(), 'F B Baz')

    def test_get_surname_without_prefixes(self):
        self.assertEqual(self.member1.get_surname_without_prefixes(), 'Tester')
        self.assertEqual(self.member2.get_surname_without_prefixes(), 'Tester')
        self.assertEqual(self.member3.get_surname_without_prefixes(), 'Tester')

    def test_full_name(self):
        self.assertEqual(self.member1.full_name, 'Foo Bar Baz Tester')
        self.assertEqual(self.member2.full_name, 'Foo Bar Baz Tester')
        self.assertEqual(self.member3.full_name, 'Foo Bar Baz von der Tester')

    def test_full_name_for_sorting(self):
        self.assertEqual(self.member1.full_name_for_sorting, 'Tester, Foo Bar Baz')
        self.assertEqual(self.member2.full_name_for_sorting, 'Tester, Foo Bar Baz')
        self.assertEqual(self.member3.full_name_for_sorting, 'Tester, Foo Bar Baz')

    def test_public_full_name(self):
        self.assertEqual(self.member1.public_full_name, 'Foo B B Tester')
        self.assertEqual(self.member2.public_full_name, 'Foo Bar Baz Tester')
        self.assertEqual(self.member3.public_full_name, 'F B Baz von der Tester')

    def test_public_full_name_for_sorting(self):
        self.assertEqual(self.member1.public_full_name_for_sorting, 'Tester, Foo B B')
        self.assertEqual(self.member2.public_full_name_for_sorting, 'Tester, Foo Bar Baz')
        self.assertEqual(self.member3.public_full_name_for_sorting, 'Tester, F B Baz')

    def test_name(self):
        self.assertEqual(self.member1.name, 'Foo Bar Baz Tester')
        self.assertEqual(self.member2.name, 'Foo Bar Baz Tester')
        self.assertEqual(self.member3.name, 'Foo Bar Baz von der Tester')

    def test_address(self):
        self.assertEquals('Otsvängen 22, 02150 Esbo, Finland', self.member1.full_address)

    def test_address_foreign(self):
        self.assertEquals('Dr. Martin Luther King Boulevard #78, Williemstad, Curaçao', self.member2.full_address)

    def test_address_incomplete(self):
        self.assertEquals('Otsvängen 22, Finland', self.member3.full_address)

    def test_str(self):
        self.assertIn('Tester', str(self.member1))
        self.assertIn('Tester', str(self.member2))
        self.assertIn('Tester', str(self.member3))

    def test_member_type(self):
        member = Member(given_names='Svatta', surname='Teknolog')
        member.save()

        # test that there are no membertypes yet
        self.assertEquals('', member.current_member_type)

        # add some member types. First default member type phux
        ph = MemberType(member=member, begin_date=datetime.date(2012, 9, 1))
        ph.save()
        # A 'Phux' is not a real member type and should return ''
        self.assertEquals('', member.current_member_type)
        self.assertFalse(member.isValidMember())

        # Make our person a 'real member'
        om = MemberType(member=member, type='OM', begin_date=datetime.date(2012, 9, 27))
        om.save()
        self.assertEquals('Ordinarie Medlem', member.current_member_type)
        self.assertTrue(member.isValidMember())

        self.assertEquals('Ordinarie Medlem: 2012-09-27->', str(om))

        # Wappen kom, phuxen är inte mera phux!
        ph.end_date = datetime.date(2012, 4, 30)
        ph.save()
        self.assertEquals('Phux: 2012-09-01-2012-04-30', str(ph))
        self.assertFalse(member.shouldBeStalm())

        # Our person became JuniorStÄlM :O
        js = MemberType(member=member, type='JS', begin_date=datetime.date(2017, 10, 15))
        js.save()
        self.assertFalse(member.shouldBeStalm())

        # Our person is now finished with his/her studies
        om.end_date = datetime.date(2019, 4, 30)
        om.save()
        self.assertEquals('Ordinarie Medlem: 2012-09-27-2019-04-30', str(om))

        # member type should be nothing ('') now
        self.assertEquals('', member.current_member_type)
        # and person should become StÄlM now
        self.assertTrue(member.shouldBeStalm())

        fg = MemberType(member=member, type='FG', begin_date=datetime.date(2019, 5, 1))
        fg.save()

        st = MemberType(member=member, type='ST', begin_date=datetime.date(2019, 5, 16))
        st.save()
        self.assertEquals('StÄlM', member.current_member_type)
        self.assertFalse(member.shouldBeStalm())

    def test_saving(self):
        member = Member(
            given_names='Svatta',
            surname='Teknolog',
        )
        member.save()

        # try to cover lines missed by conditions.
        member.username = 'teknosv1'
        member.student_id = '123456'
        member.email = 'svatta@teknolog.fi'
        with self.assertRaises(LDAPError):
            member.save()


class DecorationOwnerShipTest(TestCase):
    def setUp(self):
        member = Member.objects.create(given_names='Foo Bar', preferred_name='Foo', surname='Tester')
        decoration = Decoration.objects.create(name='Test Decoration')
        DecorationOwnership.objects.create(member=member, decoration=decoration, acquired=datetime.date.today())

    def test_str(self):
        dec_ownership = DecorationOwnership.objects.get(pk=1)
        self.assertIn('Test Decoration', str(dec_ownership))
        self.assertIn('Tester', str(dec_ownership))


class DecorationTest(TestCase):
    def setUp(self):
        Decoration.objects.create(name='Test Decoration')

    def test_str(self):
        decoration = Decoration.objects.get(pk=1)
        self.assertIn('Test Decoration', str(decoration))


class GroupTest(TestCase):
    def setUp(self):
        group_type = GroupType.objects.create(name='Group Type')
        Group.objects.create(grouptype=group_type,
                             begin_date=datetime.date(2016, 11, 6), end_date=datetime.date(2016, 11, 8))

    def test_str(self):
        group = Group.objects.get(pk=1)
        self.assertIn('Group Type', str(group))


class GroupTypeTest(TestCase):
    def setUp(self):
        GroupType.objects.create(name='Group Type')

    def test_str(self):
        group_type = GroupType.objects.get(name='Group Type')
        self.assertIn('Group Type', str(group_type))


class FunctionaryTest(TestCase):
    def setUp(self):
        func_type = FunctionaryType.objects.create(name='Functionary Type')
        member = Member.objects.create(given_names='Foo Bar', preferred_name='Foo', surname='Tester')
        Functionary.objects.create(functionarytype=func_type,
                                   member=member, begin_date=datetime.date(2016, 11, 4),
                                   end_date=datetime.date(2016, 11, 6))

    def test_get_str_member(self):
        func = Functionary.objects.get(pk=1)
        self.assertIn('Tester', func._get_str_member())

    def test_get_str_type(self):
        func = Functionary.objects.get(pk=1)
        self.assertIn('Functionary Type', func._get_str_type())

    def test_str(self):
        func = Functionary.objects.get(pk=1)
        self.assertIn('Tester', str(func))
        self.assertIn('Functionary Type', str(func))


class FunctionaryTypeTest(TestCase):
    def setUp(self):
        FunctionaryType.objects.create(name='Functionary Type')

    def test_str(self):
        func_type = FunctionaryType.objects.get(name='Functionary Type')
        self.assertIn('Functionary Type', str(func_type))
