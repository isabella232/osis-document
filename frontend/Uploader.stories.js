/*
 *
 *   OSIS stands for Open Student Information System. It's an application
 *   designed to manage the core business of higher education institutions,
 *   such as universities, faculties, institutes and professional schools.
 *   The core business involves the administration of students, teachers,
 *   courses, programs and so on.
 *
 *   Copyright (C) 2015-2021 Université catholique de Louvain (http://www.uclouvain.be)
 *
 *   This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   A copy of this license - GNU General Public License - is available
 *   at the root of the source code of this program.  If not,
 *   see http://www.gnu.org/licenses/.
 *
 */

import Uploader from './Uploader';
import { newServer } from 'mock-xmlhttprequest';
import { i18n } from './i18n';

// XMLHttpRequest mock
const server = newServer({
  post: ['/upload', function (xhr) {
    xhr.uploadProgress(4096);
    setTimeout(() => {
      xhr.uploadProgress(4096 * 5);
    }, 1000);
    setTimeout(() => {
      xhr.respond(
        200,
        { 'Content-Type': 'application/json' },
        '{"token": "0123456789"}',
      );
    }, 2000);
  }],
});

export const basic = () => {
  server.install();

  return {
    components: { Uploader },
    template: '<Uploader upload-url="/upload" name="media"/>',
    destroyed () {
      server.remove();
    },
    i18n,
  };
};

export const limited = () => {
  server.install();

  return {
    components: { Uploader },
    template: `
      <Uploader
          upload-url="/upload"
          name="media"
          :max-size="5242880"
          :mimetypes="['image/png','image/jpeg']"
      />
    `,
    destroyed () {
      server.remove();
    },
    i18n,
  };
};

export default {
  title: 'Uploader',
};
