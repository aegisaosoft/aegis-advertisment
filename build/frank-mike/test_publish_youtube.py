# -*- coding: utf-8 -*-
# Copyright (c) Aegis AO Soft LLC. All rights reserved.
"""Metadata checks for publish_youtube.py -- YouTube rejects these only after the upload."""
import os
import unittest

import publish_youtube as p


class MetadataTest(unittest.TestCase):
    def test_every_video_passes_youtube_limits(self):
        for key, v in p.VIDEOS.items():
            self.assertEqual(p.problems(v), [], key)

    def test_files_exist(self):
        for v in p.VIDEOS.values():
            self.assertTrue(os.path.exists(v['file']), v['file'])
            self.assertTrue(os.path.exists(v['captions']), v['captions'])

    def test_problems_catches_long_title_and_brackets(self):
        v = dict(p.VIDEOS['en'], title='x' * 101, description='a <b>')
        self.assertIn('title over 100 chars', p.problems(v))
        self.assertIn('angle bracket in description', p.problems(v))

    def test_public_and_not_for_kids(self):
        b = p.body(p.VIDEOS['es'])
        self.assertEqual(b['status']['privacyStatus'], 'public')
        self.assertFalse(b['status']['selfDeclaredMadeForKids'])
        self.assertEqual(b['snippet']['defaultAudioLanguage'], 'es-419')


if __name__ == '__main__':
    unittest.main()
