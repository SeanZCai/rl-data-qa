import html
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def slug(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = text.replace('`', '').replace('*', '')
    return re.sub(r'\s+', '-', re.sub(r'[^\w\s-]', '', html.unescape(text).lower())).strip('-')


class PackageTests(unittest.TestCase):
    def test_entrypoint_metadata(self):
        text = (ROOT / 'SKILL.md').read_text()
        frontmatter = text.split('---', 2)[1]
        self.assertIn('name: rl-data-qa\n', frontmatter)
        self.assertRegex(frontmatter, r'(?m)^description: .{40,}')
        self.assertLess(len(text.split()), 1500)
        self.assertNotRegex(text, r'\[TODO|\[TBD')

    def test_local_links_and_anchors_resolve(self):
        for path in [ROOT / 'SKILL.md', *sorted((ROOT / 'references').glob('*.md'))]:
            text = path.read_text()
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if target.startswith(('https://', 'http://', 'mailto:')):
                    continue
                filename, _, anchor = target.partition('#')
                destination = (path.parent / filename).resolve() if filename else path
                self.assertTrue(destination.is_relative_to(ROOT), (path, target))
                self.assertTrue(destination.is_file(), (path, target))
                if anchor:
                    headings = re.findall(r'^#{1,6} (.+)$', destination.read_text(), re.M)
                    self.assertIn(anchor, {slug(h) for h in headings}, (path, target))

    def test_references_are_discoverable(self):
        seen = set()
        queue = [ROOT / 'SKILL.md']
        while queue:
            path = queue.pop()
            if path in seen:
                continue
            seen.add(path)
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if target.startswith(('https://', 'http://', '#')):
                    continue
                destination = (path.parent / target.split('#')[0]).resolve()
                if destination.suffix == '.md':
                    queue.append(destination)
        self.assertTrue(set((ROOT / 'references').glob('*.md')).issubset(seen))


if __name__ == '__main__':
    unittest.main()
