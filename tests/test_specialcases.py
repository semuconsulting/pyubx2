"""
Special case tests for pyubx2.UBXMessage

Mainly message types which have alternative payload definitions

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest

from pyubx2 import UBXMessage, UBXReader, SET, GET
import pyubx2.ubxtypes_configdb as ubxcdb


class SpecialTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.cfg_rinv2 = b"\xb5b\x06\x34\x03\x00\x03\x07\x04\x4b\x8c"
        self.cfg_rinv7 = (
            b"\xb5b\x06\x34\x08\x00\x03\x01\x02\x03\x04\x05\x06\x07\x61\x40"
        )
        self.cfg_rinv0 = b"\xb5b\x06\x34\x01\x00\x03\x3e\xf4"

    def tearDown(self):
        pass

    def testCfg_Rinv2(self):
        res = UBXReader.parse(self.cfg_rinv2)
        self.assertIsInstance(res, UBXMessage)

    def testCfg_Rinv2ID(self):
        res = UBXReader.parse(self.cfg_rinv2)
        self.assertEqual(res.identity, "CFG-RINV")

    def testCfg_Rinv2Str(self):
        res = UBXReader.parse(self.cfg_rinv2)
        self.assertEqual(
            str(res), "<UBX(CFG-RINV, dump=1, binary=1, data_01=7, data_02=4)>"
        )

    def testCfg_Rinv7(self):
        res = UBXReader.parse(self.cfg_rinv7)
        self.assertIsInstance(res, UBXMessage)

    def testCfg_Rinv7ID(self):
        res = UBXReader.parse(self.cfg_rinv7)
        self.assertEqual(res.identity, "CFG-RINV")

    def testCfg_Rinv7Str(self):
        res = UBXReader.parse(self.cfg_rinv7)
        self.assertEqual(
            str(res),
            "<UBX(CFG-RINV, dump=1, binary=1, data_01=1, data_02=2, data_03=3, data_04=4, data_05=5, data_06=6, data_07=7)>",
        )

    def testCfg_Rinv0(self):
        res = UBXReader.parse(self.cfg_rinv0)
        self.assertIsInstance(res, UBXMessage)

    def testCfg_Rinv0ID(self):
        res = UBXReader.parse(self.cfg_rinv0)
        self.assertEqual(res.identity, "CFG-RINV")

    def testCfg_Rinv0Str(self):
        res = UBXReader.parse(self.cfg_rinv0)
        self.assertEqual(str(res), "<UBX(CFG-RINV, dump=1, binary=1)>")

    def testFill_RXMPMREQSET(
        self,
    ):  #  test RXM-PMREQ SET constructor long version with payload keyword
        EXPECTED_RESULT = "<UBX(RXM-PMREQ, version=0, reserved0=0, duration=67305985, backup=0, force=0, uartrx=0, extint0=0, extint1=0, spics=0)>"
        res = UBXMessage(
            "RXM",
            "RXM-PMREQ",
            SET,
            payload=b"\x00\x00\x00\x00\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04",
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_RXMPMREQSET2(
        self,
    ):  #  test RXM-PMREQ SET constructor long version with version keyword
        EXPECTED_RESULT = "<UBX(RXM-PMREQ, version=0, reserved0=0, duration=67305985, backup=0, force=0, uartrx=0, extint0=0, extint1=0, spics=0)>"
        res = UBXMessage(
            "RXM",
            "RXM-PMREQ",
            SET,
            version=0,
            duration=67305985,
            flags=b"\x01\x02\x03\x04",
            wakeupSources=b"\x01\x02\x03\x04",
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_RXMPMREQSET3(self):  #  test RXM-PMREQ SET constructor short version
        EXPECTED_RESULT = "<UBX(RXM-PMREQ, duration=67305985, backup=1)>"
        res = UBXMessage(
            "RXM", "RXM-PMREQ", SET, payload=b"\x01\x02\x03\x04\x02\x01\x03\x04"
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_RXMPMPSETV0(
        self,
    ):  #  test RXM-PMP SET constructor with version=0 keyword
        EXPECTED_RESULT = "<UBX(RXM-PMP, version=0, reserved0=0, timeTag=0, uniqueWord1=0, uniqueWord2=0, serviceIdentifier=0, spare=0, uniqueWordBitErrors=0, userData_01=0, userData_02=0, userData_03=0, userData_04=0, userData_05=0, userData_06=0, userData_07=0, userData_08=0, userData_09=0, userData_10=0, userData_11=0, userData_12=0, userData_13=0, userData_14=0, userData_15=0, userData_16=0, userData_17=0, userData_18=0, userData_19=0, userData_20=0, userData_21=0, userData_22=0, userData_23=0, userData_24=0, userData_25=0, userData_26=0, userData_27=0, userData_28=0, userData_29=0, userData_30=0, userData_31=0, userData_32=0, userData_33=0, userData_34=0, userData_35=0, userData_36=0, userData_37=0, userData_38=0, userData_39=0, userData_40=0, userData_41=0, userData_42=0, userData_43=0, userData_44=0, userData_45=0, userData_46=0, userData_47=0, userData_48=0, userData_49=0, userData_50=0, userData_51=0, userData_52=0, userData_53=0, userData_54=0, userData_55=0, userData_56=0, userData_57=0, userData_58=0, userData_59=0, userData_60=0, userData_61=0, userData_62=0, userData_63=0, userData_64=0, userData_65=0, userData_66=0, userData_67=0, userData_68=0, userData_69=0, userData_70=0, userData_71=0, userData_72=0, userData_73=0, userData_74=0, userData_75=0, userData_76=0, userData_77=0, userData_78=0, userData_79=0, userData_80=0, userData_81=0, userData_82=0, userData_83=0, userData_84=0, userData_85=0, userData_86=0, userData_87=0, userData_88=0, userData_89=0, userData_90=0, userData_91=0, userData_92=0, userData_93=0, userData_94=0, userData_95=0, userData_96=0, userData_97=0, userData_98=0, userData_99=0, userData_100=0, userData_101=0, userData_102=0, userData_103=0, userData_104=0, userData_105=0, userData_106=0, userData_107=0, userData_108=0, userData_109=0, userData_110=0, userData_111=0, userData_112=0, userData_113=0, userData_114=0, userData_115=0, userData_116=0, userData_117=0, userData_118=0, userData_119=0, userData_120=0, userData_121=0, userData_122=0, userData_123=0, userData_124=0, userData_125=0, userData_126=0, userData_127=0, userData_128=0, userData_129=0, userData_130=0, userData_131=0, userData_132=0, userData_133=0, userData_134=0, userData_135=0, userData_136=0, userData_137=0, userData_138=0, userData_139=0, userData_140=0, userData_141=0, userData_142=0, userData_143=0, userData_144=0, userData_145=0, userData_146=0, userData_147=0, userData_148=0, userData_149=0, userData_150=0, userData_151=0, userData_152=0, userData_153=0, userData_154=0, userData_155=0, userData_156=0, userData_157=0, userData_158=0, userData_159=0, userData_160=0, userData_161=0, userData_162=0, userData_163=0, userData_164=0, userData_165=0, userData_166=0, userData_167=0, userData_168=0, userData_169=0, userData_170=0, userData_171=0, userData_172=0, userData_173=0, userData_174=0, userData_175=0, userData_176=0, userData_177=0, userData_178=0, userData_179=0, userData_180=0, userData_181=0, userData_182=0, userData_183=0, userData_184=0, userData_185=0, userData_186=0, userData_187=0, userData_188=0, userData_189=0, userData_190=0, userData_191=0, userData_192=0, userData_193=0, userData_194=0, userData_195=0, userData_196=0, userData_197=0, userData_198=0, userData_199=0, userData_200=0, userData_201=0, userData_202=0, userData_203=0, userData_204=0, userData_205=0, userData_206=0, userData_207=0, userData_208=0, userData_209=0, userData_210=0, userData_211=0, userData_212=0, userData_213=0, userData_214=0, userData_215=0, userData_216=0, userData_217=0, userData_218=0, userData_219=0, userData_220=0, userData_221=0, userData_222=0, userData_223=0, userData_224=0, userData_225=0, userData_226=0, userData_227=0, userData_228=0, userData_229=0, userData_230=0, userData_231=0, userData_232=0, userData_233=0, userData_234=0, userData_235=0, userData_236=0, userData_237=0, userData_238=0, userData_239=0, userData_240=0, userData_241=0, userData_242=0, userData_243=0, userData_244=0, userData_245=0, userData_246=0, userData_247=0, userData_248=0, userData_249=0, userData_250=0, userData_251=0, userData_252=0, userData_253=0, userData_254=0, userData_255=0, userData_256=0, userData_257=0, userData_258=0, userData_259=0, userData_260=0, userData_261=0, userData_262=0, userData_263=0, userData_264=0, userData_265=0, userData_266=0, userData_267=0, userData_268=0, userData_269=0, userData_270=0, userData_271=0, userData_272=0, userData_273=0, userData_274=0, userData_275=0, userData_276=0, userData_277=0, userData_278=0, userData_279=0, userData_280=0, userData_281=0, userData_282=0, userData_283=0, userData_284=0, userData_285=0, userData_286=0, userData_287=0, userData_288=0, userData_289=0, userData_290=0, userData_291=0, userData_292=0, userData_293=0, userData_294=0, userData_295=0, userData_296=0, userData_297=0, userData_298=0, userData_299=0, userData_300=0, userData_301=0, userData_302=0, userData_303=0, userData_304=0, userData_305=0, userData_306=0, userData_307=0, userData_308=0, userData_309=0, userData_310=0, userData_311=0, userData_312=0, userData_313=0, userData_314=0, userData_315=0, userData_316=0, userData_317=0, userData_318=0, userData_319=0, userData_320=0, userData_321=0, userData_322=0, userData_323=0, userData_324=0, userData_325=0, userData_326=0, userData_327=0, userData_328=0, userData_329=0, userData_330=0, userData_331=0, userData_332=0, userData_333=0, userData_334=0, userData_335=0, userData_336=0, userData_337=0, userData_338=0, userData_339=0, userData_340=0, userData_341=0, userData_342=0, userData_343=0, userData_344=0, userData_345=0, userData_346=0, userData_347=0, userData_348=0, userData_349=0, userData_350=0, userData_351=0, userData_352=0, userData_353=0, userData_354=0, userData_355=0, userData_356=0, userData_357=0, userData_358=0, userData_359=0, userData_360=0, userData_361=0, userData_362=0, userData_363=0, userData_364=0, userData_365=0, userData_366=0, userData_367=0, userData_368=0, userData_369=0, userData_370=0, userData_371=0, userData_372=0, userData_373=0, userData_374=0, userData_375=0, userData_376=0, userData_377=0, userData_378=0, userData_379=0, userData_380=0, userData_381=0, userData_382=0, userData_383=0, userData_384=0, userData_385=0, userData_386=0, userData_387=0, userData_388=0, userData_389=0, userData_390=0, userData_391=0, userData_392=0, userData_393=0, userData_394=0, userData_395=0, userData_396=0, userData_397=0, userData_398=0, userData_399=0, userData_400=0, userData_401=0, userData_402=0, userData_403=0, userData_404=0, userData_405=0, userData_406=0, userData_407=0, userData_408=0, userData_409=0, userData_410=0, userData_411=0, userData_412=0, userData_413=0, userData_414=0, userData_415=0, userData_416=0, userData_417=0, userData_418=0, userData_419=0, userData_420=0, userData_421=0, userData_422=0, userData_423=0, userData_424=0, userData_425=0, userData_426=0, userData_427=0, userData_428=0, userData_429=0, userData_430=0, userData_431=0, userData_432=0, userData_433=0, userData_434=0, userData_435=0, userData_436=0, userData_437=0, userData_438=0, userData_439=0, userData_440=0, userData_441=0, userData_442=0, userData_443=0, userData_444=0, userData_445=0, userData_446=0, userData_447=0, userData_448=0, userData_449=0, userData_450=0, userData_451=0, userData_452=0, userData_453=0, userData_454=0, userData_455=0, userData_456=0, userData_457=0, userData_458=0, userData_459=0, userData_460=0, userData_461=0, userData_462=0, userData_463=0, userData_464=0, userData_465=0, userData_466=0, userData_467=0, userData_468=0, userData_469=0, userData_470=0, userData_471=0, userData_472=0, userData_473=0, userData_474=0, userData_475=0, userData_476=0, userData_477=0, userData_478=0, userData_479=0, userData_480=0, userData_481=0, userData_482=0, userData_483=0, userData_484=0, userData_485=0, userData_486=0, userData_487=0, userData_488=0, userData_489=0, userData_490=0, userData_491=0, userData_492=0, userData_493=0, userData_494=0, userData_495=0, userData_496=0, userData_497=0, userData_498=0, userData_499=0, userData_500=0, userData_501=0, userData_502=0, userData_503=0, userData_504=0, fecBits=0, ebno=0, reserved1=0)>"
        res = UBXMessage("RXM", "RXM-PMP", SET, version=0)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_RXMRLMSETV1(
        self,
    ):  #  test RXM-PMP SET constructor with version=1 keyword
        EXPECTED_RESULT = "<UBX(RXM-PMP, version=1, reserved0=0, numBytesUserData=0, timeTag=0, uniqueWord1=0, uniqueWord2=0, serviceIdentifier=0, spare=0, uniqueWordBitErrors=0, fecBits=0, ebno=0, reserved1=0)>"
        res = UBXMessage("RXM", "RXM-PMP", SET, version=1)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_RXMRLMSETS(self):  #  test RXM-RLM GET constructor with type=1 keyword
        EXPECTED_RESULT = "<UBX(RXM-RLM, version=0, type=1, svId=0, reserved0=0, beacon=0, message=0, params=0, reserved1=0)>"
        res = UBXMessage("RXM", "RXM-RLM", GET, version=0, type=1)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_RXMPMPSETL(self):  #  test RXM-RLM GET constructor with type=2 keyword
        EXPECTED_RESULT = "<UBX(RXM-RLM, version=0, type=2, svId=0, reserved0=0, beacon=0, message=0, params=0, reserved1=0)>"
        res = UBXMessage("RXM", "RXM-RLM", GET, version=0, type=2)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_ESFMEASSET(
        self,
    ):  #  test ESF_MEAS GET constructor with calibTtagValid = 0
        EXPECTED_RESULT = "<UBX(ESF-MEAS, timeTag=0, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=0, numMeas=0, id=0)>"
        res = UBXMessage(
            "ESF", "ESF-MEAS", GET, timeTag=0, flags=b"\x00\x00", parsebitfield=0
        )
        res2 = UBXReader.parse(res.serialize())
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_ESFMEASSETCT(
        self,
    ):  #  test ESF_MEAS GET constructor with calibTtagValid = 1
        EXPECTED_RESULT = "<UBX(ESF-MEAS, timeTag=0, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=0, id=0)>"
        res = UBXMessage(
            "ESF", "ESF-MEAS", GET, timeTag=0, flags=b"\x18\x00", parsebitfield=0
        )
        res2 = UBXReader.parse(res.serialize())
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_MGABDSSET(
        self,
    ):  #  test MGA-BDS-UTC SET constructor using attribute keywords, very large scaling factors
        EXPECTED_RESULT = "<UBX(MGA-BDS-UTC, type=5, version=0, reserved0=0, a0UTC=1.2218952178955079e-09, a1UTC=1.2949641359227826e-15, dtLS=0, reserved1=0, wnRec=23, wnLSF=41, dN=0, dtLSF=0, reserved2=0)>"
        res = UBXMessage(
            b"\x13",
            b"\x03",
            SET,
            type=5,
            a0UTC=1.312 * 2**-30,
            a1UTC=1.458 * 2**-50,
            wnRec=23,
            wnLSF=41,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_RELPOSNED_v0(self):  # test NAV-RELPOSNED V0 constructor
        EXPECTED_RESULT = "<UBX(NAV-RELPOSNED, version=0, reserved1=0, refStationID=0, iTOW=23:59:42, relPosN=1, relPosE=2, relPosD=3, relPosHPN=0, relPosHPE=0, relPosHPD=0, reserved2=0, accN=0, accE=0, accD=0, gnssFixOK=0, diffSoln=0, relPosValid=0, carrSoln=0, isMoving=0, refPosMiss=0, refObsMiss=0, relPosHeadingValid=0, relPosNormalized=0)>"
        EXPECTED_RESULT2 = "<UBX(NAV-RELPOSNED, version=0, reserved1=0, refStationID=0, iTOW=23:59:42, relPosN=1, relPosE=2, relPosD=3, relPosHPN=0.0, relPosHPE=0.0, relPosHPD=0.0, reserved2=0, accN=0.0, accE=0.0, accD=0.0, gnssFixOK=0, diffSoln=0, relPosValid=0, carrSoln=0, isMoving=0, refPosMiss=0, refObsMiss=0, relPosHeadingValid=0, relPosNormalized=0)>"
        res = UBXMessage(
            "NAV",
            "NAV-RELPOSNED",
            GET,
            version=0,
            relPosN=1,
            relPosE=2,
            relPosD=3,
        )
        res2 = UBXMessage("NAV", "NAV-RELPOSNED", GET, payload=res.payload)
        self.assertEqual(str(res), EXPECTED_RESULT)
        # self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_RELPOSNED_v1(self):  # test NAV-RELPOSNED V1 constructor
        EXPECTED_RESULT = "<UBX(NAV-RELPOSNED, version=1, reserved0=0, refStationID=0, iTOW=23:59:42, relPosN=1, relPosE=2, relPosD=3, relPosLength=0, relPosHeading=0, reserved1=0, relPosHPN=0, relPosHPE=0, relPosHPD=0, relPosHPLength=0, accN=0, accE=0, accD=0, accLength=0, accHeading=0, reserved2=0, gnssFixOK=0, diffSoln=0, relPosValid=0, carrSoln=0, isMoving=0, refPosMiss=0, refObsMiss=0, relPosHeadingValid=0, relPosNormalized=0)>"
        EXPECTED_RESULT2 = "<UBX(NAV-RELPOSNED, version=1, reserved0=0, refStationID=0, iTOW=23:59:42, relPosN=1, relPosE=2, relPosD=3, relPosLength=0, relPosHeading=0.0, reserved1=0, relPosHPN=0.0, relPosHPE=0.0, relPosHPD=0.0, relPosHPLength=0.0, accN=0.0, accE=0.0, accD=0.0, accLength=0.0, accHeading=0.0, reserved2=0, gnssFixOK=0, diffSoln=0, relPosValid=0, carrSoln=0, isMoving=0, refPosMiss=0, refObsMiss=0, relPosHeadingValid=0, relPosNormalized=0)>"
        res = UBXMessage(
            "NAV",
            "NAV-RELPOSNED",
            GET,
            version=1,
            relPosN=1,
            relPosE=2,
            relPosD=3,
        )
        res2 = UBXMessage("NAV", "NAV-RELPOSNED", GET, payload=res.payload)
        self.assertEqual(str(res), EXPECTED_RESULT)
        # self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_AOPSTATUSL(self):  # testNAV-AOPSTATUS M6 constructor
        EXPECTED_RESULT = "<UBX(NAV-AOPSTATUS, iTOW=18:41:27.985000, config=1, status=2, reserved0=0, reserved1=0, avail=67305985, reserved2=67305985, reserved3=67305985)>"
        res = UBXMessage(
            "NAV",
            "NAV-AOPSTATUS",
            GET,
            payload=b"\x01\x02\x03\x04\x01\x02\x00\x00\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04",
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_AOPSTATUS(self):  # testNAV-AOPSTATUS M8 constructor
        EXPECTED_RESULT = "<UBX(NAV-AOPSTATUS, iTOW=18:41:27.985000, aopCfg=1, status=2, reserved1=42649378395939397566720)>"
        res = UBXMessage(
            "NAV",
            "NAV-AOPSTATUS",
            GET,
            payload=b"\x01\x02\x03\x04\x01\x02\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09",
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_TIMVCOCAL_v0(self):  # test TIM-VCOCAL-V0 constructor
        EXPECTED_RESULT = "<UBX(TIM-VCOCAL, type=0)>"
        res = UBXMessage(
            "TIM",
            "TIM-VCOCAL",
            SET,
            type=0,
        )
        res2 = UBXMessage("TIM", "TIM-VCOCAL", SET, payload=res.payload)
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_TIMVCOCAL(self):  # test TIM-VCOCAL constructor
        EXPECTED_RESULT = "<UBX(TIM-VCOCAL, type=2, version=0, oscId=0, srcId=0, reserved1=0, raw0=0, raw1=0, maxStepSize=2)>"
        res = UBXMessage(
            "TIM",
            "TIM-VCOCAL",
            SET,
            type=2,
            maxStepSize=2,
        )
        res2 = UBXMessage("TIM", "TIM-VCOCAL", SET, payload=res.payload)
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_CFGDAT(self):  # test CFG-DAT constructor
        EXPECTED_RESULT = "<UBX(CFG-DAT, majA=15.2, flat=23.4, dX=4.6, dY=7.2, dZ=15.7, rotX=123.3, rotY=18.4, rotZ=43.5, scale=2.3)>"
        res = UBXMessage(
            "CFG",
            "CFG-DAT",
            SET,
            majA=15.2,
            flat=23.4,
            dX=4.6,
            dY=7.2,
            dZ=15.7,
            rotX=123.3,
            rotY=18.4,
            rotZ=43.5,
            scale=2.3,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)
        res2 = UBXMessage("CFG", "CFG-DAT", SET, payload=res.payload)
        self.assertAlmostEqual(res2.majA, 15.2, 5)
        self.assertAlmostEqual(res2.dX, 4.6, 5)
        self.assertAlmostEqual(res2.scale, 2.3, 5)

    def testFill_CFGDAT_NUM(self):  # test CFG-DAT-NUM constructor
        EXPECTED_RESULT = "<UBX(CFG-DAT, datumNum=7)>"
        res = UBXMessage(
            "CFG",
            "CFG-DAT",
            SET,
            datumNum=7,
        )
        res2 = UBXMessage("CFG", "CFG-DAT", SET, payload=res.payload)
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testConfigSet(self):  # test creation of CFG-VALSET message with single key
        cfgData = [("CFG_UART1_BAUDRATE", 9600)]
        res = UBXMessage.config_set(ubxcdb.SET_LAYER_RAM, ubxcdb.TXN_NONE, cfgData)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALSET, version=0, ram=1, bbr=0, flash=0, action=0, reserved0=0, CFG_UART1_BAUDRATE=9600)>",
        )

    def testConfigSet2(
        self,
    ):  # test creation of CFG-VALSET message with multiple keys as transaction
        cfgData = [("CFG_UART1_BAUDRATE", 9600), (0x40530001, 115200)]
        res = UBXMessage.config_set(ubxcdb.SET_LAYER_BBR, ubxcdb.TXN_START, cfgData)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALSET, version=1, ram=0, bbr=1, flash=0, action=1, reserved0=0, CFG_UART1_BAUDRATE=9600, CFG_UART2_BAUDRATE=115200)>",
        )

    def testConfigDel(self):  # test creation of CFG-VALSET message with single key
        keys = [
            "CFG_UART1_BAUDRATE",
        ]
        res = UBXMessage.config_del(ubxcdb.SET_LAYER_BBR, ubxcdb.TXN_NONE, keys)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALDEL, version=0, bbr=1, flash=0, action=0, reserved0=0, keys_01=1079115777)>",
        )

    def testConfigDel2(
        self,
    ):  # test creation of CFG-VALSET message with multiples keys as transaction
        keys = ["CFG_UART1_BAUDRATE", 0x40530001]
        res = UBXMessage.config_del(ubxcdb.SET_LAYER_FLASH, ubxcdb.TXN_START, keys)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALDEL, version=1, bbr=0, flash=1, action=1, reserved0=0, keys_01=1079115777, keys_02=1079181313)>",
        )

    def testConfigPoll(self):  # test creation of CFG-VALGET message with multiple keys
        keys = ["CFG_UART1_BAUDRATE", 0x40530001]
        res = UBXMessage.config_poll(ubxcdb.POLL_LAYER_FLASH, 0, keys)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALGET, version=0, layer=2, position=0, keys_01=1079115777, keys_02=1079181313)>",
        )

    def testESFMEASSET0(self):  # test generation fo ESF-MEAS with calibTtagValid=0
        EXPECTED_RESULT = "<UBX(ESF-MEAS, timeTag=12345000, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=0, numMeas=1, id=0, dataField_01=188, dataType_01=11)>"
        msg = UBXMessage(
            "ESF",
            "ESF-MEAS",
            SET,
            timeTag=12345000,
            timeMarkSent=0,
            timeMarkEdge=0,
            calibTtagValid=0,
            numMeas=1,
            dataField_01=188,
            dataType_01=11,
        )
        self.assertEqual(str(msg), EXPECTED_RESULT)

    def testESFMEASSET1(self):  # test generation fo ESF-MEAS with calibTtagValid=1
        EXPECTED_RESULT = "<UBX(ESF-MEAS, timeTag=12345000, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=2, id=0, dataField_01=223, dataType_01=9, dataField_02=118, dataType_02=11, dataField_03=12345000, dataType_03=0)>"
        msg = UBXMessage(
            "ESF",
            "ESF-MEAS",
            SET,
            timeTag=12345000,
            timeMarkSent=0,
            timeMarkEdge=0,
            calibTtagValid=1,
            numMeas=2,
            dataField_01=223,
            dataType_01=9,
            dataField_02=118,
            dataType_02=11,
            dataField_03=12345000,
            dataType_03=0,
        )
        self.assertEqual(str(msg), EXPECTED_RESULT)

    def testACKACKNK(self):  # test ACK-ACK of unknown message class
        EXPECTED_RESULT = "<UBX(ACK-ACK, clsID=b'w', msgID=b'w\\x88')>"
        msg = UBXMessage("ACK", "ACK-ACK", GET, clsID=0x77, msgID=0x88)
        self.assertEqual(str(msg), EXPECTED_RESULT)

    def testCFGMSGNK(self):  # test CFG-MSG of unknown message class
        EXPECTED_RESULT = "<UBX(CFG-MSG, msgClass=b'w', msgID=b'w\\x88', rateDDC=0, rateUART1=4, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0)>"
        msg = UBXMessage("CFG", "CFG-MSG", GET, msgClass=0x77, msgID=0x88, rateUART1=4)
        self.assertEqual(str(msg), EXPECTED_RESULT)

    def testUnknownClassID(self):  # test for unknown class and id
        EXPECTED_RESULT = "<UBX(UNKNOWN-5566-NOMINAL, payload=b'\\x33\\x44')>"
        msg = UBXReader.parse(b"\xb5b\x55\x66\x02\x00\x33\x44\x34\xae")
        # print(msg)
        self.assertEqual(str(msg), EXPECTED_RESULT)

    def testUnknownID(self):  # test for known class, unknown id
        EXPECTED_RESULT = "<UBX(DBG-0c66-NOMINAL, payload=b'\\x55\\x66')>"
        msg = UBXReader.parse(b"\xb5b\x0c\x66\x02\x00\x55\x66\x2f\x5e")
        # print(msg)
        self.assertEqual(str(msg), EXPECTED_RESULT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
