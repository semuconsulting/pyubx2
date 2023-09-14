"""
Parse method tests for pyubx2.UBXMessage

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest

from pyubx2 import UBXMessage, UBXReader, VALCKSUM, VALNONE, SET


class ParseTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ack_ack = b"\xb5b\x05\x01\x02\x00\x06\x01\x0f\x38"
        self.ack_ack_badck = b"\xb5b\x05\x01\x02\x00\x06\x01\x0f\x37"
        self.cfg_msg = b"\xb5b\x06\x01\x08\x00\xf0\x01\x00\x01\x01\x01\x00\x00\x036"
        self.cfg_prt = b"\xb5b\x06\x00\x00\x00\x06\x18"
        self.nav_pl = b"\xb5b\x01\x62\x34\x00\x01\x05\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x48\x04\xA9\x14\x6D\x00\x00\x00\x6D\x00\x00\x00\x6D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xEF\x88"
        self.nav_velned = b"\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6"
        self.nav_svinfo = b""
        self.cfg_nmeavx = b"\xb5b\x06\x17\x04\x00\x00\x00\x00\x00\x21\xe9"
        self.cfg_nmeav0 = b"\xb5b\x06\x17\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x29\x61"
        self.mga_dbd = b"\xb5b\x13\x80\x0e\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x01\x02\xf2\xc2"
        self.mga_flash_ack = b"\xb5b\x13\x21\x06\x00\x03\x01\x02\x00\x00\x04\x44\x3a"
        self.cfg_valget = b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x01\x00\x52\x40\x80\x25\x00\x00\xd5\xd0"
        self.cfg_valget2 = (
            b"\xb5b\x06\x8b\x09\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x61\xc2"
        )
        self.cfg_valget3 = b"\xb5b\x06\x8b\x16\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x01\x00\x52\x40\x80\x25\x00\x00\x02\x00\x21\x30\x23\x1c\x92"
        self.cfg_valget4 = b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x68\x00\x11\x40\xb6\xf3\x9d\x3f\xdb\x3d"
        self.esf_meas = b"\xb5b\x10\x02\x1c\x00\x6d\xd8\x07\x00\x18\x20\x00\x00\xcd\x06\x00\x0e\xe4\xfe\xff\x0d\x03\xfa\xff\x05\x09\x0b\x00\x0c\x6d\xd8\x07\x00\xee\x51"
        self.esf_meas2 = b"\xb5b\x10\x02\x18\x00\x72\xd8\x07\x00\x18\x18\x00\x00\x4b\xfd\xff\x10\x40\x02\x00\x11\x23\x28\x00\x12\x72\xd8\x07\x00\x03\x9c"
        self.mga_ini1 = b"\xb5b\x13\x40\x14\x00\x01\x00\x01\x02\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x93\xc8"
        self.mon_span = b"\xb5b\n1\x14\x01\x00\x01\x00\x00-+-,+-.,-.+,+.-..-,..//./00203017?9398:L]<@C;H<>=A@BDCGJNQRVY[_cgpqyz\x7f\x84\x8c\x90\x99\xa0\xa7\xae\xb0\xae\xaa\xa7\xa2\x9b\x97\x96\x94\x91\x90\x8e\x8c\x8c\x8c\x8b\x8b\x89\x88\x89\x89\x89\x8b\x88\x89\x8a\x89\x8a\x8a\x89\x8a\x8b\x8a\x8a\x8b\x8b\x8c\x8a\x8a\x8a\x8b\x88\x88\x87\x87\x86\x85\x85\x85\x84\x89\x84\x85\x83\x84\x84\x84\x85\x88\x87\x87\x88\x8a\x8a\x8a\x8a\x8b\x8e\x8c\x8d\x8d\x8f\x8e\x8d\x8f\x8e\x8f\x8f\x8e\x8f\x8f\x90\x91\x92\x93\x93\x93\x95\x94\x94\x94\x94\x95\x94\x95\x93\x93\x91\x92\x93\x92\x94\x95\x94\x95\x97\x97\x98\x97\x94\x90\x8d\x86\x82\x7fyupmg`]VRLEB?=;99665422202101///-//.-0-.-/..--,.-+-,--+.,,--,,-*\x00 \xa1\x07 \xa1\x07\x00@\xc4`^\x0c\x00\x00\x00\x15j"
        self.tim_tp = b"\xb5b\r\x01\x10\x00\x88gh\x16\x00\x00\x00\x00\x00\x00\x00\x00\x85\x08\x1b\x0fB\xff"
        self.esf_status = b"\xb5b\x10\x10.\x00\x00\x00\x00\x00\x02$\x02\x00\x00\x00\x00\x00\x00\x00\x00\x06\x85\x04\x00\x00\r\x04\n\x00\x8e\x04\n\x00\x00\x04\n\x00\x01\x00\n\x00\x92\x04\x00\x00\x00\x00\x00\x00\x00\x00k4"

    def tearDown(self):
        pass

    def testAck(self):
        res = UBXReader.parse(self.ack_ack, validate=VALCKSUM)
        self.assertIsInstance(res, UBXMessage)

    def testAckID(self):
        res = UBXReader.parse(self.ack_ack)
        self.assertEqual(res.identity, "ACK-ACK")

    def testAckStr(self):
        res = UBXReader.parse(self.ack_ack, validate=VALCKSUM)
        self.assertEqual(str(res), "<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)>")

    def testAckRepr(self):
        res = UBXReader.parse(self.ack_ack)
        self.assertEqual(
            repr(res), "UBXMessage(b'\\x05', b'\\x01', 0, payload=b'\\x06\\x01')"
        )

    def testAckCkF(self):
        UBXReader.parse(self.ack_ack_badck, validate=VALNONE)

    def testCfg(self):
        res = UBXReader.parse(self.ack_ack)
        self.assertIsInstance(res, UBXMessage)

    def testCfgID(self):
        res = UBXReader.parse(self.cfg_msg, validate=VALCKSUM)
        self.assertEqual(res.identity, "CFG-MSG")

    def testCfgStr(self):
        res = UBXReader.parse(self.cfg_msg, validate=VALCKSUM)
        self.assertEqual(
            str(res),
            "<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=GLL, rateDDC=0, rateUART1=1, rateUART2=1, rateUSB=1, rateSPI=0, reserved=0)>",
        )

    def testCfgRepr(self):
        res = UBXReader.parse(self.cfg_msg)
        self.assertEqual(
            repr(res),
            "UBXMessage(b'\\x06', b'\\x01', 0, payload=b'\\xf0\\x01\\x00\\x01\\x01\\x01\\x00\\x00')",
        )

    def testCfgProp1(self):
        res = UBXReader.parse(self.cfg_msg, validate=VALCKSUM)
        self.assertEqual(res.rateUART1, 1)

    def testCfgProp2(self):
        res = UBXReader.parse(self.cfg_msg)
        self.assertEqual(res.rateSPI, 0)

    def testNavPL(self):
        res = UBXReader.parse(self.nav_pl, validate=VALCKSUM)
        self.assertEqual(res.plPos2, 109)

    def testNavVelNed(self):
        res = UBXReader.parse(self.nav_velned, validate=VALCKSUM)
        self.assertIsInstance(res, UBXMessage)

    def testNavVelNedID(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(res.identity, "NAV-VELNED")

    def testNavVelNedStr(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(
            str(res),
            "<UBX(NAV-VELNED, iTOW=16:01:48, velN=-3, velE=-15, velD=-4, speed=16, gSpeed=15, heading=1.28387, sAcc=65, cAcc=80.5272)>",
        )

    def testNavVelNedRepr(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(
            repr(res),
            "UBXMessage(b'\\x01', b'\\x12', 0, payload=b'0D\\n\\x18\\xfd\\xff\\xff\\xff\\xf1\\xff\\xff\\xff\\xfc\\xff\\xff\\xff\\x10\\x00\\x00\\x00\\x0f\\x00\\x00\\x00\\x83\\xf5\\x01\\x00A\\x00\\x00\\x00\\xf0\\xdfz\\x00')",
        )

    def testNavVelNedProp1(self):
        res = UBXReader.parse(self.nav_velned, validate=VALCKSUM)
        self.assertEqual(res.iTOW, 403326000)

    def testNavVelNedProp2(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(res.cAcc, 80.5272)

    def testCfgPrt(self):  # POLL example with null payload
        res = UBXReader.parse(self.cfg_prt)
        self.assertIsInstance(res, UBXMessage)

    def testCfgPrtID(self):
        res = UBXReader.parse(self.cfg_prt)
        self.assertEqual(res.identity, "CFG-PRT")

    def testCfgPrtStr(self):
        res = UBXReader.parse(self.cfg_prt, validate=VALCKSUM)
        self.assertEqual(str(res), "<UBX(CFG-PRT)>")

    def testCfgPrtRepr(self):
        res = UBXReader.parse(self.cfg_prt)
        self.assertEqual(repr(res), "UBXMessage(b'\\x06', b'\\x00', 0)")

    def testCfgNmeaVx(self):  # test older NMEA message parse
        res = UBXReader.parse(self.cfg_nmeavx)
        self.assertEqual(
            str(res),
            "<UBX(CFG-NMEA, posFilt=0, mskPosFilt=0, timeFilt=0, dateFilt=0, gpsOnlyFilter=0, trackFilt=0, nmeaVersion=0, numSV=0, compat=0, consider=0, limit82=0, highPrec=0)>",
        )

    def testCfgNmeaV0(self):  # test older NMEA message parse
        res = UBXReader.parse(self.cfg_nmeav0)
        self.assertEqual(
            str(res),
            "<UBX(CFG-NMEA, posFilt=0, mskPosFilt=0, timeFilt=0, dateFilt=0, gpsOnlyFilter=0, trackFilt=0, nmeaVersion=0, numSV=0, compat=0, consider=0, limit82=0, highPrec=0, gps=0, sbas=0, galileo=0, qzss=0, glonass=0, bBeidou=0, svNumbering=0, mainTalkerId=0, gsvTalkerId=0, version=0)>",
        )

    def testMgaDbd(self):
        res = UBXReader.parse(self.mga_dbd)
        self.assertEqual(
            str(res),
            "<UBX(MGA-DBD, reserved1=3727165692135864801209549313, data_01=1, data_02=2)>",
        )

    def testMgaFlashAck(self):
        res = UBXReader.parse(self.mga_flash_ack)
        self.assertEqual(
            str(res),
            "<UBX(MGA-FLASH-ACK, type=3, version=1, ack=2, reserved1=0, sequence=1024)>",
        )

    def testCFGVALGET(self):  # test parser of CFG-VALGET CFG-UART1-BAUDRATE
        res = UBXReader.parse(self.cfg_valget)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_UART1_BAUDRATE=9600)>",
        )

    def testCFGVALGET2(self):  # test parse of CFG-VALGET CFG-I2C-ADDRESS
        res = UBXReader.parse(self.cfg_valget2)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_I2C_ADDRESS=85)>",
        )

    def testCFGVALGET3(
        self,
    ):  # test parse of CFG-VALGET CFG-I2C-ADDRESS, CFG-UART1-BAUDRATE, CFG-RATE-NAV
        res = UBXReader.parse(self.cfg_valget3)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_I2C_ADDRESS=85, CFG_UART1_BAUDRATE=9600, CFG_RATE_NAV=35)>",
        )

    def testCFGVALGET4(self):  # test parser of CFG-VALGET CFG-NAVSPG-USRDAT_ROTY
        res = UBXReader.parse(self.cfg_valget4)
        self.assertAlmostEqual(res.CFG_NAVSPG_USRDAT_ROTY, 1.23, 2)

    def testRXMPMPV0(self):  # test parser of RXM-PMP v0 message
        rxm_pmpv0 = b"\xb5b\x02\x72\x0e\x02\x00\x00\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x01\x01"
        for i in range(504):
            n = i % 256
            rxm_pmpv0 += n.to_bytes(1, "little", signed=False)
        rxm_pmpv0 += b"\x01\x02\x01\x00\xcf\xa9"
        res = UBXReader.parse(rxm_pmpv0, validate=VALCKSUM, msgmode=SET)
        self.assertEqual(
            str(res),
            "<UBX(RXM-PMP, version=0, reserved0=131328, timeTag=33620995, uniqueWord1=33620995, uniqueWord2=33620995, serviceIdentifier=257, spare=0, uniqueWordBitErrors=1, userData_01=2, userData_02=3, userData_03=4, userData_04=5, userData_05=6, userData_06=7, userData_07=8, userData_08=9, userData_09=10, userData_10=11, userData_11=12, userData_12=13, userData_13=14, userData_14=15, userData_15=16, userData_16=17, userData_17=18, userData_18=19, userData_19=20, userData_20=21, userData_21=22, userData_22=23, userData_23=24, userData_24=25, userData_25=26, userData_26=27, userData_27=28, userData_28=29, userData_29=30, userData_30=31, userData_31=32, userData_32=33, userData_33=34, userData_34=35, userData_35=36, userData_36=37, userData_37=38, userData_38=39, userData_39=40, userData_40=41, userData_41=42, userData_42=43, userData_43=44, userData_44=45, userData_45=46, userData_46=47, userData_47=48, userData_48=49, userData_49=50, userData_50=51, userData_51=52, userData_52=53, userData_53=54, userData_54=55, userData_55=56, userData_56=57, userData_57=58, userData_58=59, userData_59=60, userData_60=61, userData_61=62, userData_62=63, userData_63=64, userData_64=65, userData_65=66, userData_66=67, userData_67=68, userData_68=69, userData_69=70, userData_70=71, userData_71=72, userData_72=73, userData_73=74, userData_74=75, userData_75=76, userData_76=77, userData_77=78, userData_78=79, userData_79=80, userData_80=81, userData_81=82, userData_82=83, userData_83=84, userData_84=85, userData_85=86, userData_86=87, userData_87=88, userData_88=89, userData_89=90, userData_90=91, userData_91=92, userData_92=93, userData_93=94, userData_94=95, userData_95=96, userData_96=97, userData_97=98, userData_98=99, userData_99=100, userData_100=101, userData_101=102, userData_102=103, userData_103=104, userData_104=105, userData_105=106, userData_106=107, userData_107=108, userData_108=109, userData_109=110, userData_110=111, userData_111=112, userData_112=113, userData_113=114, userData_114=115, userData_115=116, userData_116=117, userData_117=118, userData_118=119, userData_119=120, userData_120=121, userData_121=122, userData_122=123, userData_123=124, userData_124=125, userData_125=126, userData_126=127, userData_127=128, userData_128=129, userData_129=130, userData_130=131, userData_131=132, userData_132=133, userData_133=134, userData_134=135, userData_135=136, userData_136=137, userData_137=138, userData_138=139, userData_139=140, userData_140=141, userData_141=142, userData_142=143, userData_143=144, userData_144=145, userData_145=146, userData_146=147, userData_147=148, userData_148=149, userData_149=150, userData_150=151, userData_151=152, userData_152=153, userData_153=154, userData_154=155, userData_155=156, userData_156=157, userData_157=158, userData_158=159, userData_159=160, userData_160=161, userData_161=162, userData_162=163, userData_163=164, userData_164=165, userData_165=166, userData_166=167, userData_167=168, userData_168=169, userData_169=170, userData_170=171, userData_171=172, userData_172=173, userData_173=174, userData_174=175, userData_175=176, userData_176=177, userData_177=178, userData_178=179, userData_179=180, userData_180=181, userData_181=182, userData_182=183, userData_183=184, userData_184=185, userData_185=186, userData_186=187, userData_187=188, userData_188=189, userData_189=190, userData_190=191, userData_191=192, userData_192=193, userData_193=194, userData_194=195, userData_195=196, userData_196=197, userData_197=198, userData_198=199, userData_199=200, userData_200=201, userData_201=202, userData_202=203, userData_203=204, userData_204=205, userData_205=206, userData_206=207, userData_207=208, userData_208=209, userData_209=210, userData_210=211, userData_211=212, userData_212=213, userData_213=214, userData_214=215, userData_215=216, userData_216=217, userData_217=218, userData_218=219, userData_219=220, userData_220=221, userData_221=222, userData_222=223, userData_223=224, userData_224=225, userData_225=226, userData_226=227, userData_227=228, userData_228=229, userData_229=230, userData_230=231, userData_231=232, userData_232=233, userData_233=234, userData_234=235, userData_235=236, userData_236=237, userData_237=238, userData_238=239, userData_239=240, userData_240=241, userData_241=242, userData_242=243, userData_243=244, userData_244=245, userData_245=246, userData_246=247, userData_247=248, userData_248=249, userData_249=250, userData_250=251, userData_251=252, userData_252=253, userData_253=254, userData_254=255, userData_255=0, userData_256=1, userData_257=2, userData_258=3, userData_259=4, userData_260=5, userData_261=6, userData_262=7, userData_263=8, userData_264=9, userData_265=10, userData_266=11, userData_267=12, userData_268=13, userData_269=14, userData_270=15, userData_271=16, userData_272=17, userData_273=18, userData_274=19, userData_275=20, userData_276=21, userData_277=22, userData_278=23, userData_279=24, userData_280=25, userData_281=26, userData_282=27, userData_283=28, userData_284=29, userData_285=30, userData_286=31, userData_287=32, userData_288=33, userData_289=34, userData_290=35, userData_291=36, userData_292=37, userData_293=38, userData_294=39, userData_295=40, userData_296=41, userData_297=42, userData_298=43, userData_299=44, userData_300=45, userData_301=46, userData_302=47, userData_303=48, userData_304=49, userData_305=50, userData_306=51, userData_307=52, userData_308=53, userData_309=54, userData_310=55, userData_311=56, userData_312=57, userData_313=58, userData_314=59, userData_315=60, userData_316=61, userData_317=62, userData_318=63, userData_319=64, userData_320=65, userData_321=66, userData_322=67, userData_323=68, userData_324=69, userData_325=70, userData_326=71, userData_327=72, userData_328=73, userData_329=74, userData_330=75, userData_331=76, userData_332=77, userData_333=78, userData_334=79, userData_335=80, userData_336=81, userData_337=82, userData_338=83, userData_339=84, userData_340=85, userData_341=86, userData_342=87, userData_343=88, userData_344=89, userData_345=90, userData_346=91, userData_347=92, userData_348=93, userData_349=94, userData_350=95, userData_351=96, userData_352=97, userData_353=98, userData_354=99, userData_355=100, userData_356=101, userData_357=102, userData_358=103, userData_359=104, userData_360=105, userData_361=106, userData_362=107, userData_363=108, userData_364=109, userData_365=110, userData_366=111, userData_367=112, userData_368=113, userData_369=114, userData_370=115, userData_371=116, userData_372=117, userData_373=118, userData_374=119, userData_375=120, userData_376=121, userData_377=122, userData_378=123, userData_379=124, userData_380=125, userData_381=126, userData_382=127, userData_383=128, userData_384=129, userData_385=130, userData_386=131, userData_387=132, userData_388=133, userData_389=134, userData_390=135, userData_391=136, userData_392=137, userData_393=138, userData_394=139, userData_395=140, userData_396=141, userData_397=142, userData_398=143, userData_399=144, userData_400=145, userData_401=146, userData_402=147, userData_403=148, userData_404=149, userData_405=150, userData_406=151, userData_407=152, userData_408=153, userData_409=154, userData_410=155, userData_411=156, userData_412=157, userData_413=158, userData_414=159, userData_415=160, userData_416=161, userData_417=162, userData_418=163, userData_419=164, userData_420=165, userData_421=166, userData_422=167, userData_423=168, userData_424=169, userData_425=170, userData_426=171, userData_427=172, userData_428=173, userData_429=174, userData_430=175, userData_431=176, userData_432=177, userData_433=178, userData_434=179, userData_435=180, userData_436=181, userData_437=182, userData_438=183, userData_439=184, userData_440=185, userData_441=186, userData_442=187, userData_443=188, userData_444=189, userData_445=190, userData_446=191, userData_447=192, userData_448=193, userData_449=194, userData_450=195, userData_451=196, userData_452=197, userData_453=198, userData_454=199, userData_455=200, userData_456=201, userData_457=202, userData_458=203, userData_459=204, userData_460=205, userData_461=206, userData_462=207, userData_463=208, userData_464=209, userData_465=210, userData_466=211, userData_467=212, userData_468=213, userData_469=214, userData_470=215, userData_471=216, userData_472=217, userData_473=218, userData_474=219, userData_475=220, userData_476=221, userData_477=222, userData_478=223, userData_479=224, userData_480=225, userData_481=226, userData_482=227, userData_483=228, userData_484=229, userData_485=230, userData_486=231, userData_487=232, userData_488=233, userData_489=234, userData_490=235, userData_491=236, userData_492=237, userData_493=238, userData_494=239, userData_495=240, userData_496=241, userData_497=242, userData_498=243, userData_499=244, userData_500=245, userData_501=246, userData_502=247, userData_503=1, userData_504=2, fecBits=1, ebno=0.0, reserved1=0)>",
        )

    def testRXMPMPV1(self):  # test parser of RXM-PMP v1 message
        rxm_pmpv1 = b"\xb5b\x02\x72\x23\x00\x01\x00\x0b\x00\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x00\x01\x01\x02\x01\x00"
        for i in range(11):
            rxm_pmpv1 += i.to_bytes(1, "little", signed=False)
        rxm_pmpv1 += b"\x00\x20"
        res = UBXReader.parse(rxm_pmpv1, msgmode=SET)
        self.assertEqual(
            str(res),
            "<UBX(RXM-PMP, version=1, reserved0=0, numBytesUserData=11, timeTag=67305985, uniqueWord1=67305985, uniqueWord2=67305985, serviceIdentifier=513, spare=0, uniqueWordBitErrors=1, fecBits=513, ebno=0.125, reserved1=0, userData_01=0, userData_02=1, userData_03=2, userData_04=3, userData_05=4, userData_06=5, userData_07=6, userData_08=7, userData_09=8, userData_10=9, userData_11=10)>",
        )

    def testRXMRLMS(self):  # test parser of RXM-RLM-S message
        rxm_rlms = b"\xb5b\x02\x59\x10\x00\x00\x01\x00\x00"
        for i in range(8):
            rxm_rlms += i.to_bytes(1, "little", signed=False)
        rxm_rlms += b"\x00\x01\x02\x00\x8b\xbd"
        res = UBXReader.parse(rxm_rlms)
        self.assertEqual(
            str(res),
            "<UBX(RXM-RLM, version=0, type=1, svId=0, reserved0=0, beacon=506097522914230528, message=0, params=513, reserved1=0)>",
        )

    def testRXMRLML(self):  # test parser of RXM-RLM-L message
        rxm_rlms = b"\xb5b\x02\x59\x1c\x00\x00\x02\x00\x00"
        for i in range(8):
            rxm_rlms += i.to_bytes(1, "little", signed=False)
        rxm_rlms += b"\x00"
        for i in range(12):
            rxm_rlms += i.to_bytes(1, "little", signed=False)
        rxm_rlms += b"\x00\x01\x02\xda\x81"
        res = UBXReader.parse(rxm_rlms)
        self.assertEqual(
            str(res),
            "<UBX(RXM-RLM, version=0, type=2, svId=0, reserved0=0, beacon=506097522914230528, message=0, params=3416467015609337987117220096, reserved1=131328)>",
        )

    def testMONSPAN2(self):  # test parser of MON-SPAN message (repeating groups empty)
        mon_span = b"\xb5b\x0a\x31\x04\x00\x00\x00\x01\x02"
        mon_span += b"\x42\xc3"
        res = UBXReader.parse(mon_span)
        self.assertEqual(
            str(res), "<UBX(MON-SPAN, version=0, numRfBlocks=0, reserved0=513)>"
        )

    def testMGAINI1(self):  # test parser of MGA-INI input message with kwargs
        res = UBXReader.parse(self.mga_ini1, msgmode=SET)
        self.assertEqual(
            str(res),
            "<UBX(MGA-INI-POS-LLH, type=1, version=0, reserved0=513, lat=6.7305985, lon=6.7305985, alt=67305985, posAcc=67305985)>",
        )

    def testMGAINI2(self):  # test parser of MGA-INI input message with args
        res = UBXReader.parse(self.mga_ini1, validate=VALCKSUM, msgmode=SET)
        self.assertEqual(
            str(res),
            "<UBX(MGA-INI-POS-LLH, type=1, version=0, reserved0=513, lat=6.7305985, lon=6.7305985, alt=67305985, posAcc=67305985)>",
        )

    def testESFSTATUS(self):  # test parser of ESF-STATUS message
        res = UBXReader.parse(self.esf_status)
        # print(res)
        self.assertEqual(
            str(res),
            #"<UBX(ESF-STATUS, iTOW=23:59:42, version=2, reserved0=548, fusionMode=0, reserved1=0, numSens=6, type_01=5, used_01=0, ready_01=1, calibStatus_01=0, timeStatus_01=1, freq_01=0, badMeas_01=0, badTTag_01=0, missingMeas_01=0, noisyMeas_01=0, type_02=13, used_02=0, ready_02=0, calibStatus_02=0, timeStatus_02=1, freq_02=10, badMeas_02=0, badTTag_02=0, missingMeas_02=0, noisyMeas_02=0, type_03=14, used_03=0, ready_03=1, calibStatus_03=0, timeStatus_03=1, freq_03=10, badMeas_03=0, badTTag_03=0, missingMeas_03=0, noisyMeas_03=0, type_04=0, used_04=0, ready_04=0, calibStatus_04=0, timeStatus_04=1, freq_04=10, badMeas_04=0, badTTag_04=0, missingMeas_04=0, noisyMeas_04=0, type_05=1, used_05=0, ready_05=0, calibStatus_05=0, timeStatus_05=0, freq_05=10, badMeas_05=0, badTTag_05=0, missingMeas_05=0, noisyMeas_05=0, type_06=18, used_06=0, ready_06=1, calibStatus_06=0, timeStatus_06=1, freq_06=0, badMeas_06=0, badTTag_06=0, missingMeas_06=0, noisyMeas_06=0)>",
            "<UBX(ESF-STATUS, iTOW=23:59:42, version=2, wtInitStatus=0, mntAlgStatus=1, insInitStatus=1, imuInitStatus=2, reserved0=0, fusionMode=0, reserved1=0, numSens=6, type_01=5, used_01=0, ready_01=1, calibStatus_01=0, timeStatus_01=1, freq_01=0, badMeas_01=0, badTTag_01=0, missingMeas_01=0, noisyMeas_01=0, type_02=13, used_02=0, ready_02=0, calibStatus_02=0, timeStatus_02=1, freq_02=10, badMeas_02=0, badTTag_02=0, missingMeas_02=0, noisyMeas_02=0, type_03=14, used_03=0, ready_03=1, calibStatus_03=0, timeStatus_03=1, freq_03=10, badMeas_03=0, badTTag_03=0, missingMeas_03=0, noisyMeas_03=0, type_04=0, used_04=0, ready_04=0, calibStatus_04=0, timeStatus_04=1, freq_04=10, badMeas_04=0, badTTag_04=0, missingMeas_04=0, noisyMeas_04=0, type_05=1, used_05=0, ready_05=0, calibStatus_05=0, timeStatus_05=0, freq_05=10, badMeas_05=0, badTTag_05=0, missingMeas_05=0, noisyMeas_05=0, type_06=18, used_06=0, ready_06=1, calibStatus_06=0, timeStatus_06=1, freq_06=0, badMeas_06=0, badTTag_06=0, missingMeas_06=0, noisyMeas_06=0)>",
        )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
