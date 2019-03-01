INDENT = '    '


class Entry():
    """
    Representation of an Entry in an EGG file.
    NOTE: If performance becomes an issue for large scene, consider using __slots__ to save space and speed up Entry
    management.
    """
    def __init__(self, entry_type, name=None, content=[]):
        self.type = entry_type
        if isinstance(content, list):
            self._contents = content
        else:
            self._contents = [content]
        self.name = name

    def count(self):
        return len(self._contents)

    def append(self, entry):
        self._contents.append(entry)

    def format_output(self):
        output_lines = []
        output_lines.append('<{}>{} {{'.format(self.type, '' if not self.name else ' {}'.format(self.name)))
        if self.count() > 1:
            for content in self._contents:
                if isinstance(content, Entry):
                    output_lines.extend([INDENT + line for line in content.format_output()])
                elif isinstance(content, tuple):
                    output_lines.append(INDENT + ' '.join(str(x) for x in content))
                else:
                    output_lines.append(INDENT + content)
            output_lines.append('}')
        elif self.count() == 1:
            content = self._contents[0]
            if isinstance(content, Entry):
                output_lines.extend([INDENT + line for line in content.format_output()])
                output_lines.append('}')
            elif isinstance(content, tuple):
                output_lines[-1] += ' {} }}'.format(' '.join(str(x) for x in content))
            else:
                output_lines[-1] += ' {} }}'.format(content)
        else:
            output_lines[-1] += '}'

        return output_lines

    def __len__(self):
        return self.count()

    def __str__(self):
        return '\n'.join(self.format_output())

    def __repr__(self):
        return '{} "{}" object at {}'.format(self.type, self.name, hex(id(self)))
