from dataclasses import dataclass


def translate_to_english(chinese_arg):
    """将中文参数转换为英语参数"""

    translation_table = {
        "刀": "knife",
        "手铐": "handcuffs",
        "香烟": "cigarettes",
        "放大镜": "glass",
        "饮料": "drink",
        # ... 更多映射关系
    }
    if chinese_arg in translation_table:
        return translation_table[chinese_arg]
    else:
        return chinese_arg  # 如果找不到对应的英语参数，则返回原始参数


@dataclass
class Action:
    action_type: str  # 行动类型,例如 "开枪"、"使用"
    argument: str = ""  # 行动参数,例如 "1"、"刀"

    def __post_init__(self):
        # 校验 action_type 是否为空
        if not self.action_type:
            raise ValueError("行动类型不能为空")

        # 校验 action_type 是否为允许的类型
        allowed_action_types = ["开枪", "使用"]  # 示例
        if self.action_type not in allowed_action_types:
            raise ValueError(f"行动类型必须为 {allowed_action_types} 中的一种")

        # 对 argument 进行处理，例如去除空格
        self.argument = self.argument.strip()
        allowed_action_args = ["knife", "handcuffs", "cigarettes", "glass", "drink"]

        # 如果 action_type 为“开枪”，argument 必须为数字
        if self.action_type == "开枪":
            if not self.argument.isdigit():
                raise ValueError("“开枪”行动的参数必须为数字")
            self.argument = str(self.argument).strip()
        elif self.action_type == "使用":
            temp_Args = translate_to_english(self.argument)
            if temp_Args not in allowed_action_args:
                raise ValueError(f"“使用”行动的参数必须为{allowed_action_args}中的一种")
            else:
                self.argument = temp_Args

    def __str__(self):  # 方便打印
        return f"{self.action_type} {self.argument}"
