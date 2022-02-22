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
        "RequestTimestamp": "2022-02-22 11:19:52",
        "PeriodFrom": "2021-05-10",
        "PeriodTo": "2021-05-30",
        "NumberOfPasses": 5,
        "PassesList": [
            {
            "PassIndex": 1,
            "PassID": "SMV1544228",
            "StationID": "AO09",
            "TimeStamp": "2021-05-22T21:07:00",
            "VehicleID": "KB55KTM48860",
            "Charge": "2.8"
            },
            {
            "PassIndex": 2,
            "PassID": "GLS2058880",
            "StationID": "AO01",
            "TimeStamp": "2021-05-10T07:10:00",
            "VehicleID": "QO77TFN61853",
            "Charge": "2.8"
            },
            {
            "PassIndex": 3,
            "PassID": "ZLV3589994",
            "StationID": "AO06",
            "TimeStamp": "2021-05-29T03:47:00",
            "VehicleID": "WY00MLL63827",
            "Charge": "2.8"
            },
            {
            "PassIndex": 4,
            "PassID": "ZXJ8435667",
            "StationID": "AO14",
            "TimeStamp": "2021-05-14T12:57:00",
            "VehicleID": "YH66OKD41942",
            "Charge": "2.8"
            },
            {
            "PassIndex": 5,
            "PassID": "JSG8629778",
            "StationID": "AO04",
            "TimeStamp": "2021-05-10T01:35:00",
            "VehicleID": "ZY93PCY41868",
            "Charge": "2.8"
            }
        ]
    },
    "PassesAnalysis 402":
    {
        "op1_ID": "AO",
        "op2_ID": "KO",
        "RequestTimestamp": "2022-02-22 20:02:28",
        "PeriodFrom": "2020-04-25",
        "PeriodTo": "2020-04-20",
        "NumberOfPasses": 0,
        "PassesList": []
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
    "PassesCost 402":
    {
    "op1_ID": "AO",
    "op2_ID": "KO",
    "RequestTimestamp": "2022-02-22 20:08:32",
    "PeriodFrom": "2020-04-30",
    "PeriodTo": "2020-04-29",
    "NumberOfPasses": 0,
    "PassesCost": 0
    },

    "PassesPerStation":
    {
        "Station": "EG03",
        "StationOperator": "egnatia",
        "RequestTimestamp": "2022-02-22 19:10:58",
        "PeriodFrom": "2020-04-10",
        "PeriodTo": "2020-04-15",
        "NumberOfPasses": 4,
        "PassesList": [
            {
            "PassIndex": 1,
            "PassID": "HIZ9464270",
            "PassTimeStamp": "2020-04-11T16:04:00",
            "VehicleID": "DW44ZOO26361",
            "TagProvider": "egnatia",
            "PassType": "home",
            "PassCharge": "2.5"
            },
            {
            "PassIndex": 2,
            "PassID": "KAJ5037577",
            "PassTimeStamp": "2020-04-11T16:56:00",
            "VehicleID": "CM15YCB60994",
            "TagProvider": "egnatia",
            "PassType": "home",
            "PassCharge": "2.0"
            },
            {
            "PassIndex": 3,
            "PassID": "PHR0622064",
            "PassTimeStamp": "2020-04-11T22:34:00",
            "VehicleID": "JV67MTI17124",
            "TagProvider": "nea_odos",
            "PassType": "visitor",
            "PassCharge": "1.0"
            },
            {
            "PassIndex": 4,
            "PassID": "XGI8326917",
            "PassTimeStamp": "2020-04-13T20:35:00",
            "VehicleID": "TE24LCO18661",
            "TagProvider": "egnatia",
            "PassType": "home",
            "PassCharge": "1.25"
            }
        ]
    },
    "PassesPerStation 402":
    {
        "Station": "MR01",
        "StationOperator": "moreas",
        "RequestTimestamp": "2022-02-22 19:45:09",
        "PeriodFrom": "2020-04-30",
        "PeriodTo": "2020-04-20",
        "NumberOfPasses": 0,
        "PassesList": []
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