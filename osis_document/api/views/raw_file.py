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

import hashlib

from django.conf import settings
from django.http import FileResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView

from osis_document.api.utils import CorsAllowOriginMixin
from osis_document.models import Upload


class RawFileSchema(AutoSchema):  # pragma: no cover
    def get_responses(self, path, method):
        responses = super().get_responses(path, method)
        responses['200'] = {
            "description": "The raw binary file",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "string",
                        "format": "binary"
                    }
                }
            }
        }
        return responses


class RawFileView(CorsAllowOriginMixin, APIView):
    """Get raw file from a token"""
    name = 'raw-file'
    authentication_classes = []
    permission_classes = []
    schema = RawFileSchema()

    def get(self, *args, **kwargs):
        upload = Upload.objects.from_token(self.kwargs['token'])
        if not upload:
            return Response({
                'error': _("Resource not found")
            }, status.HTTP_404_NOT_FOUND)
        with upload.file.open() as file:
            md5 = hashlib.md5(file.read()).hexdigest()
        if upload.metadata.get('md5') != md5:
            return Response({
                'error': _("MD5 checksum mismatch")
            }, status.HTTP_409_CONFLICT)
        # TODO handle internal nginx redirect based on a setting
        kwargs = {}
        if self.request.GET.get('dl'):
            kwargs = dict(as_attachment=True, filename=upload.metadata.get('name'))
        response = FileResponse(upload.file.open('rb'), **kwargs)
        domain_list = getattr(settings, 'OSIS_DOCUMENT_DOMAIN_LIST', [])
        if domain_list:
            response['Content-Security-Policy'] = "frame-ancestors {};".format(' '.join(domain_list))
            response['X-Frame-Options'] = ";"
        return response
