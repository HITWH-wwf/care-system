//在该文件中定义并实现画echarts的函数

import { colorList } from '@/api/api'
import echarts from 'echarts'
//首页第一个折线图
export const drawIndexMajorLine = (lineData) => {
    /*
    lineData传递样例:
    {
    "date":["2017-01","2017-02","2017-03"],
    "全校学生":[100,200,150],
    "计算机院":[30,50,80],
    "土木学院":[30,50,80]
    }
    */
    let item
    let dateList = lineData["date"]
    let collegeName = new Array()
    let collegeSeries = new Array()
    for (item in lineData) {
        if (item != "date") {
            collegeSeries.push(
                {
                    name: item,
                    type: "line",
                    hoverAnimation: true,
                    symbolSize: 8,
                    itemStyle: {
                        emphasis: {
                            borderColor: "#fff",
                            borderWidth: 4,
                            borderType: "solid",
                            shadowBlur: 5,
                            shadowColor: "#9c9a9b",
                        }
                    },
                    lineStyle: {
                        normal: {
                            width: 1,
                        }
                    },
                    data: lineData[item]
                }
            )
            collegeName.push(item)
        }
    }

    let option = {
        title: {
            text: '学院重点关注学生增长量(按学院)',
            x: 'center',
            textStyle: {
                fontSize: 16
            }
        },
        //color: colorList,
        grid: {
            bottom: 70
        },
        legend: {
            data: collegeName,
            x: 'left',
            top:'25px'
        },
        tooltip: {
            trigger: 'axis',
            z: -1,
            axisPointer: {
                type: 'line',
                lineStyle: {
                    type: 'dashed',
                    color: '#a4a4a4',
                    opacity: 0.7
                }
            },
        },
        dataZoom: [
            {
                show: true,
                realtime: true,
                start: 0,
                end: 100,
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                handleSize: '30%',
                handleStyle: {
                    color: '#80cbc4'
                },
                fillerColor: '#d8faf4',
                borderColor: "#b1b1b1"
            }
        ],
        xAxis: [
            {
                type: 'category',
                axisTick: {
                    show: false
                },
                axisLine: {
                    lineStyle: {
                        color: '#90979c'
                    }
                },
                data: dateList.map(function (str) {
                    return str.replace(' ', '\n')
                })
            }
        ],
        yAxis: [
            {
                name: '',
                axisTick: {
                    show: false
                },
                axisLine: {
                    lineStyle: {
                        color: '#90979c'
                    }
                },
                axisLabel: {
                    formatter: '{value}人'
                },
                type: 'value'
            }
        ],
        series: collegeSeries,
    };
    return option
}

//首页显示的柱状图
export const drawIndexMajorBar = (barData) => {
    /*{
        "date":["2017-01","2017-02","2017-03"],
        "17":[100,200,150],
        "16":[30,50,80],
        "15":[30,50,80],
        "14":[30,50,80],
        "13":[30,50,80]
    }*/

    let item
    let dateList = barData["date"]
    let collegeName = new Array()
    let collegeSeries = new Array()
    for (item in barData) {
        if (item != "date") {
            collegeSeries.push(
                {
                    name: item + "级",
                    type: 'bar',
                    stack: 'test',
                    data: barData[item],
                    label: {
                        normal: {
                            show: true
                        }
                    },
                }
            )
            collegeName.push(item + "级")
        }
    }
    let option = {
        title: {
            text: '学院重点关注学生增长量(按年级)',
            x: 'center',
            textStyle: {
                fontSize: 16
            }
        },
        tooltip: {
            trigger: 'axis',
            z: -1,
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {
            data: collegeName,
            x: 'left',
            top:'25px'
        },
        dataZoom: [
            {
                show: true,
                realtime: true,
                start: 0,
                end: 100,
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                handleSize: '30%',
                handleStyle: {
                    color: '#80cbc4'
                },
                fillerColor: '#d8faf4',
                borderColor: "#b1b1b1"
            }
        ],
        grid: {
            bottom: 70,
        },

        xAxis: [{
            type: 'category',
            data: dateList
        }],
        yAxis: [{
            name: '',
            axisTick: {
                show: false
            },
            axisLine: {
                lineStyle: {
                    color: '#90979c'
                }
            },
            axisLabel: {
                formatter: '{value}人'
            },
            type: 'value'
        }],
        series: collegeSeries
    };
    return option
}

//个人页上的成绩统计饼状图
export const drawPersonalScorePie = (pieData) => {
    /*
        "scoreInfo":{
        "totalNum":30,//查询到的该生的考试数量
        "failNum":30,//其中挂科的数量
        "data":[
            {
                "courseID":"EC5444646355",//课程号
                "courseIndex":"1",//课序号
                "initialScore":"45.2", //初始成绩
                "makeUpScore":"0",//补考成绩
                "examDate":"2017-01-04 20:20:50",//考试时间
                "repairOrNot":"是"//是否重修
            },
            {
                
            }
        ]
    }
    */
    let option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data: ['及格', '不及格']
        },
        series: [
            {
                name: '成绩统计',
                type: 'pie',
                radius: ['25%', '58%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '30',
                            fontWeight: 'bold'
                        }
                    }
                },
                color: ['#86D560', '#AF89D6', '#59ADF3', '#FF999A', '#FFCC67'],
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data: [
                    { value: pieData['totalNum'] - pieData['failNum'], name: '及格' },
                    { value: pieData['failNum'], name: '不及格' },
                ]
            }
        ]
    };
    return option
}

//个人页上的进出公寓统计饼状图
export const drawPersonalTripPie = (pieData) => {
    /*
       "totalNum": 30,
    "failNum": 20,
    "normolWord":"正常时间归寝"
    "unNormolWord":"晚于23点归寝"
    "colName": [
        "通过公寓号",
        "离开时间",
        "进入时间"
    ],
    "propName": [
        "department",
        "exitTime",
        "entryTime"
    ],
    "data": [
        {
            "department": "2#",
            "exitTime": "2017-01-01 20:33:45",
            "entryTime": "2017-01-01 20:00:00"
        }
    ]
    */
    let option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data: [pieData["normolWord"], pieData["unNormolWord"]]
        },
        series: [
            {
                name: '进出公寓统计',
                type: 'pie',
                radius: ['38%', '58%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '28',
                            fontWeight: 'bold'
                        }
                    }
                },
                color: ['#FFCC67', '#FF999A'],
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data: [
                    { value: pieData['totalNum'] - pieData['failNum'], name: pieData["normolWord"] },
                    { value: pieData['failNum'], name: pieData["unNormolWord"] },
                ]
            }
        ]
    };
    return option
}

//个人页上一卡通消费记录统计的折线图
export const drawPersonalCardLine = (lineData) => {
    /*
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
    }
    */

    let option = {
        color: ["#9DCE50"],
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            icon: 'rect', //设置图例的图形形状，circle为圆，rect为矩形
            itemWidth: 14, //图例标记的图形宽度[ default: 25 ] 
            itemHeight: 5, //图例标记的图形高度。[ default: 14 ] 
            itemGap: 13, //图例每项之间的间隔。横向布局时为水平间隔，纵向布局时为纵向间隔。[ default: 10 ] 
            top: '5%',
            right: '4%', //图例组件离容器右侧的距离
            textStyle: {
                fontSize: 12,
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: lineData['date']
        },
        yAxis: [{
            type: 'value',
            axisTick: {
                show: false
            },
            axisLine: {
                lineStyle: {
                    color: '#57617B'
                }
            },
            axisLabel: {
                margin: 10,
            },
            splitLine: {
                show: false,
                lineStyle: {
                    color: '#57617B'
                }
            },
            splitArea: {
                show: false
            },
        }],
        series: [{
            type: 'line',
            smooth: true,
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ //填充的颜色。
                        offset: 0, // 0% 处的颜色
                        color: 'rgba(137, 189, 27, 0.3)'
                    }, {
                        offset: 0.8, // 80% 处的颜色
                        color: 'rgba(137, 189, 27, 0)'
                    }], false),
                    shadowColor: 'rgba(0, 0, 0, 0.1)', //阴影颜色。支持的格式同color
                    shadowBlur: 10 //图形阴影的模糊大小。该属性配合 shadowColor,shadowOffsetX, shadowOffsetY 一起设置图形的阴影效果
                }
            },
            data: lineData['consume']
        }]
    };
    return option
}