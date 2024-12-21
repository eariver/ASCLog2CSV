from dataclasses import dataclass
from enum import Enum
from typing import Self


# Data Classes
@dataclass
class UDSCANPhyIDs:
    """物理CAN ID

    UDSフレームで扱う物理CAN IDを規定する。

    Attributes:
        * ST2ECU: Scan ToolからECUに対する要求用CAN ID
        * ECU2ST: ECUからScan Toolに対する返答用CAN ID
        * ECUName: このインスタンスが扱うECUの名前

    """
    ST2ECU: str
    ECU2ST: str
    ECUName: str = ""


@dataclass
class UDSCANFncIDs:
    """機能CAN ID

    UDSフレームで扱う機能CAN IDを規定する。

    Attributes:
        * FncIDs: Scan Toolから各ECUに対する要求用CAN IDのリスト
        * FncIDNum: FNCIDsのサイズ

    """
    FncIDs: list[str]
    FncIDNum: int = 0

    def append(self, fncid: str):
        """機能CAN ID追加

        引数で与えられた機能CAN IDをFncIDsに追加してFncIDNumを更新する

        Args:
            fncid (str): 追加する機能CAN ID

        Returns:
            None
        """
        self.FncIDs.append(fncid)
        self.FncIDNum = len(self.FncIDs)


# Enums
class SID(Enum):
    """Service ID

    UDSで使用するSIDの一覧
    """
    DiagSCntr = 0x10
    ECUReset = 0x11
    SecAccess = 0x27
    ComCntr = 0x28
    TsPresent = 0x3E
    AccTimParam = 0x83
    SecDatTrans = 0x84
    CntrDTCSet = 0x85
    ResOnEve = 0x86
    LinkCntr = 0x87
    RDatByID = 0x22
    RMemByAddr = 0x23
    RScDatByID = 0x24
    RDatByPID = 0x2A
    DynDefDID = 0x2C
    WDatByID = 0x2E
    WMemByAddr = 0x3D
    ClrDiagInfo = 0x14
    RDTCInfo = 0x19
    IOCntrByID = 0x2F
    RoutineCntr = 0x31
    ReqDnL = 0x34
    ReqUpL = 0x35
    TransDat = 0x36
    ReqTransExit = 0x37
    ReqFileTrans = 0x38
    Other = 0xFF
    
    @classmethod
    def get_sid(cls, sid: int) -> Self:
        ret = SID.Other
        for _sid in cls:
            if _sid.value == sid:
                ret = _sid
        return ret


class SType(Enum):
    """Service ID Type

    identify_serviceで判別した結果の一覧
    """
    UDSService = 0
    UDSPosRes = 1
    UDSNegRes = 2
    OBDService = 3
    Other = 4


class PDUType(Enum):
    """PDUType Type

    Protocol Data Unitの種類を示す。
    """
    SF = 0
    FF = 1
    CF = 2
    FC = 3


# Private Methods
def __identify_service(sid: int) -> tuple[SID, SType]:
    """SID確認

    引数に与えられたSIDが何で定義されたServiceのものかを判別する。

    Args:
        sid (int): 判別するSID

    Returns:
        Tuple containing

        * SID: 判別されたUDS SID
        * SType: 判別結果 (UDS Service/Pos/Neg、OBD-II、Other)
    """
    if sid < 0x10:
        return SID.Other, SType.OBDService
    elif sid < 0x3F:
        return SID.get_sid(sid), SType.UDSService
    elif 0x3F < sid < 0x7F:
        return SID.get_sid(sid-0x40), SType.UDSPosRes
    elif sid == 0x7F:
        return SID.Other, SType.UDSNegRes
    elif 0x82 < sid < 0x89:
        return SID.get_sid(sid), SType.UDSService
    elif 0xC2 < sid < 0xC9:
        return SID.get_sid(sid-0x40), SType.UDSPosRes

    return SID.Other, SType.Other


# Class
class UDSFrame:
    """各UDSデータフレームを扱う
    """
    type: PDUType
    DL: int
    SF: int
    DID: int
    pass #がんばる

# TODO UDSFrameに必要な要素を考える
# * SF/FF/CFでそれぞれ何が必要か？
# * FCではこれらの情報が必要なさそうでは？
# * FF/CFのDLの定義、CFでは残バイト数を示す？
# * NRCのEnumを作る？
