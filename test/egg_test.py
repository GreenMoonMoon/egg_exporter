import unittest

from egg_exporter.egg import Entry, Egg


TEST_STRING_A = '''<CoordinateSystem> { Z-Up }

<VertexPool> box {
    <Vertex> 1 {
        0 1 1
        <UV> { 1 1 }
    }
}

<Group> box {
    <Polygon> {
        <Normal> { 0 -1 0 }
        <VertexRef> {
            3 7 8 4
            <Ref> { box }
        }
    }
}'''

TEST_STRING_B = '''<VertexPool> box {
    <Vertex> 1 {
        0 1 1
        <UV> { 1 1 }
    }
}'''


class EggTestCase(unittest.TestCase):
    def setUp(self):
        self.egg = Entry(None)  # a None entry is considered the root of an egg file.
        super(EggTestCase, self).setUp()

    def tearDown(self):
        self.egg = None
        super(EggTestCase, self).tearDown()

    @unittest.skip
    def test_egg_entry_index(self):
        self.egg.append(Entry('CoordinateSystem', content='Z-Up'))

        pool_entry = Entry('VertexPool', 'box')
        pool_entry.append(Entry('Vertex', 1, [(0, 1, 1), Entry('UV', content=(1, 1))]))
        self.egg.append(pool_entry)

        group_entry = Entry('Group', 'box')
        group_entry.append(
            Entry('Polygon', content=[
                Entry('Normal', content=(0, -1, 0)),
                Entry('VertexRef', content=[(3, 7, 8, 4), Entry('Ref', content='box')]),
            ]),
        )
        self.egg.append(group_entry)

        index = self.egg.index('VertexPool', 'box')
        entry = self.egg[index]
        self.assertEqual(entry, pool_entry)

    def test_egg_entry_format(self):
        test_string = '''<Vertex> 1 {\n    1 1 1\n    <UV> { 1 1 }\n}'''
        entry = Entry('Vertex', 1, [(1, 1, 1), Entry('UV', content=(1, 1))])
        self.assertEqual(str(entry), test_string)

    def test_egg_hierarchy_entry_format(self):
        entry = Entry('VertexPool', 'box')
        entry.append(Entry('Vertex', 1, [(0, 1, 1), Entry('UV', content=(1, 1))]))

        self.assertEqual(str(entry), TEST_STRING_B)

    def test_egg_str(self):
        self.egg.append(Entry('CoordinateSystem', content='Z-Up'))

        pool_entry = Entry('VertexPool', 'box')
        pool_entry.append(Entry('Vertex', 1, [(0, 1, 1), Entry('UV', content=(1, 1))]))
        self.egg.append(pool_entry)

        group_entry = Entry('Group', 'box')
        group_entry.append(
            Entry('Polygon', content=[
                Entry('Normal', content=(0, -1, 0)),
                Entry('VertexRef', content=[(3, 7, 8, 4), Entry('Ref', content='box')]),
            ]),
        )
        self.egg.append(group_entry)

        self.assertEqual(str(self.egg), TEST_STRING_A)
