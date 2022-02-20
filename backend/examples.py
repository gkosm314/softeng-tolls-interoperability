# This dictionary contains examples for the following cases:
#   - ChargesBy
#   - PassesAnalysis
#   - PassesCost
#   - PassesPerStation
#   - Unauthorized_invalidToken
#   - Unauthorized_noCredentials

ourdict = {
    "ChargesBy":
    {
        "op_ID": "AO",
        "RequestTimestamp": "2022-02-18 16:27:55",
        "PeriodFrom": "2020-10-01",
        "PeriodTo": "2020-10-10",
        "PPOList": [
            {
                "VisitingOperator": "EG",
                "NumberOfPasses": 5,
                "PassesCost": 14.0
            },
            {
                "VisitingOperator": "GF",
                "NumberOfPasses": 3,
                "PassesCost": 8.399999999999999
            },
            {
                "VisitingOperator": "KO",
                "NumberOfPasses": 3,
                "PassesCost": 8.399999999999999
            },
            {
                "VisitingOperator": "MR",
                "NumberOfPasses": 1,
                "PassesCost": 2.8
            },
            {
                "VisitingOperator": "NE",
                "NumberOfPasses": 3,
                "PassesCost": 8.399999999999999
            },
            {
                "VisitingOperator": "OO",
                "NumberOfPasses": 8,
                "PassesCost": 22.400000000000002
            }
        ]
    },

    "PassesAnalysis":
    {
        "op1_ID": "AO",
        "op2_ID": "KO",
        "RequestTimestamp": "2022-02-19 15:00:00",
        "PeriodFrom": "2021-05-10",
        "PeriodTo": "2021-06-10",
        "NumberOfPasses": 10,
        "PassesList": [
            {
                "passid": "MRV8379613",
                "timestamp": "2021-06-06T10:03:00",
                "charge": 2.8,
                "ishome": 0,
                "stationref": "AO12",
                "vehicleref": "DO24BCW15511",
                "providerabbr": 1
            },
            {
                "passid": "POA7570830",
                "timestamp": "2021-06-09T21:27:00",
                "charge": 2.8,
                "ishome": 0,
                "stationref": "AO05",
                "vehicleref": "HW75BKT77773",
                "providerabbr": 1
            },
            {
                "passid": "SMV1544228",
                "timestamp": "2021-05-22T21:07:00",
                "charge": 2.8,
                "ishome": 0,
                "stationref": "AO09",
                "vehicleref": "KB55KTM48860",
                "providerabbr": 1
            },
            {
                "passid": "OII8257294",
                "timestamp": "2021-05-31T21:05:00",
                "charge": 2.8,
                "ishome": 0,
                "stationref": "AO18",
                "vehicleref": "MQ65WJJ60020",
                "providerabbr": 1
            },
            {
                "passid": "GLS2058880",
                "timestamp": "2021-05-10T07:10:00",
                "charge": 2.8,
                "ishome": 0,
                "stationref": "AO01",
                "vehicleref": "QO77TFN61853",
                "providerabbr": 1
            },
            {
                "passid": "NAB8968920",
                "timestamp": "2021-06-06T17:21:00",
                "charge": 2.8,
                "ishome": 0,
                "stationref": "AO13",
                "vehicleref": "QW79CHL42244",
                "providerabbr": 1
            },
            {
                "passid": "CLF8749027",
                "timestamp": "2021-06-09T06:01:00",
                "charge": 2.8,
                "ishome": 0,
                "stationref": "AO16",
                "vehicleref": "UO75YNW62238",
                "providerabbr": 1
            },
            {
                "passid": "ZLV3589994",
                "timestamp": "2021-05-29T03:47:00",
                "charge": 2.8,
                "ishome": 0,
                "stationref": "AO06",
                "vehicleref": "WY00MLL63827",
                "providerabbr": 1
            },
            {
                "passid": "ZXJ8435667",
                "timestamp": "2021-05-14T12:57:00",
                "charge": 2.8,
                "ishome": 0,
                "stationref": "AO14",
                "vehicleref": "YH66OKD41942",
                "providerabbr": 1
            },
            {
                "passid": "JSG8629778",
                "timestamp": "2021-05-10T01:35:00",
                "charge": 2.8,
                "ishome": 0,
                "stationref": "AO04",
                "vehicleref": "ZY93PCY41868",
                "providerabbr": 1
            }
        ]
    },

    "PassesCost":
    {
        "op1_ID": "AO",
        "op2_ID": "EG",
        "RequestTimestamp": "2022-02-19 15:00:50",
        "PeriodFrom": "2021-10-05",
        "PeriodTo": "2021-10-10",
        "NumberOfPasses": 2,
        "PassesCost": 5.6
    },

    "PassesPerStation":
    {
        "Station": "EG05",
        "StationOperator": "egnatia",
        "RequestTimestamp": "2022-02-19 15:01:38",
        "PeriodFrom": "2020-05-01",
        "PeriodTo": "2020-05-10",
        "NumberOfPasses": 2,
        "PassesList": [
            {
                "passid": "DFC5897825",
                "timestamp": "2020-05-07T02:40:00",
                "charge": 3.1,
                "ishome": 1,
                "stationref": "EG05",
                "vehicleref": "TZ48CCW54765",
                "providerabbr": 3
            },
            {
                "passid": "QGD4799312",
                "timestamp": "2020-05-07T19:29:00",
                "charge": 3.1,
                "ishome": 0,
                "stationref": "EG05",
                "vehicleref": "XV40HUQ04740",
                "providerabbr": 3
            }
        ]
    },

    "Unauthorized_invalidToken":
    {
        "detail": "Given token not valid for any token type",
        "code": "token_not_valid",
        "messages": [
            {
                "token_class": "AccessToken",
                "token_type": "access",
                "message": "Token is invalid or expired"
            }
        ]
    },

    "Unauthorized_noCredentials":
    {
        "detail": "Authentication credentials were not provided."
    }

}