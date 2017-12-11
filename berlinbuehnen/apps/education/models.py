# -*- coding: UTF-8 -*-
import time
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.urlresolvers import reverse
from django.conf import settings

from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import URLField
from base_libs.utils.misc import get_translation
from base_libs.models.fields import PositionField
from base_libs.middleware.threadlocals import get_current_language
from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify

from berlinbuehnen.apps.locations.models import Location, District

from filebrowser.fields import FileBrowseField

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('trashed', _("Trashed")),
)

COPYRIGHT_RESTRICTION_CHOICES = (
    ('general_use', _("Released for general use")),
    ('protected', _("Released for this and own site only"))
)

TOKENIZATION_SUMMAND = 56436  # used to hide the ids of media files



class DepartmentManager(models.Manager):
    def accessible_to(self, user):
        from berlinbuehnen.apps.locations.models import Location
        if user.has_perm("education.change_department"):
            return self.get_query_set().exclude(status="trashed")

        owned_locations = Location.objects.owned_by(user=user)
        return self.get_query_set().filter(
            location__in=owned_locations,
        ).exclude(status="trashed")

    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        ids = PerObjectGroup.objects.filter(
            content_type__app_label="education",
            content_type__model="department",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True)
        return self.get_query_set().filter(pk__in=ids).exclude(status="trashed")

    def for_newsletter(self):
        return self.filter(
            status="published",
            newsletter=True
        ).order_by('-creation_date')


class Department(CreationModificationMixin, UrlMixin, SlugMixin()):

    location = models.ForeignKey(Location, verbose_name=_("Location"))
    
    title = MultilingualCharField(_("Title"), max_length=255)
    description = MultilingualTextField(_("Description"), blank=True)
    teaser = MultilingualTextField(_("Teaser"), blank=True)

    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    city = models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)

    contact_name = models.CharField(_("Contact Name"), max_length=255, blank=True)
    phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    fax_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    fax_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    fax_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    email = models.EmailField(_("Email"), max_length=255, blank=True)
    website = URLField("Website", blank=True)
    
    districts = models.ManyToManyField(District, verbose_name=_("District"), blank=True)
    newsletter = models.BooleanField(_("Show in newsletter"), default=False)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    objects = DepartmentManager()

    row_level_permissions = True

    class Meta:
        ordering = ['title']
        verbose_name = _("Education department")
        verbose_name_plural = _("Education departments")

    def __unicode__(self):
        return self.title

    def get_url_path(self):
        try:
            path = reverse("department_detail", kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path
            
    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Department),
            )
        except:
            role = PerObjectGroup(
                sysname="owners",
            )
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(role, "title_%s" % lang_code, get_translation("Owners", language=lang_code))
            role.content_object = self
            role.save()

            RowLevelPermission.objects.create_default_row_permissions(
                model_instance=self,
                owner=role,
            )

        if not role.users.filter(pk=user.pk).count():
            role.users.add(user)
    set_owner.alters_data = True

    def remove_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Department),
                )
        except:
            return
        role.users.remove(user)
        if not role.users.count():
            role.delete()
    remove_owner.alters_data = True

    def get_owners(self):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Department),
            )
        except:
            return []
        return role.users.all()

    def get_social_media(self):
        return self.socialmediachannel_set.all()

    def _get_first_image(self):
        if not hasattr(self, '_first_image_cache'):
            self._first_image_cache = None
            qs = self.image_set.all()
            if qs.count():
                self._first_image_cache = qs[0]
        return self._first_image_cache
    first_image = property(_get_first_image)
    
    def get_projects(self):
        return self.department_projects.filter(status="published")
        
    def get_future_projects(self):
        all_projects = self.get_projects()
        projects_with_events = all_projects.filter(projecttime__isnull=False).distinct()
        projects_sorted_events = sorted(projects_with_events, key= lambda t: t.get_next_timestamp())
        projects_without_events = all_projects.filter(projecttime__isnull=True)
        
        result = []
        for project in projects_sorted_events:
            if project.get_next_date():
                result.append(project)
                
        for project in projects_without_events:
            result.append(project)
            
        if len(result):
            return result
        return None

    def is_editable(self, user=None):
        return self.location.is_editable(user=user)

    def is_deletable(self, user=None):
        return self.is_editable(user=user)

    def get_next_item(self):
        lang_code = settings.LANGUAGE_CODE
        field_name = 'title_{}'.format(lang_code)
        try:
            return Department.objects.filter(
                ~models.Q(pk=self.pk),
                status="published",
                **{
                    '{}__gt'.format(field_name): getattr(self, field_name)
                }
            ).order_by(field_name)[0]
        except:
            return None

    def get_previous_item(self):
        lang_code = settings.LANGUAGE_CODE
        field_name = 'title_{}'.format(lang_code)
        try:
            return Department.objects.filter(
                ~models.Q(pk=self.pk),
                status="published",
                **{
                    '{}__lt'.format(field_name): getattr(self, field_name)
                }
            ).order_by('-{}'.format(field_name))[0]
        except:
            return None


class DepartmentMember(CreationModificationDateMixin):
    department = models.ForeignKey(Department, verbose_name=_("Department"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"), blank=True, null=True)
    function = MultilingualCharField(_('Function'), max_length=255, blank=True)

    phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    email = models.EmailField(_("Email"), max_length=255, blank=True)

    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = _("Department team member")
        verbose_name_plural = _("Department team members")

    def __unicode__(self):
        return unicode(self.person)

    def get_function(self):
        return self.function


class Image(CreationModificationDateMixin):
    department = models.ForeignKey(Department, verbose_name=_("Department"))
    path = FileBrowseField(_('File path'), max_length=255, directory="education/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."))
    copyright_restrictions = models.CharField(_('Copyright restrictions'), max_length=20, blank=True, choices=COPYRIGHT_RESTRICTION_CHOICES)
    sort_order = PositionField(_("Sort order"), collection="department")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class SocialMediaChannel(models.Model):
    department = models.ForeignKey(Department)
    channel_type = models.CharField(_("Social media type"), max_length=255, help_text=_("e.g. twitter, facebook, etc."))
    url = URLField(_("URL"), max_length=255)

    class Meta:
        ordering = ['channel_type']
        verbose_name = _("Social media channel")
        verbose_name_plural = _("Social media channels")

    def __unicode__(self):
        return self.channel_type
        
    def get_class(self):
        social = self.channel_type.lower()
        if social == "google+":
            return u"googleplus"
        return social


class PDF(CreationModificationDateMixin):
    department = models.ForeignKey(Department, verbose_name=_("Department"))
    path = FileBrowseField(_('File path'), max_length=255, directory="education/", extensions=['.pdf'], help_text=_("A path to a locally stored PDF file."))
    sort_order = PositionField(_("Sort order"), collection="department")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("PDF")
        verbose_name_plural = _("PDFs")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class ProjectTargetGroup(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Project target group")
        verbose_name_plural = _("Project target groups")


class ProjectFormat(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Project format")
        verbose_name_plural = _("Project formats")

        
class ProjectManager(models.Manager):
    def accessible_to(self, user):
        from berlinbuehnen.apps.locations.models import Location
        if user.has_perm("education.change_project"):
            return self.get_query_set().exclude(status="trashed")
        owned_locations = Location.objects.owned_by(user=user)
        return self.get_query_set().filter(
            departments__location__in=owned_locations,
        ).exclude(status="trashed").distinct()

    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        ids = PerObjectGroup.objects.filter(
            content_type__app_label="education",
            content_type__model="project",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True)
        return self.get_query_set().filter(pk__in=ids).exclude(status="trashed")

    def for_newsletter(self):
        return self.filter(
            status="published",
            newsletter=True
        ).order_by('-creation_date')


class Project(CreationModificationMixin, UrlMixin, SlugMixin()):
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    departments = models.ManyToManyField(Department, verbose_name=_("Educational departments"), blank=True, related_name="department_projects")

    location_title = models.CharField(_("Location title"), max_length=255, blank=True)
    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    city = models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)

    contact_department = models.CharField(_("Contact Department"), max_length=255, blank=True)
    contact_name = models.CharField(_("Contact Name"), max_length=255, blank=True)
    phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    fax_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    fax_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    fax_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    email = models.EmailField(_("Email"), max_length=255, blank=True)
    website = URLField("Website", blank=True)

    age_from = models.PositiveSmallIntegerField(_(u"Age from"), blank=True, null=True)
    age_till = models.PositiveSmallIntegerField(_(u"Age till"), blank=True, null=True)
    participant_count = MultilingualTextField(_("Participant count"), blank=True)
    needs_teachers = models.BooleanField(_("Project needs teachers"), default=False)
    prices = MultilingualTextField(_("Prices"), blank=True)
    free_entrance = models.BooleanField(_("Free entrance"))
    tickets_website = URLField(_("Tickets website"), blank=True, max_length=255)

    special_conditions = MultilingualTextField(_("Special conditions"), blank=True)
    remarks = MultilingualTextField(_("Remarks"), blank=True)
    cooperation = MultilingualTextField(_("Cooperation partners"), blank=True)
    supporters = MultilingualTextField(_("Supporters"), blank=True)
    sponsors = models.ManyToManyField("sponsors.Sponsor", verbose_name=_("Sponsors"), blank=True)

    target_groups = models.ManyToManyField("ProjectTargetGroup", verbose_name=_("Target groups"), blank=True, null=True)
    formats = models.ManyToManyField("ProjectFormat", verbose_name=_("Project formats"), blank=True, null=True)

    newsletter = models.BooleanField(_("Show in newsletter"), default=False)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    objects = ProjectManager()

    row_level_permissions = True

    def get_url_path(self, event=None):
        if event:
            try:
                path = reverse("project_event_detail", kwargs={'slug': self.slug, 'event_id': event.id})
            except:
                # the apphook is not attached yet
                return ""
            else:
                return path
        else:    
            try:
                path = reverse("project_detail", kwargs={'slug': self.slug})
            except:
                # the apphook is not attached yet
                return ""
            else:
                return path

    class Meta:
        ordering = ["-creation_date"]
        verbose_name = _("Educational project")
        verbose_name_plural = _("Educational projects")

    def __unicode__(self):
        return self.title

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Project),
            )
        except:
            role = PerObjectGroup(
                sysname="owners",
            )
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(role, "title_%s" % lang_code, get_translation("Owners", language=lang_code))
            role.content_object = self
            role.save()

            RowLevelPermission.objects.create_default_row_permissions(
                model_instance=self,
                owner=role,
            )

        if not role.users.filter(pk=user.pk).count():
            role.users.add(user)
    set_owner.alters_data = True

    def remove_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Project),
            )
        except:
            return
        role.users.remove(user)
        if not role.users.count():
            role.delete()
    remove_owner.alters_data = True

    def get_owners(self):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Project),
            )
        except:
            return []
        return role.users.all()
        
    def get_next_timestamp(self):
        next_date = self.get_next_date()
        if next_date:
            return time.mktime(next_date.timetuple())
        else:
            return 0
        
    def get_next_date(self):
        next_event = self.get_next_event()
        if next_event:
            return next_event.start
        return None
        
    def get_next_event(self):
        next_events = self.get_next_events()
        if next_events:
            return next_events[0]
        return None
        
    def get_next_events(self):
        today = datetime.today()
        return self.projecttime_set.filter(
            models.Q(end__gte=today) | models.Q(end=None, start__gte=today),
        )
        
    def has_events(self):
        if self.projecttime_set.exists():
            return True
        else:
            return False
        
    def _get_first_image(self):
        if not hasattr(self, '_first_image_cache'):
            self._first_image_cache = None
            qs = self.projectimage_set.all()
            if qs.count():
                self._first_image_cache = qs[0]
        return self._first_image_cache
    first_image = property(_get_first_image)

    def get_social_media(self):
        return self.projectsocialmediachannel_set.all()

    def get_first_department(self):
        departments = self.get_published_departments()
        if departments:
            return departments[0]
        else:
            return None
        
    def get_published_departments(self):
        return self.departments.filter(status="published")

    def duplicate(self, new_values={}):
        import os
        from distutils.dir_util import copy_tree
        from filebrowser.models import FileDescription
        # copy the model
        source_proj = self
        target_proj = Project.objects.get(pk=self.pk)
        target_proj.pk = None

        for key, value in new_values.items():
            setattr(target_proj, key, value)

        target_proj.slug = get_unique_value(Project, better_slugify(target_proj.title_de))
        target_proj.status = "draft"
        target_proj.save()

        # add m2m relationships
        target_proj.departments = source_proj.departments.all()
        target_proj.sponsors = source_proj.sponsors.all()
        target_proj.target_groups = source_proj.target_groups.all()
        target_proj.formats = source_proj.formats.all()

        # copy media directory
        source_media_dir = "education/projects/%s" % source_proj.slug
        target_media_dir = "education/projects/%s" % target_proj.slug
        abs_source_media_path = os.path.join(settings.MEDIA_ROOT, source_media_dir)
        abs_target_media_path = os.path.join(settings.MEDIA_ROOT, target_media_dir)
        if os.path.exists(abs_source_media_path):
            copy_tree(abs_source_media_path, abs_target_media_path)
        for file_desc in FileDescription.objects.filter(file_path__startswith=source_media_dir):
            file_desc.pk = None
            file_desc.file_path = file_desc.file_path.path.replace(source_media_dir, target_media_dir)
            file_desc.save()
        # add m2o relationships
        for social_media in source_proj.projectsocialmediachannel_set.all():
            social_media.pk = None
            social_media.project = target_proj
            social_media.save()
        for video in source_proj.projectvideo_set.all():
            video.pk = None
            video.project = target_proj
            video.save()
        for time in source_proj.projecttime_set.all():
            time.pk = None
            time.project = target_proj
            time.save()
        for image in source_proj.projectimage_set.all():
            image.pk = None
            image.path = image.path.path.replace(source_media_dir, target_media_dir)
            image.project = target_proj
            image.save()
        for pdf in source_proj.projectpdf_set.all():
            pdf.pk = None
            pdf.path = pdf.path.path.replace(source_media_dir, target_media_dir)
            pdf.project = target_proj
            pdf.save()
        for member in source_proj.projectmember_set.all():
            member.pk = None
            member.project = target_proj
            member.save()

        # set ownership
        for owner in source_proj.get_owners():
            target_proj.set_owner(owner)
        return target_proj

    def is_editable(self, user=None):
        if not hasattr(self, "_is_editable_cache"):
            # return True when the first editable department is found
            self._is_editable_cache = any((department.is_editable() for department in self.departments.all()))
        return self._is_editable_cache

    def is_deletable(self, user=None):
        return self.is_editable(user=user)

    def get_previous_item(self):
        try:
            return Project.objects.filter(
                ~models.Q(pk=self.pk),
                creation_date__lt=self.creation_date,
                status="published",
                departments__in=self.departments.all(),
            ).order_by("-creation_date")[0]
        except Exception as e:
            return None

    def get_next_item(self):
        try:
            return Project.objects.filter(
                ~models.Q(pk=self.pk),
                creation_date__gt=self.creation_date,
                status="published",
                departments__in=self.departments.all(),
            ).order_by("creation_date")[0]
        except Exception as e:
            return None


class ProjectTime(CreationModificationMixin, UrlMixin):
    project = models.ForeignKey(Project, verbose_name=_("Project"))
    start = models.DateTimeField(_("Start date and time"))
    end = models.DateTimeField(_("End date and time"), blank=True, null=True)

    class Meta:
        ordering = ["start"]
        verbose_name = _("Project time")
        verbose_name_plural = _("Project times")

    def __unicode__(self):
        return unicode(self.project) + ' ' + self.start.strftime('%Y-%m-%d %H:%M')


class ProjectMember(CreationModificationDateMixin):
    project = models.ForeignKey(Project, verbose_name=_("Project"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"), blank=True, null=True)
    function = MultilingualCharField(_('Function'), max_length=255, blank=True)

    phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    email = models.EmailField(_("Email"), max_length=255, blank=True)

    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = _("Project team member")
        verbose_name_plural = _("Project team members")

    def __unicode__(self):
        return unicode(self.person)

    def get_function(self):
        return self.function


class ProjectImage(CreationModificationDateMixin):
    project = models.ForeignKey(Project, verbose_name=_("Project"))
    path = FileBrowseField(_('File path'), max_length=255, directory="education/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."))
    copyright_restrictions = models.CharField(_('Copyright restrictions'), max_length=20, blank=True, choices=COPYRIGHT_RESTRICTION_CHOICES)
    sort_order = PositionField(_("Sort order"), collection="project")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class ProjectSocialMediaChannel(models.Model):
    project = models.ForeignKey(Project)
    channel_type = models.CharField(_("Social media type"), max_length=255, help_text=_("e.g. twitter, facebook, etc."))
    url = URLField(_("URL"), max_length=255)

    class Meta:
        ordering = ['channel_type']
        verbose_name = _("Social media channel")
        verbose_name_plural = _("Social media channels")

    def __unicode__(self):
        return self.channel_type

    def get_class(self):
        social = self.channel_type.lower()
        if social == "google+":
            return u"googleplus"
        return social

class ProjectPDF(CreationModificationDateMixin):
    project = models.ForeignKey(Project, verbose_name=_("Project"))
    path = FileBrowseField(_('File path'), max_length=255, directory="education/", extensions=['.pdf'], help_text=_("A path to a locally stored PDF file."))
    sort_order = PositionField(_("Sort order"), collection="project")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("PDF")
        verbose_name_plural = _("PDFs")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class ProjectVideo(CreationModificationDateMixin):
    project = models.ForeignKey(Project, verbose_name=_("Project"))
    title = MultilingualCharField(_("Title"), max_length=255)
    link_or_embed = models.TextField(verbose_name=_("Link or embed code"))
    sort_order = PositionField(_("Sort order"), collection="project")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Video/Audio")
        verbose_name_plural = _("Videos/Audios")

    def __unicode__(self):
        return self.title

    def get_embed(self):
        # TODO: return embed code
        return self.link_or_embed

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class ProjectSponsor(CreationModificationDateMixin):
    project = models.ForeignKey(Project, verbose_name=_("Project"), on_delete=models.CASCADE)
    title = MultilingualCharField(_("Title"), max_length=255, blank=True)
    image = FileBrowseField(_("Image"), max_length=255, directory="education/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."), blank=True)
    website = URLField(_("Website"), blank=True)

    class Meta:
        ordering = ["title"]
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")

    def __unicode__(self):
        return self.title or (self.image and self.image.filename) or self.pk
