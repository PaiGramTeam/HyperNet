from enum import Enum


class EndfieldEquipProperties(str, Enum):
    """
    枚举类，表示 Endfield 装备的属性。

    属性值:
        ATK: 攻击力
        MAX_HP: 生命值
        CRITICAL_RATE: 暴击率
        PHYSICAL_AND_SPELLINFLICTION_ENHANCE: 源石技艺强度
        HEAL_OUTPUT_INCREASE: 治疗效率加成
        PHYSICAL_DAMAGE_INCREASE: 物理伤害加成
        ULTIMATE_SP_GAIN_SCALAR: 终结技充能效率
        NORMAL_ATTACK_DAMAGE_INCREASE: 普通攻击伤害加成
        NORMAL_SKILL_DAMAGE_INCREASE: 战技伤害加成
        COMBO_SKILL_DAMAGE_INCREASE: 连携技伤害加成
        ULTIMATE_SKILL_DAMAGE_INCREASE: 终结技伤害加成
        DAMAGE_TO_BROKEN_UNIT_INCREASE: 对失衡目标伤害加成
        MAIN_ABILITY: 主能力
        CRYST_AND_PULSE_DAMAGE_INCREASE: 寒冷和电磁伤害加成
        ALL_SKILL_DAMAGE_INCREASE: 所有技能伤害加成
        SUB_ABILITY: 副能力
        ALL_DAMAGE_TAKEN_SCALAR: 全伤害减免
        FIRE_AND_NATURAL_DAMAGE_INCREASE: 灼热和自然伤害加成
        SPELL_DAMAGE_INCREASE: 法术伤害加成
    """

    ATK = "攻击力"
    MAX_HP = "生命值"
    CRITICAL_RATE = "暴击率"
    PHYSICAL_AND_SPELLINFLICTION_ENHANCE = "源石技艺强度"
    HEAL_OUTPUT_INCREASE = "治疗效率加成"
    PHYSICAL_DAMAGE_INCREASE = "物理伤害加成"
    ULTIMATE_SP_GAIN_SCALAR = "终结技充能效率"
    NORMAL_ATTACK_DAMAGE_INCREASE = "普通攻击伤害加成"
    NORMAL_SKILL_DAMAGE_INCREASE = "战技伤害加成"
    COMBO_SKILL_DAMAGE_INCREASE = "连携技伤害加成"
    ULTIMATE_SKILL_DAMAGE_INCREASE = "终结技伤害加成"
    DAMAGE_TO_BROKEN_UNIT_INCREASE = "对失衡目标伤害加成"
    MAIN_ABILITY = "主能力"
    CRYST_AND_PULSE_DAMAGE_INCREASE = "寒冷和电磁伤害加成"
    ALL_SKILL_DAMAGE_INCREASE = "所有技能伤害加成"
    SUB_ABILITY = "副能力"
    ALL_DAMAGE_TAKEN_SCALAR = "全伤害减免"
    FIRE_AND_NATURAL_DAMAGE_INCREASE = "灼热和自然伤害加成"
    SPELL_DAMAGE_INCREASE = "法术伤害加成"

    @classmethod
    def parse_from_str(cls, value: str) -> "EndfieldEquipProperties":
        """
        从字符串解析出对应的 EndfieldEquipProperties 枚举值。

        参数:
            value (str): 输入的字符串值。

        返回:
            EndfieldEquipProperties: 对应的枚举值。

        异常:
            ValueError: 如果输入的值无法匹配任何枚举值，则抛出此异常。
        """
        value = value.replace("equip_attr_", "").strip().upper()
        for item in cls:
            if item.name == value:
                return item
        raise ValueError(f"Unknown EndfieldEquipProperties value: {value}")
