//在该js中，定义并实现与后端对接的api

import {
    systemGetTotalUsersUrl, systemAddOneUserUrl, systemGetTotalRoleTeamUrl,
    systemGetTotalUserTeamUrl, systemGetOneUserUrl, systemSetOneUserUrl, systemDelOneUserUrl, systemAddOneUserTeamUrl, systemDelOneUserTeamUrl, systemSetOneUserTeamUrl, systemGetOneUserTeamUrl, systemAddOneRoleTeamUrl, systemDelOneRoleTeamUrl, systemSetOneRoleTeamUrl, systemGetOneRoleTeamUrl, officeSuggestionUrl, officeDataExporeUrl, indexMajorFocusTableUrl, indexMajorFocusGrowLineUrl, indexMajorFocusGrowBarUrl, personGetBasicUrl, personGetEventInfoUrl, personGetPersonScoreInfoUrl, personGetPersonTripInfoUrl, personGetPersonCardfInfoUrl,
    personAddEventInfoUrl, personAddFocusInfoUrl, personCancelFocusInfoUrl, loginUrl, officeDataFilterUrl
} from "@/api/httpapi"
import { myAxios } from '@/main'

//登录
export const login = (data) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(loginUrl, data).then(
            (res) => {
                resolve(res['data'])
            }
        )
    })
    return p
}

//获取首页列表框要展示的数据以及列的名+数据的key
export const getIndexTableInfo = (userid) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(indexMajorFocusTableUrl, { userId: userid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            colName: ["姓名", "性别", "学号", "专业", "公寓", "房间号", "状态"],
            propName: ["name", "sex", "stuId", "major", "department", "room", "status"],
            data: []
        } */
}

//获取首页重点关注折线趋势数据
export const getIndexMajorLineInfo = (userid) => {

    var p = new Promise(function (resolve, reject) {
        myAxios.post(indexMajorFocusGrowLineUrl, { userId: userid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p

    /*  return {
         date: ["2017-01", "2017-02", "2017-03", "2017-04", "2017-05", "2017-06"],
         "全校学生": [70, 203, 165, 70, 203, 165],
         "计算机院": [30, 150, 80, 30, 150, 80],
         "土木学院": [40, 53, 85, 40, 53, 85],
         "外语学院": [50, 58, 22, 77, 53, 85],
     } */
}

//获取首页重点关注柱状图趋势数据
export const getIndexMajorBarInfo = (userid) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(indexMajorFocusGrowBarUrl, { userId: userid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            date: ["2017-01", "2017-02", "2017-03"],
            "17": [100, 200, 150],
            "16": [30, 50, 80],
            "15": [30, 50, 80],
            "14": [30, 50, 80],
        } */
}

//获取个人页上该学生的基础信息
export const getPersonBasicInfo = (userid, stuid) => {

    var p = new Promise(function (resolve, reject) {
        myAxios.post(personGetBasicUrl, { userId: userid, stuId: stuid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p

    /* return {
        basicInfo: {
            colName: ["学号", "班号", "姓名", "性别", "民族", "政治面貌", "学历", "身份证号", "公寓号", "宿舍号", "毕业高中", "手机号", "家庭地址", "父亲姓名", "父亲工作单位", "父亲手机号", "母亲姓名", "母亲工作单位", "母亲手机号"],
            propName: ["stuID", "stuClassNumber", "stuName", "sex", "nationality", "politicalLandscape", "stuEducation", "idNumber", "apartmentNumber", "dormitoryNumber", "graduatedHighSchool", "stuMobileNumber", "homeAddress", "fatherName", "fatherWorkUnit", "fatherMobileNumber", "motherName", "motherWorkUnit", "motherMobileNumber"],
            data: {
                stuID: "110410120",
                stuClassNumber: "1104101",
                stuName: "张三",
                sex: "男",
                nationality: "汉族",
                politicalLandscape: "党员",
                stuEducation: "本科",
                idNumber: "610112411512210598",
                apartmentNumber: "6",
                dormitoryNumber: "404",
                graduatedHighSchool: "XX高中",
                stuMobileNumber: "18363120012",
                homeAddress: "XX省XX市场",
                fatherName: "张三爸",
                fatherWorkUnit: "XX工作单位",
                fatherMobileNumber: "18363120013",
                motherName: "张三妈",
                motherWorkUnit: "XX工作单位",
                motherMobileNumber: "18363120014"
            }
        },
        focusInfo: {
            focusReason: "延期毕业",
            focusLevel: "推介关注"//当为正常或者毕业时，Reason为空
        }
    } */
}

//获取个人页上该学生的成绩信息
export const getPersonScoreInfo = (userid, stuid) => {

    var p = new Promise(function (resolve, reject) {
        myAxios.post(personGetPersonScoreInfoUrl, { userId: userid, stuId: stuid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*  return {
         totalNum: 30,//查询到的该生的考试数量
         failNum: 15,//其中挂科的数量
         colName: ["课程号", "课序号", "初始成绩", "补考成绩", "考试时间", "是否重修"],
         propName: ["courseID", "courseIndex", "initialScore", "makeUpScore", "examDate", "repairOrNot"],
         data: [
             {
                 courseID: "EC5444646355",//课程号
                 courseIndex: "1",//课序号
                 initialScore: "45.2", //初始成绩
                 makeUpScore: "0",//补考成绩
                 examDate: "2017-01-04 20:20:50",//考试时间
                 repairOrNot: "是"//是否重修
             },
             {
                 courseID: "EC5444646355",//课程号
                 courseIndex: "1",//课序号
                 initialScore: "45.2", //初始成绩
                 makeUpScore: "0",//补考成绩
                 examDate: "2017-01-04 20:20:50",//考试时间
                 repairOrNot: "是"//是否重修
             }
         ]
     } */
}

//获取个人页上该学生的进出信息
export const getPersonTripInfo = (userid, stuid) => {

    var p = new Promise(function (resolve, reject) {
        myAxios.post(personGetPersonTripInfoUrl, { userId: userid, stuId: stuid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /* return {
        totalNum: 30,
        failNum: 10,
        normolWord: "正常时间归寝",
        unNormolWord: "晚于23点归寝",
        colName: [
            "通过公寓号",
            "离开时间",
            "进入时间"
        ],
        propName: [
            "department",
            "exitTime",
            "entryTime"
        ],
        data: [
            {
                department: "2#",
                exitTime: "2017-01-01 20:33:45",
                entryTime: "2017-01-01 20:00:00"
            },
            {
                department: "2#",
                exitTime: "2017-01-01 20:33:45",
                entryTime: "2017-01-01 20:00:00"
            },
            {
                department: "2#",
                exitTime: "2017-01-01 20:33:45",
                entryTime: "2017-01-01 20:00:00"
            }
        ]
    } */
}

//获取个人页上该学生的消费信息
export const getPersonCardInfo = (userid, stuid) => {

    var p = new Promise(function (resolve, reject) {
        myAxios.post(personGetPersonCardfInfoUrl, { userId: userid, stuId: stuid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /* return {
        date: ["2010-01-01", "2010-01-03", "2010-01-03", "2010-01-03", "2010-01-03", "2010-01-03"],
        consume: [30, 198, 30, 198, 30, 198],
        colName: [
            "商户名称",
            "金额",
            "消费时间",
            "消费类型"
        ],
        propName: [
            "storeName",
            "count",
            "time",
            "type"
        ],
        data: [
            {
                "storeName": "超市",
                "count": 30,//绝对值
                "time": "2017-01-01 20:20:29",
                "type": "持卡人消费"
            }
        ]
    } */
}

//获取个人页上该学生的事件记录
export const getPersonEventInfo = (userid, stuid) => {

    var p = new Promise(function (resolve, reject) {
        myAxios.post(personGetEventInfoUrl, { userId: userid, stuId: stuid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*  return {
         colName: [
             "时间",
             "事件主题",
             "事件内容",
             "事件记录人"
         ],
         propName: [
             "time",
             "thmeme",
             "content",
             "author"
         ],
         data: [
             {
                 time: "2017-04-04 20:55:55",
                 thmeme: "王导员的一次记录",
                 content: "今天跟XXX聊天，感觉到XXX有XXX倾向，记录下",
                 author: "admin"
             },
             {
                 time: "2017-04-07 20:55:55",
                 thmeme: "李导员的一次记录",
                 content: "今天跟XXX聊天，感觉到XXX有XXX倾向，记录下",
                 author: "admin"
             }
         ]
     } */
}

//向后端发送添加一条事件记录的请求
export const postPersonAddEvent = (data) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(personAddEventInfoUrl, { data }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p

    /*data样例：{
    "stuId":"11012231",
    "userId":"admin",
    "theme":"记录一次谈话",
    "time":"2017-01-01 20:20:22",
    "content":"巴拉巴拉"
}*/

}

//向后端发起一条将学生状态从关注制成正常的请求
export const postPersonCancelFocus = (data) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(personCancelFocusInfoUrl, { data }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*data样例：{
    "stuId":"11012231",
    "userId":"admin",
}
    返回的样例： {
        "status":1,//1代表成功取消关注、0表示失败，前端可提供操作失败、请重试
        }
    */
    // return { status: 1 }
}

//向后端发起一条将学生状态从正常制成关注的请求
export const postPersonAddFocus = (data) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(personAddFocusInfoUrl, { data }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p


    /*data样例：    {
        "stuId":"11012231",
    "userId":"admin",
    "focusLevel":0,//0表示重点关注， 1表示推介关注
    "reson":"巴兰巴拉"
*/

    /*
    返回的样例： {
        "status":1,//1代表成功取消关注、0表示失败，前端可提供操作失败、请重试
        }
    */

    return { status: 1 }
}

//获取数据导出界面上的数据
export const officeDataExpore = (userid) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(officeDataExporeUrl, { userId: userid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            colName: ["姓名", "性别", "学号", "专业", "民族", "公寓", "房间号", "身份证号", "政治面貌", "学历", "毕业高中", "联系电话", "家庭住址", "状态"],
            propName: ["name", "sex", "stuId", "major", "nation", "department", "room", "idNumber", "political", "education", "graduatedHighSchool", "phoneNumber", "homeAddress", "status"],
            data: [{
                "name": "张三",
                "stuId": "学号",
                "sex": "男",
                "nation": "汉族",
                "major": "计算机科学与技术",
                "department": "6公寓",
                "room": "404",
                "idNumber": "61021324821462122",
                "political": "党员",//政治面貌
                "education": "本科",
                "graduatedHighSchool": "某某高中",//毕业高中
                "phoneNumber": "1532255622",
                "homeAddress": "某某地方",
                "status": "正常"
            }, {
                "name": "张三",
                "stuId": "学号",
                "sex": "男",
                "nation": "汉族",
                "major": "计算机科学与技术",
                "department": "6公寓",
                "room": "404",
                "idNumber": "61021324821462122",
                "political": "党员",//政治面貌
                "education": "本科",
                "graduatedHighSchool": "某某高中",//毕业高中
                "phoneNumber": "1532255622",
                "homeAddress": "某某地方",
                "status": "正常"
            }, {
                "name": "张三",
                "stuId": "学号",
                "sex": "男",
                "nation": "汉族",
                "major": "计算机科学与技术",
                "department": "6公寓",
                "room": "404",
                "idNumber": "61021324821462122",
                "political": "党员",//政治面貌
                "education": "本科",
                "graduatedHighSchool": "某某高中",//毕业高中
                "phoneNumber": "1532255622",
                "homeAddress": "某某地方",
                "status": "重点关注"
            }]
        } */
}

//json转成excel导出的函数
export const JSONToExcelConvertor = (JSONData, FileName, ShowLabel) => {
    //先转化json
    var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;

    var excel = '<table>';

    //设置表头
    var row = "<tr>";
    for (var i = 0, l = ShowLabel.length; i < l; i++) {
        row += "<td>" + ShowLabel[i] + '</td>';
    }


    //换行
    excel += row + "</tr>";

    //设置数据
    for (var i = 0; i < arrData.length; i++) {
        var row = "<tr>";

        for (var index in arrData[i]) {
            var value = arrData[i][index] === "." ? "" : arrData[i][index];
            row += '<td>' + value + '</td>';
        }

        excel += row + "</tr>";
    }

    excel += "</table>";

    var excelFile = "<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:x='urn:schemas-microsoft-com:office:excel' xmlns='http://www.w3.org/TR/REC-html40'>";
    excelFile += '<meta http-equiv="content-type" content="application/vnd.ms-excel; charset=UTF-8">';
    excelFile += '<meta http-equiv="content-type" content="application/vnd.ms-excel';
    excelFile += '; charset=UTF-8">';
    excelFile += "<head>";
    excelFile += "<!--[if gte mso 9]>";
    excelFile += "<xml>";
    excelFile += "<x:ExcelWorkbook>";
    excelFile += "<x:ExcelWorksheets>";
    excelFile += "<x:ExcelWorksheet>";
    excelFile += "<x:Name>";
    excelFile += "{worksheet}";
    excelFile += "</x:Name>";
    excelFile += "<x:WorksheetOptions>";
    excelFile += "<x:DisplayGridlines/>";
    excelFile += "</x:WorksheetOptions>";
    excelFile += "</x:ExcelWorksheet>";
    excelFile += "</x:ExcelWorksheets>";
    excelFile += "</x:ExcelWorkbook>";
    excelFile += "</xml>";
    excelFile += "<![endif]-->";
    excelFile += "</head>";
    excelFile += "<body>";
    excelFile += excel;
    excelFile += "</body>";
    excelFile += "</html>";


    var uri = 'data:application/vnd.ms-excel;charset=utf-8,' + encodeURIComponent(excelFile);

    var link = document.createElement("a");
    link.href = uri;

    link.style = "visibility:hidden";
    link.download = FileName + ".xlsx";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

//异常数据筛选
export const officeDataFilter = (data) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(officeDataFilterUrl, data, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
}

//获取所有用户组信息用以展示
export const systemGetTotalUserTeam = (userid) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemGetTotalUserTeamUrl, { userId: userid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            colName: ["用户组名称", "描述"],
            propName: ["name", "description"],
            data: [
                {
                    name: "一号用户组",
                    description: "巴拉巴拉一号",
                },
                {
                    name: "二号用户组",
                    description: "巴拉巴拉二号",
                }
            ]
        } */
}

//获取某一个用户组的可查看班级权限用以展示
export const systemGetOneUserTeam = (userid, userTeamName) => {

    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemGetOneUserTeamUrl, { userId: userid, userTeamName: userTeamName }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p

    /* return {
        data: {
            "1101401": "1",
            "1101141": "1",
            "1101142": "1",
            "1101143": "1",
            "1101144": "1",
            "1101145": "1",
            "1101146": "1",
            "1101147": "1",
            "1101148": "1",
            "1101149": "0",
        }
    } */
}

//向后端发送一条设置用户组权限的请求
export const systemSetOneUserTeam = (userid, userTeamName, data) => {
    /*
    "userId":"admin",
    "userTeamName":"一号用户组",
    "data":{
        //0表示未勾选，1表示勾选
        "1101401":"0",
        "1101141":"1",
        "1101142":"1",
        "1101143":"1",
        "1101144":"0",
        "1101145":"1",
        "1101146":"1",
        "1101147":"1",
        "1101148":"0",
        "1101149":"0",
    }
    */
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemSetOneUserTeamUrl, { userId: userid, userTeamName: userTeamName, data: data }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            status: 1,//1表示成功，0表示失败
            errorInfo: "该用户没有权限"//status为0时，前端展示errorinfo
        } */
}

//向后端发送一条添加用户组信息的请求
export const systemAddOneUserTeam = (userid, data) => {
    /*
    "userId": "admin",
    "data": {
        "name": "用户组三",
        "description": "巴拉巴拉",
    }
    */
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemAddOneUserTeamUrl, { userId: userid, data: data }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            status: 1,//1表示成功，0表示失败
            errorInfo: "该用户没有权限"//status为0时，前端展示errorinfo
        } */
}

//向后端发送一条删除用户组权限的请求
export const systemDelOneUserTeam = (userid, userTeamName) => {
    /*
    "userId":"admin",
    "userTeamName":"一号用户组",
    */
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemDelOneUserTeamUrl, { userId: userid, userTeamName: userTeamName }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            status: 1,//1表示成功，0表示失败
            errorInfo: "还有用户存在于该用户组内"//status为0时，前端展示errorinfo
        } */
}

//获取所有角色组信息用以展示
export const systemGetTotalRoleTeam = (userid) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemGetTotalRoleTeamUrl, { userId: userid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            colName: ["角色组名称", "描述"],
            propName: ["name", "description"],
            data: [
                {
                    "name": "一号角色组",
                    "description": "巴拉巴拉",
                },
                {
                    "name": "二号角色组",
                    "description": "巴拉巴拉",
                }
            ]
        } */
}

//获取某一个角色组的可查看页面权限用以展示
export const systemGetOneRoleTeam = (userid, roleTeamName) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemGetOneRoleTeamUrl, { userId: userid, roleTeamName: roleTeamName }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /* return {
        data: {
            indexMajor: 1, //0表示不可以看
            indexStudents: 1,
            person: 1,
            officeDataExpore: 0,
            officeSuggestions: 0,
            dataUpdateBasic: 0,
            dataUpdateScore: 0,
            systemUserTeam: 0,//用户组权限设定页
            systemRoleTeam: 0,//角色组权限设定页
            systemUsers: 1//用户设定页
        }
    } */
}

//获得该用户的角色组权限
export const getPagePower = (userid) => {
    //this.$http
    //与systemGetOneRoleTeam的差异为：本函数不会查看userid是否有查看角色设置页的权限，只会返回该userid的页面权限
    return {
        indexMajor: true,
        indexStudents: true,
        person: true,
        officeDataExpore: true,
        officeSuggestions: true,
        dataFilter: true,
        systemUserTeam: true,
        systemUsers: true,
        systemRoleTeam: true,
        dataUpdateBasic: true,
        dataUpdateScore: true,
    };

}

//向后端发送一条删除角色组权限的请求
export const systemDelOneRoleTeam = (userid, userRoleName) => {
    /*
    "userId":"admin",
    "roleTeamName":"一号角色组",
    */
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemDelOneRoleTeamUrl, { userId: userid, roleTeamName: userRoleName }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            status: 1,//1表示成功，0表示失败
            errorInfo: "还有用户存在于该角色组内"//status为0时，前端展示errorinfo
        } */
}

//向后端发送一条设置角色组权限的请求
export const systemSetOneRoleTeam = (userid, roleTeamName, data) => {
    /*
    "userId":"admin",
    "roleTeamName":"一号角色组",
    "data":{
        //0表示未勾选，1表示勾选
        "index": 0, //0表示不可以看
        "person": 0,
        "officeExport": 0,
        "officeSuggestion": 0,
        "dataUpdateBasic": 0,
        "dataUpdateScore": 0,
        "systemUserTeam": 0, //用户组权限设定页
        "systemRoleTeam": 0, //角色组权限设定页
        "systemUsers": 0 //用户设定页
    }
    */
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemSetOneRoleTeamUrl, { userId: userid, roleTeamName: roleTeamName, data: data }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            status: 1,//1表示成功，0表示失败
            errorInfo: "该用户没有权限"//status为0时，前端展示errorinfo
        } */
}

//向后端发送一条添加用户组信息的请求
export const systemAddOneRoleTeam = (userid, data) => {
    /*
    "userId": "admin",
    "data": {
        "name": "角色组三",
        "description": "巴拉巴拉",
    }
    */
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemAddOneRoleTeamUrl, { userId: userid, data: data }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            status: 1,//1表示成功，0表示失败
            errorInfo: "该用户没有权限"//status为0时，前端展示errorinfo
        } */
}

//获取所有用户信息用以展示
export const systemGetTotalUsers = (userid) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemGetTotalUsersUrl, { userId: userid }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return res
        return {
            colName: ["用户名", "描述", "所在角色组", "所在用户组", "密码"],
            propName: ["name", "description", "roleTeamName", "userTeamName", "passWord"],
            data: [
                {
                    name: "王导员",
                    description: "巴拉巴拉",
                    roleTeamName: "一号角色组",
                    userTeamName: "一号用户组",
                    passWord: "XXX"
                },
                {
                    name: "李导员",
                    description: "巴拉巴拉",
                    roleTeamName: "二号角色组",
                    userTeamName: "二号用户组",
                    passWord: "XXX"
                },
                {
                    name: "张导员",
                    description: "巴拉巴拉1",
                    roleTeamName: "二号角色组",
                    userTeamName: "一号用户组",
                    passWord: "XXX"
                }
            ]
        } */
}

//获取某一个角色组的可查看页面权限用以展示
export const systemGetOneUser = (userid, userName) => {
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemGetOneUserUrl, { userId: userid, userName: userName }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*     return {
            data: {
                name: "用户一",
                description: "巴拉巴拉",
                userTeamName: "一号用户组",
                roleTeamName: "一号角色组",
                passWord: "XXX"
            }
        } */
}

//向后端发送一条删除用户的请求
export const systemDelOneUser = (userid, userName) => {
    /*
    "userId":"admin",
    "userName":"用户一",
    */
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemDelOneUserUrl, { userId: userid, userName: userName }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*
        return {
            status: 1,//1表示成功，0表示失败
            errorInfo: "用户没有权限删除"//status为0时，前端展示errorinfo
        } */
}

//向后端发送一条更改用户信息的请求
export const systemSetOneUser = (userid, name, data) => {
    /*
    "userId": "admin",
    "name": "用户一",
    "data": {
        "name": "用户一",
        "description": "巴拉巴拉",
        "userTeamName": "用户组一",
        "roleTeamName": "角色组一",
        "passWord": "1234",
    }
    */
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemSetOneUserUrl, { userId: userid, name: name, data: data }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*
        return {
            status: 1,//1表示成功，0表示失败
            errorInfo: "该用户没有权限"//status为0时，前端展示errorinfo
        } */
}

//向后端发送一条添加用户信息的请求
export const systemAddOneUser = (userid, data) => {
    /*
    "userId": "admin",
    "data": {
        "name": "用户三",
        "description": "巴拉巴拉",
        "userTeamName": "用户组一",
        "roleTeamName": "角色组一",
        "passWord": "1234",
    }
    */
    var p = new Promise(function (resolve, reject) {
        myAxios.post(systemAddOneUserUrl, { userId: userid, data: data }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /*    return {
           status: 1,//1表示成功，0表示失败
           errorInfo: "该用户没有权限"//status为0时，前端展示errorinfo
       } */
}

//向后端发送一条反馈的意见
export const officeSuggestions = (userid, content, start) => {
    /*
    "userId":"admin",
    "content":"巴拉巴拉",
    "start":5
    */
    var p = new Promise(function (resolve, reject) {
        myAxios.post(officeSuggestionUrl, { userId: userid, content: content, start: start }, { headers: { 'Content-Type': 'application/json' } }).then(
            (respone) => {
                resolve(respone['data'])
            }
        )
    })
    return p
    /* return {
        status: 1,//1表示成功，0表示失败
        errorInfo: "该用户没有权限"//status为0时，前端展示errorinfo
    } */
}

//获得学生基本数据模板下载
export const dataGetModeBasic = () => {
    return { "学号": "stuID", "班号": "stuClassNumber", "姓名": "stuName", "性别": "sex", "民族": "nationality", "政治面貌": "politicalLandscape", "学历": "stuEducation", "身份证号": "idNumber", "公寓号": "apartmentNumber", "寝室号": "dormitoryNumber", "毕业高中": "graduatedHighSchool", "学生手机号": "stuMobileNumber", "家庭地址": "homeAddress", "父亲姓名": "fatherName", "父亲工作单位": "fatherWorkUnit", "父亲联系方式": "fatherMobileNumber", "母亲姓名": "motherName", "母亲工作单位": "motherWorkUnit", "母亲联系方式": "motherMobileNumber" }
}

//函数获得学生基础信息导入后，系统返回的无法插入的数据，转成excel下载
export const dataGetBasicFailed = (data) => {
    JSONToExcelConvertor(data, "学生关怀系统--基本数据导入失败的学号", ["导入失败的学号"])
}

//获得学生成绩数据模板下载
export const dataGetModeScore = () => {

    return { "课程号": "courseID", "课序号": "courseIndex", "学号": "stuID", "初试成绩": "initialScore", "补考成绩(没有不填写)": "makeUpScore", "考试时间(格式如:2017-01-01)": "examDate", "是否重修(是或者否)": "repairOrNot" }
}

//函数获得学生成绩信息导入后，系统返回的无法插入的数据，转成excel下载
export const dataGetScoreFailed = (data) => {
    JSONToExcelConvertor(data, "学生关怀系统--成绩导入失败的课程号与课序号", ["学号","导入失败的课程号", "导入失败的课序号"])
}

//获得重点关注数据模板下载
export const dataGetModeFocus = () => {
        return { "学号": "stuID", "班号": "stuClassNumber", "姓名": "stuName", "性别": "sex", "民族": "nationality", "政治面貌": "politicalLandscape", "学历": "stuEducation", "身份证号": "idNumber", "公寓号": "apartmentNumber", "寝室号": "dormitoryNumber", "毕业高中": "graduatedHighSchool", "学生手机号": "stuMobileNumber", "家庭地址": "homeAddress", "父亲姓名": "fatherName", "父亲工作单位": "fatherWorkUnit", "父亲联系方式": "fatherMobileNumber", "母亲姓名": "motherName", "母亲工作单位": "motherWorkUnit", "母亲联系方式": "motherMobileNumber" }
    }

//函数获得煮点关注信息导入后，系统返回的无法插入的数据，转成excel下载
export const dataGetFocusFailed = (data) => {
    JSONToExcelConvertor(data, "学生关怀系统--重点关注信息导入失败的学号", ["导入失败的学号"])
}

//定义一些轻柔的颜色
export const colorList = ["#80cbc4", "#82dae6", "#81e7cf", "#88e186", "#acd680", "#99FF99", "#99CC33", "#FFCC66", "#FF9900", "#CCCC99", "#999966", "#66CC99", "#80cbc4", "#82dae6", "#81e7cf", "#88e186", "#acd680", "#99FF99", "#99CC33", "#FFCC66", "#FF9900", "#CCCC99", "#999966", "#66CC99", "#80cbc4", "#82dae6", "#81e7cf", "#88e186", "#acd680", "#99FF99", "#99CC33", "#FFCC66", "#FF9900", "#CCCC99", "#999966", "#66CC99"]
