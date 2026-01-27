from typing import Optional

from hypernet.models.base import APIModel, DateTimeField


class EndfieldCharacterKV(APIModel):
    """
    Represents a key-value pair used in various character attributes.

    Attributes:
        key (str): The key of the key-value pair.
        value (str): The value of the key-value pair.
    """

    key: str
    value: str


class EndfieldCharacterSkill(APIModel):
    """
    Represents a skill of an Endfield character.

    Attributes:
        id (str): The unique identifier of the skill.
        name (str): The name of the skill.
        property (EndfieldCharacterKV): The property associated with the skill.
        type (EndfieldCharacterKV): The type of the skill.
        iconUrl (str): The URL of the skill's icon.
        desc (str): The description of the skill.
        descLevelParams (dict): Parameters for the skill's level-based description.
        descParams (dict): Additional parameters for the skill's description.
    """

    id: str
    name: str
    property: EndfieldCharacterKV
    type: EndfieldCharacterKV

    iconUrl: str

    desc: str
    descLevelParams: dict
    descParams: dict


class EndfieldCharacterCharData(APIModel):
    """
    Represents character data for an Endfield character.

    Attributes:
        id (str): The unique identifier of the character.
        name (str): The name of the character.
        profession (EndfieldCharacterKV): The profession of the character.
        property (EndfieldCharacterKV): The property of the character.
        rarity (EndfieldCharacterKV): The rarity of the character.
        weaponType (EndfieldCharacterKV): The weapon type of the character.
        avatarRtUrl (str): The URL of the character's portrait avatar.
        avatarSqUrl (str): The URL of the character's square avatar.
        illustrationUrl (str): The URL of the character's illustration.
        tags (list[str]): Tags associated with the character.
    """

    id: str
    name: str

    profession: EndfieldCharacterKV
    property: EndfieldCharacterKV
    rarity: EndfieldCharacterKV
    weaponType: EndfieldCharacterKV

    avatarRtUrl: str
    avatarSqUrl: str
    illustrationUrl: str

    tags: list[str]


class EndfieldCharacterUserSkill(APIModel):
    """
    Represents a user's skill for an Endfield character.

    Attributes:
        skillId (str): The unique identifier of the skill.
        level (int): The current level of the skill.
        maxLevel (int): The maximum level of the skill.
    """

    skillId: str
    level: int
    maxLevel: int


class EndfieldCharacterEquipSuit(APIModel):
    """
    Represents an equipment suit for an Endfield character.

    Attributes:
        id (str): The unique identifier of the equipment suit.
        name (str): The name of the equipment suit.
        skillDesc (str): The description of the suit's skill.
        skillDescParams (dict): Parameters for the skill description.
        skillId (str): The unique identifier of the suit's skill.
    """

    id: str
    name: str
    skillDesc: str
    skillDescParams: dict
    skillId: str


class EndfieldCharacterEquipData(APIModel):
    """
    Represents data for a piece of equipment.

    Attributes:
        id (str): The unique identifier of the equipment.
        name (str): The name of the equipment.
        rarity (EndfieldCharacterKV): The rarity of the equipment.
        level (EndfieldCharacterKV): The level of the equipment.
        type (EndfieldCharacterKV): The type of the equipment.
        properties (list[str]): The properties of the equipment.
        isAccessory (bool): Whether the equipment is an accessory.
        suit (EndfieldCharacterEquipSuit): The suit associated with the equipment.
        function (str): The function of the equipment.
        pkg (str): The package of the equipment.
        iconUrl (str): The URL of the equipment's icon.
    """

    id: str
    name: str

    rarity: EndfieldCharacterKV
    level: EndfieldCharacterKV
    type: EndfieldCharacterKV
    properties: list[str]
    isAccessory: bool
    suit: EndfieldCharacterEquipSuit

    function: str
    pkg: str
    iconUrl: str


class EndfieldCharacterEquip(APIModel):
    """
    Represents an equipment item for an Endfield character.

    Attributes:
        equipId (str): The unique identifier of the equipment.
        equipData (EndfieldCharacterEquipData): The data associated with the equipment.
    """

    equipId: str
    equipData: EndfieldCharacterEquipData


class EndfieldCharacterTacticalData(APIModel):
    """
    Represents tactical data for an Endfield character.

    Attributes:
        id (str): The unique identifier of the tactical item.
        name (str): The name of the tactical item.
        rarity (EndfieldCharacterKV): The rarity of the tactical item.
        activeEffect (str): The active effect of the tactical item.
        activeEffectParams (dict): Parameters for the active effect.
        activeEffectType (EndfieldCharacterKV): The type of the active effect.
        passiveEffect (str): The passive effect of the tactical item.
        passiveEffectParams (dict): Parameters for the passive effect.
        iconUrl (str): The URL of the tactical item's icon.
    """

    id: str
    name: str

    rarity: EndfieldCharacterKV

    activeEffect: str
    activeEffectParams: dict
    activeEffectType: EndfieldCharacterKV

    passiveEffect: str
    passiveEffectParams: dict

    iconUrl: str


class EndfieldCharacterTactical(APIModel):
    """
    Represents a tactical item for an Endfield character.

    Attributes:
        tacticalItemId (str): The unique identifier of the tactical item.
        tacticalItemData (EndfieldCharacterTacticalData): The data associated with the tactical item.
    """

    tacticalItemId: str
    tacticalItemData: EndfieldCharacterTacticalData


class EndfieldCharacterWeaponData(APIModel):
    """
    Represents weapon data for an Endfield character.

    Attributes:
        id (str): The unique identifier of the weapon.
        name (str): The name of the weapon.
        rarity (EndfieldCharacterKV): The rarity of the weapon.
        type (EndfieldCharacterKV): The type of the weapon.
        skills (list[EndfieldCharacterKV]): The skills associated with the weapon.
        function (str): The function of the weapon.
        description (str): The description of the weapon.
        iconUrl (str): The URL of the weapon's icon.
    """

    id: str
    name: str

    rarity: EndfieldCharacterKV
    type: EndfieldCharacterKV
    skills: list[EndfieldCharacterKV]

    function: str
    description: str

    iconUrl: str


class EndfieldCharacterWeapon(APIModel):
    """
    Represents a weapon for an Endfield character.

    Attributes:
        level (int): The level of the weapon.
        refineLevel (int): The refinement level of the weapon.
        breakthroughLevel (int): The breakthrough level of the weapon.
        weaponData (EndfieldCharacterWeaponData): The data associated with the weapon.
    """

    level: int
    refineLevel: int
    breakthroughLevel: int
    weaponData: EndfieldCharacterWeaponData


class EndfieldCharacter(APIModel):
    """
    Represents an Endfield character.

    Attributes:
        id (str): The unique identifier of the character.
        level (int): The level of the character.
        weapon (EndfieldCharacterWeapon): The weapon equipped by the character.
        evolvePhase (int): The evolution phase of the character.
        potentialLevel (int): The potential level of the character.
        gender (str): The gender of the character.
        ownTs (DateTimeField): The timestamp when the character was obtained.
        charData (EndfieldCharacterCharData): The character data.
        userSkills (dict[str, EndfieldCharacterUserSkill]): The user's skills for the character.
        bodyEquip (Optional[EndfieldCharacterEquip]): The body equipment of the character.
        armEquip (Optional[EndfieldCharacterEquip]): The arm equipment of the character.
        firstAccessory (Optional[EndfieldCharacterEquip]): The first accessory of the character.
        secondAccessory (Optional[EndfieldCharacterEquip]): The second accessory of the character.
        tacticalItem (Optional[EndfieldCharacterTactical]): The tactical item of the character.
    """

    id: str
    level: int

    weapon: EndfieldCharacterWeapon

    evolvePhase: int
    potentialLevel: int
    gender: str
    ownTs: DateTimeField

    charData: EndfieldCharacterCharData
    userSkills: dict[str, EndfieldCharacterUserSkill]

    bodyEquip: Optional[EndfieldCharacterEquip] = None
    armEquip: Optional[EndfieldCharacterEquip] = None
    firstAccessory: Optional[EndfieldCharacterEquip] = None
    secondAccessory: Optional[EndfieldCharacterEquip] = None

    tacticalItem: Optional[EndfieldCharacterTactical] = None
