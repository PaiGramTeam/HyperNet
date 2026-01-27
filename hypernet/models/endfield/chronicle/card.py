from typing import Optional

from hypernet.models.base import APIModel, DateTimeField
from hypernet.models.endfield.character import EndfieldCharacter
from hypernet.models.endfield.chronicle.notes import EndfieldNoteSkport


class EndfieldCardDetailBaseInfoMainMission(APIModel):
    """
    表示主线任务的基本信息。

    属性:
        id (str): 主线任务的唯一标识符。
        description (str): 主线任务的描述。
    """

    id: str
    description: str


class EndfieldCardDetailBaseInfo(APIModel):
    """
    表示 Endfield 卡片的基本信息。

    属性:
        roleId (int): 角色 ID。
        name (str): 角色名称。
        createTime (DateTimeField): 创建时间。
        saveTime (DateTimeField): 保存时间。
        lastLoginTime (DateTimeField): 上次登录时间。
        exp (int): 经验值。
        level (int): 等级。
        worldLevel (int): 世界等级。
        gender (int): 性别。
        avatarUrl (str): 头像 URL。
        mainMission (EndfieldCardDetailBaseInfoMainMission): 主线任务信息。
        charNum (int): 拥有的角色数量。
        weaponNum (int): 拥有的武器数量。
        docNum (int): 拥有的文档数量。
    """

    roleId: int
    name: str

    createTime: DateTimeField
    saveTime: DateTimeField
    lastLoginTime: DateTimeField

    exp: int
    level: int
    worldLevel: int
    gender: int
    avatarUrl: str
    mainMission: EndfieldCardDetailBaseInfoMainMission
    charNum: int
    weaponNum: int
    docNum: int


class EndfieldCardDetailAchieveInfo(APIModel):
    """
    表示成就信息。

    属性:
        count (int): 成就数量。
    """

    count: int


class EndfieldCardDetailSpaceShipChar(APIModel):
    """
    表示飞船中的角色信息。

    属性:
        charId (str): 角色 ID。
        favorability (int): 好感度。
        physicalStrength (float): 体力值。
    """

    charId: str
    favorability: int
    physicalStrength: float


class EndfieldCardDetailSpaceShipReport(APIModel):
    """
    表示飞船的报告信息。

    属性:
        char (list[str]): 参与的角色列表。
        output (dict[str, int]): 输出数据。
        createdTimeTs (DateTimeField): 报告创建时间戳。
    """

    char: list[str]
    output: dict[str, int]
    createdTimeTs: DateTimeField


class EndfieldCardDetailSpaceShipRoom(APIModel):
    """
    表示飞船中的房间信息。

    属性:
        id (str): 房间 ID。
        type (int): 房间类型。
        level (int): 房间等级。
        chars (list[EndfieldCardDetailSpaceShipChar]): 房间中的角色列表。
        reports (dict[str, EndfieldCardDetailSpaceShipReport]): 房间的报告信息。
    """

    id: str
    type: int
    level: int
    chars: list[EndfieldCardDetailSpaceShipChar]
    reports: dict[str, EndfieldCardDetailSpaceShipReport]


class EndfieldCardDetailSpaceShip(APIModel):
    """
    表示飞船信息。

    属性:
        rooms (list[EndfieldCardDetailSpaceShipRoom]): 飞船中的房间列表。
    """

    rooms: list[EndfieldCardDetailSpaceShipRoom]


class EndfieldCardDetailDomainSettlementItem(APIModel):
    """
    表示据点信息。

    属性:
        id (str): 据点 ID。
        name (str): 据点名称。
        level (int): 据点等级。
        officerCharIds (Optional[str]): 据点的指挥官角色 ID 列表。
    """

    id: str
    name: str
    level: int
    officerCharIds: Optional[str] = None


class EndfieldCardDetailDomainCollectionItem(APIModel):
    """
    表示采集点信息。

    属性:
        levelId (str): 采集点等级 ID。
        puzzleCount (int): 拼图数量。
        trchestCount (int): 宝箱数量。
        blackboxCount (int): 黑匣子数量。
        pieceCount (int): 碎片数量。
    """

    levelId: str
    puzzleCount: int
    trchestCount: int
    blackboxCount: int
    pieceCount: int


class EndfieldCardDetailDomainItem(APIModel):
    """
    表示区域信息。

    属性:
        domainId (str): 区域 ID。
        name (str): 区域名称。
        level (int): 区域等级。
        settlements (list[EndfieldCardDetailDomainSettlementItem]): 区域内的据点列表。
        collections (list[EndfieldCardDetailDomainCollectionItem]): 区域内的采集点列表。
    """

    domainId: str
    name: str
    level: int

    settlements: list[EndfieldCardDetailDomainSettlementItem]
    collections: list[EndfieldCardDetailDomainCollectionItem]


class EndfieldCardDetailConfig(APIModel):
    """
    表示卡片的配置信息。

    属性:
        charSwitch (bool): 角色开关状态。
        charIds (list[str]): 角色 ID 列表。
    """

    charSwitch: bool
    charIds: list[str]


class EndfieldCardDetail(EndfieldNoteSkport):
    """
    表示 Endfield 卡片的详细信息。

    属性:
        base (EndfieldCardDetailBaseInfo): 卡片的基本信息。
        chars (list[EndfieldCharacter]): 卡片中的角色列表。
        achieve (EndfieldCardDetailAchieveInfo): 成就信息。
        spaceShip (EndfieldCardDetailSpaceShip): 飞船信息。
        domain (list[EndfieldCardDetailDomainItem]): 区域信息列表。
        config (EndfieldCardDetailConfig): 配置信息。
        currentTs (DateTimeField): 当前时间戳。
    """

    base: EndfieldCardDetailBaseInfo
    chars: list[EndfieldCharacter]
    achieve: EndfieldCardDetailAchieveInfo
    spaceShip: EndfieldCardDetailSpaceShip
    domain: list[EndfieldCardDetailDomainItem]
    config: EndfieldCardDetailConfig

    currentTs: DateTimeField
