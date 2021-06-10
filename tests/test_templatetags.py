# ##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2021 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
# ##############################################################################
from django.template import Template, Context
from django.test import TestCase, override_settings

from osis_document.tests.factories import PdfUploadFactory


@override_settings(ROOT_URLCONF='osis_document.tests.document_test.urls',
                   OSIS_DOCUMENT_BASE_URL='http://dummyurl.com/')
class TemplateTagsTestCase(TestCase):
    def test_visualizer_does_not_expose_uuid(self):
        stub_uuid = PdfUploadFactory().uuid
        context = Context({
            'values': [stub_uuid]
        })
        rendered = Template(
            '{% load osis_document %}'
            '{% document_visualizer values %}'
        ).render(context)
        self.assertNotIn(str(stub_uuid), rendered)
        self.assertIn('class="document-visualizer"', rendered)
        self.assertIn('http://dummyurl.com/', rendered)

    def test_other_tags(self):
        stub_uuid = PdfUploadFactory().uuid
        context = Context({
            'values': [stub_uuid]
        })
        rendered = Template(
            '{% load osis_document %}'
            '{% for file_uuid in values %}'
            '{% get_metadata file_uuid as metadata %}'
            '{% get_file_url file_uuid as file_url %}'
            '   <a href="{{ file_url }}">'
            '       {{ metadata.name }} ({{ metadata.mimetype }} - {{ metadata.size|filesizeformat }})'
            '   </a>'
            '{% endfor %}'
        ).render(context)
        self.assertNotIn(str(stub_uuid), rendered)
        self.assertIn('http://dummyurl.com/', rendered)
        self.assertIn('application/pdf', rendered)
