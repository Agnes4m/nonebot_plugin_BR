from dataclasses import dataclass


@dataclass
class Action:
  action_type: str  # 行动类型，例如 "开枪"、"使用"
  argument: str = ""  # 行动参数，例如 "1"、"刀"

  def __str__(self):  # 方便打印
    return f"{self.action_type} {self.argument}"
