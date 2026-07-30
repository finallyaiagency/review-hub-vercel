from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CourseResourcesTest(unittest.TestCase):
    def resources(self) -> dict[str, object]:
        script = "const fs=require('fs'),vm=require('vm');const c={window:{}};vm.runInNewContext(fs.readFileSync('course-resources.js','utf8'),c);console.log(JSON.stringify(c.window.FDE_CHAPTER_RESOURCES));"
        output = subprocess.check_output(['node', '-e', script], cwd=ROOT, text=True)
        return json.loads(output)

    def test_every_chapter_has_a_youtube_resource(self) -> None:
        resources = self.resources()
        self.assertEqual({str(number) for number in range(1, 31)}, set(resources))
        for chapter, resource in resources.items():
            video = resource['video']
            self.assertTrue(video['title'], chapter)
            self.assertRegex(video['url'], r'^https://www\.youtube\.com/watch\?v=[\w-]{11}$')

    def test_replay_entries_reference_retained_audio(self) -> None:
        resources = self.resources()
        replay_chapters = {chapter for chapter, resource in resources.items() if 'audio' in resource}
        self.assertEqual({'10', '11', '13'}, replay_chapters)
        for chapter in replay_chapters:
            audio = resources[chapter]['audio']
            self.assertTrue((ROOT / audio['url']).is_file(), chapter)
            self.assertGreater((ROOT / audio['url']).stat().st_size, 0, chapter)


if __name__ == '__main__':
    unittest.main()
