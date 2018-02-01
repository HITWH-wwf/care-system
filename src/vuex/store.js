import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// 应用初始状态
const state = {
    indexState: -1,//当前导航栏的索引值，0：首页 1：办公 2：系统管理 3：数据维护
    pagePower: {
        indexMajor: false,
        indexStudents: false,
        person: false,
        officeDataExpore: false,
        officeSuggestions: false,
        systemUserTeam: false,
        systemUsers: false,
        systemRoleTeam: false,
        dataUpdateBasic: false,
        dataUpdateScore: false,
        dataFilter: false,
    },//页面权限
    pageName: {
        indexMajor: "关注学生趋势",
        indexStudents: "学生数据(权限内)",
        person: "个人页",
        officeDataExpore: "数据导出",
        officeSuggestions: "意见反馈",
        systemUserTeam: "用户组管理",
        systemUsers: "用户管理",
        systemRoleTeam: "角色组管理",
        dataUpdateBasic: "学生基本数据增量导入",
        dataUpdateScore: "学生成绩数据增量导入",
        dataUpdateFocus:"重点关注数据增量导入",
        dataFilter: "异常数据筛选"
    },//页面对应的名称
    pageNameLower: {
        indexmajor: "关注学生趋势",
        indexstudents: "学生数据(权限内)",
        person: "个人页",
        officedataexpore: "数据导出",
        officesuggestions: "意见反馈",
        systemuserteam: "用户组管理",
        systemusers: "用户管理",
        systemroleteam: "角色组管理",
        dataupdatebasic: "学生基本数据增量导入",
        dataupdatescore: "学生成绩数据增量导入",
        dataupdatefocus:"重点关注数据增量导入",
        datafilter: "异常数据筛选"
    },//页面对应的名称，小写形式，方便后端传递数据
    pageNameLowerChange: {
        indexmajor: "indexMajor",
        indexstudents: "indexStudents",
        person: "person",
        officedataexpore: "officeDataExpore",
        officesuggestions: "officeSuggestions",
        systemuserteam: "systemUserTeam",
        systemusers: "systemUsers",
        systemroleteam: "systemRoleTeam",
        dataupdatebasic: "dataUpdateBasic",
        dataupdatescore: "dataUpdateScore",
        datafilter: "dataFilter",
        dataupdatefocus:"dataUpdateFocus"
    },//页面对应的名称，小写转大写

    userid: "",//用户名
    stuid: "",//学生学号,用于个人页处理
    state: 0
}

// 定义所需的 mutations
const mutations = {
  setIndexState: (state, paras) => {
        state.indexState = paras.index
    },
    setPagePower: (state, paras) => {
        let pageName
        //console.log(paras)
        for (pageName in paras) {
            state.pagePower[state.pageNameLowerChange[pageName]] = paras[pageName]
            //state.pagePower[pageName] = paras[pageName]
        }
    },
    setUserId: (state, paras) => {
        state.userid = paras.userid
    },
    setStuId: (state, paras) => {
        state.stuid = paras.stuid
    },
    delUserId: (state) => {
        state.userid = ""
    }
}

// 创建 store 实例
export default new Vuex.Store({
    state,
    mutations,
})
