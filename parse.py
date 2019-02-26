from enum import Enum

latex_fmt = {
    'char_list': [
        "#line#",
        "2",
        ".",
        "1",
        "3",
        "1",
        "3",
        "≈",
        "2",
        ".",
        "1",
        "#end#",
        "#end#"
    ],
    'tmpl_format': [],
    'typeface_format': [
        "",
        "",
        "",
        "",
        "",
        "",
        ""
    ]}


class Latex:
    def __init__(self, mt_type, mt_val=None):
        self.mt_type = mt_type
        self.mt_val = mt_val

        self.data = []


class MtPrefix(Enum):
    # 从1开始
    selector = '#M_'


class MtType(Enum):
    line = '#line#'
    char = '#char#'
    tmpl = '#tmpl#'
    end = '#end#'


def format_latex(char_list):
    stack_list = []
    latex_obj = None
    for idx, char in enumerate(char_list):
        if char == MtType.line.value:
            ltx = Latex(mt_type=MtType.line.value)
            if len(stack_list) > 0:
                sk = stack_list.pop()
                sk.data.append(ltx)
                stack_list.append(sk)

            stack_list.append(ltx)
        elif char == MtType.tmpl.value:
            ltx = Latex(mt_type=MtType.tmpl.value)
            sk = stack_list.pop()
            sk.data.append(ltx)

            stack_list.append(sk)
            stack_list.append(ltx)
        elif char == MtType.end.value:
            if len(stack_list) > 1:
                stack_list.pop()
            else:
                latex_obj = stack_list[0]
        else:
            sk = stack_list.pop()
            sk.data.append(char)

            stack_list.append(sk)

    return latex_obj


def parse_latex(latex_obj, tmpl_fmt_list):
    def read_line_data(line_data):
        if len(line_data) == 0:
            return

        tmp_line_str = ""
        for dt in line_data:
            if isinstance(dt, (Latex,)):
                ltx_str = read_latex_obj(dt)
                tmp_line_str += ltx_str
            else:
                tmp_line_str += dt

        return tmp_line_str

    def read_tmpl_data(tmpl_data):
        if len(tmpl_data) == 0:
            return

        tmpl_fmt_str = tmpl_fmt_list.pop()

        tmpl_fmt_item = {}
        for idx, dt in enumerate(tmpl_data):
            fmt_item_key = '{0}{1}'.format(MtPrefix.selector.value, idx+1)

            if isinstance(dt, (Latex,)):
                ltx_str = read_latex_obj(dt)
                tmpl_fmt_item[fmt_item_key] = ltx_str
            else:
                tmpl_fmt_item[fmt_item_key] = dt

        tmpl_str = tmpl_fmt_str.format(**tmpl_fmt_item)
        return tmpl_str

    def read_latex_obj(latex_obj):
        if not isinstance(latex_obj, (Latex)):
            raise ValueError('需要Latex对象')

        if latex_obj.mt_type == MtType.line.value:
            return read_line_data(latex_obj.data)
        elif latex_obj.mt_type == MtType.tmpl.value:
            return read_tmpl_data(latex_obj.data)
        else:
            return ""

    latex_str = read_latex_obj(latex_obj)
    return "$$ " + latex_str + " $$"


latex_obj = format_latex(latex_fmt.get('char_list'))
latex_str = parse_latex(
    latex_obj,
    latex_fmt.get('tmpl_format')
)

print(latex_str)
