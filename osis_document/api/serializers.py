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
from django.core import signing
from rest_framework import serializers

from osis_document.models import Token


class RequestUploadResponseSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="A writing token for the uploaded file")


class ConfirmUploadResponseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(help_text="The uuid of the persisted file upload")


class MetadataSerializer(serializers.Serializer):
    size = serializers.IntegerField(help_text="The size, in bytes, of the file")
    mimetype = serializers.CharField(help_text="The file's mimetype")
    name = serializers.CharField(help_text="The file's name")
    uploaded_at = serializers.DateTimeField(help_text="The file's upload date")
    url = serializers.CharField(help_text="An url for direct access to the raw file")


class ChangeMetadataSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="The file's new name")


class RotateImageSerializer(serializers.Serializer):
    rotate = serializers.IntegerField(help_text="The rotation requested, in degrees, usually 90, 180 or 270")


class RotateImageResponseSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="A fresh writing token for the rotated file")


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    upload_id = serializers.UUIDField(required=True)

    class Meta:
        model = Token
        fields = [
            'token',
            'upload_id',
            'access',
            'expires_at',
        ]

    def create(self, validated_data):
        validated_data['token'] = signing.dumps(str(validated_data['upload_id']))
        return super().create(validated_data)
