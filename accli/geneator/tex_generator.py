# -*-  coding:utf-8 -*-

import os.path
import tempfile

from accli.result_generator import ResultGenerator


class TexGenerator(ResultGenerator):
    def generate(self):
        tmp_dir = tempfile.mkdtemp()
        tmp_filename = os.path.join(tmp_dir, 'output.tex')
        template_tree = os.walk(template_fullpath)

        try:
            for root, _, files in template_tree:
                for f in files:
                    os.system('ln -sf %s %s' % (
                        os.path.join(os.path.abspath(root), f),
                        os.path.join(tmp_dir, f)))
            open(tmp_filename, mode='w', encoding='utf-8').write(output)
            os.system('cd %s; pdflatex output.tex' % tmp_dir)
            os.system('cd %s; mv output.pdf %s' % (tmp_dir, output_filename))
        finally:
            # os.system('rm -rf %s' % tmp_dir)
            pass
