from enum import Enum

latex_fmt = {
    'char_list': [
        "#line#",
        "3",
        "4",
        "%",
        "×",
        "#tmpl#",
        "#line#",
        "4",
        "#end#",
        "#line#",
        "7",
        "#end#",
        "#end#",
        "=",
        "#end#",
        "#end#"
    ],
    'tmpl_format': [
        "\\frac {#M_1}  {#M_2} "
    ],
    'typeface_format': [
        "",
        "",
        "",
        "",
        ""
    ]
}


class Latex:
    """
    Latex对象
    """
    def __init__(self, mt_type, mt_val=None):
        self.mt_type = mt_type
        self.mt_val = mt_val

        self.data = []

# Latex需要转义的特殊符号
LATEX_SPECIAL_CHAR = [
    '%'
]

class MtPrefix(Enum):
    """
    Mathtype 自定义前缀
    """
    # 从1开始
    selector = '#M_'


class MtType(Enum):
    """
    Mathtype 自定义类型
    """
    line = '#line#'
    char = '#char#'
    tmpl = '#tmpl#'
    end = '#end#'


def format_latex(char_list):
    """
    出栈入栈算法实现
    :param char_list:
    :return:
    """
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
        """
        组装数据
        :param line_data:
        :return:
        """
        if len(line_data) == 0:
            return

        tmp_line_str = ""
        for dt in line_data:
            if isinstance(dt, (Latex,)):
                ltx_str = read_latex_obj(dt)
                tmp_line_str += ltx_str
            else:
                if dt in LATEX_SPECIAL_CHAR:
                    dt = "\{0}".format(dt)

                tmp_line_str += dt

        return tmp_line_str

    def read_tmpl_data(tmpl_data):
        """
        组装公式
        :param tmpl_data:
        :return:
        """
        if len(tmpl_data) == 0:
            return

        tmpl_fmt_str = tmpl_fmt_list.pop()

        tmpl_fmt_item = {}
        for idx, dt in enumerate(tmpl_data):
            fmt_item_key = '{0}{1}'.format(MtPrefix.selector.value, idx + 1)

            if isinstance(dt, (Latex,)):
                ltx_str = read_latex_obj(dt)
                tmpl_fmt_item[fmt_item_key] = ltx_str
            else:
                tmpl_fmt_item[fmt_item_key] = dt

        print(tmpl_fmt_item, tmpl_fmt_str)
        tmpl_str = tmpl_fmt_str.format(**tmpl_fmt_item)
        return tmpl_str

    def read_latex_obj(latex_obj):
        """
        转发条件
        :param latex_obj:
        :return:
        """
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
