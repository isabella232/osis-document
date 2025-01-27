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
from django.urls import path

from .api import views
from .enums import TokenAccess

app_name = 'osis_document'
urlpatterns = [
    path('request-upload', views.RequestUploadView.as_view(), name=views.RequestUploadView.name),
    path('confirm-upload/<path:token>', views.ConfirmUploadView.as_view(), name=views.ConfirmUploadView.name),
    path('read-token/<uuid:pk>', views.GetTokenView.as_view(token_access=TokenAccess.READ.name), name='read-token'),
    path('write-token/<uuid:pk>', views.GetTokenView.as_view(token_access=TokenAccess.WRITE.name), name='write-token'),
    path('metadata/<path:token>', views.MetadataView.as_view(), name=views.MetadataView.name),
    path('change-metadata/<path:token>', views.ChangeMetadataView.as_view(), name=views.ChangeMetadataView.name),
    path('rotate-image/<path:token>', views.RotateImageView.as_view(), name=views.RotateImageView.name),
    path('file/<path:token>', views.RawFileView.as_view(), name=views.RawFileView.name),
]
