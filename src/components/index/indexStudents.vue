<template>
  <div>
    <el-row style="margin-top:50px" :gutter="40" justify>
      <el-col :span="5" :offset="6">
        <el-input placeholder="模糊搜索" icon="search" v-model="inputDataForSearch"
                  :on-icon-click="filterByInputDataForSearch" @keyup.enter.native="filterByInputDataForSearch">
        </el-input>
      </el-col>
      <el-col :span="3">
        <div style="display: flex">
          <el-button type="primary" icon="search" @click="filterByInputDataForSearch" :loading="loadingButton">搜 索
          </el-button>
          <el-button type="primary" icon="delete2" @click="delInputDataForSearch">清空条件</el-button>
        </div>
      </el-col>
    </el-row>
    <el-row style="margin-top:30px">
      <el-col :span="22" :offset="1">
        <el-table :data="tableInfoShow['data']" style="width: 100%" highlight-current-row v-loading.body="loadingTable"
                  height="500">
          <template v-for="(item, index) in tableInfoShow['colName']">
            <el-table-column :prop="tableInfoShow['propName'][index]" :label="item" :key="item.key"
                             v-if="tableInfoShow['propName'][index]!='state'" align='center'>
            </el-table-column>
            <el-table-column :prop="tableInfoShow['propName'][index]" :label="item" :key="item.key" v-else
                             align='center'>
              <template slot-scope="scope">
                <el-tag :type="tableRowStyle(scope.row)" close-transition>{{scope.row.state}}</el-tag>
              </template>
            </el-table-column>
          </template>
          <el-table-column label="操作" align='center'>
            <template slot-scope="scope">
              <i v-run="register(scope.$index)" :class="iconClassMouseOut" @click="handleEdit(scope.$index, scope.row)"
                 @mousemove="changeIcon(0, scope.$index)" @mouseout="changeIcon(1, scope.$index)"></i>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="22" :offset="1">
        <el-pagination style="float:right" @current-change="handleCurrentChange" :current-page.sync="currentPage1"
                       :page-size="10" layout="total, prev, pager, next, jumper" :total="stuNum">
        </el-pagination>
      </el-col>
    </el-row>
  </div>
</template>

<script>

  import {getIndexTableInfo} from '@/api/api'

  export default {
    data() {
      return {
        currentPage1: 1,
        currrentPage1: 1,
        tableInfoTotal: '',
        tableInfoShow: {data: []},
        tableInfoTemp: '',
        elements: {},
        iconClassMouseMove: 'fa fa-search fa-2x txt-blue cur-icon',
        iconClassMouseOut: 'fa fa-search fa-lg txt-blue',
        inputDataForSearch: '',
        searchKey: '',
        loadingTable: false,
        loadingButton: false,
        stuNum: 0
      }
    },
    directives: {
      //将该dom注册进this中
      run(el, binding) {
        if (typeof binding.value == 'function')
          binding.value(el);
      }
    },
    methods: {
      handleCurrentChange(val) {
        this.tableInfoShow['data'] = []
        for (var i = 0; i < 10; i++) {
          this.tableInfoShow['data'].push()
        }
        var j = 0
        for (var i = (val - 1) * 10; i < (val - 1) * 10 + 10 && i < this.stuNum; i++ , j++) {
          this.$set(this.tableInfoShow['data'], j, this.tableInfoTemp['data'][i])
        }
        //console.log(this.tableInfoShow['data'])
      },
      tableRowStyle(row) {
        if (row['state'] == '推介关注') {
          return 'warning'
        } else if (row['state'] == '重点关注') {
          return 'danger'
        } else if (row['state'] == '毕业') {
          return 'success'
        }
        return ''
      },
      changeIcon(mode, index) {
        let refValue = 'icon' + index
        if (mode == 0) {
          //this.iconClass = "fa fa-search fa-2x txt-blue"
          this.elements[refValue].className = this.iconClassMouseMove
        } else {
          //this.iconClass = "fa fa-search fa-lg txt-blue"
          this.elements[refValue].className = this.iconClassMouseOut
        }
      },
      handleEdit(index, row) {
        this.$store.commit("setStuId", {stuid: row['stuID']})
        localStorage.stuID = row['stuID']
        //window.open("http://localhost:8080/#/person")
        window.open("/#/person")
      },
      register(index) {
        return (el) => {
          this.elements["icon" + index] = el;
        }
      },
      filterByInputDataForSearch() {
        //this.tableInfoShow = ''
        var index
        var indexProp
        var tableInfoShowTemp = JSON.parse(JSON.stringify(this.tableInfoTotal))
        var ifpush
        this.loadingButton = true
        tableInfoShowTemp['data'] = new Array()
        for (index in this.tableInfoTotal['data']) {
          ifpush = false
          for (indexProp in this.tableInfoTotal['propName']) {
            if (this.tableInfoTotal['data'][index][this.tableInfoTotal['propName'][indexProp]] != null && this.tableInfoTotal['data'][index][this.tableInfoTotal['propName'][indexProp]].match(this.inputDataForSearch) != null) {
              ifpush = true
              break
            }
          }
          if (ifpush == true) {
            tableInfoShowTemp['data'].push(this.tableInfoTotal['data'][index])
          }
        }
        //        this.tableInfoShow = tableInfoShowTemp
        this.currentPage1 = 1
        this.tableInfoTemp = tableInfoShowTemp
        this.tableInfoShow['data'] = []
        this.stuNum = tableInfoShowTemp['data'].length
        for (var i = 0; i < 10 && i < this.stuNum; i++) {
          this.$set(this.tableInfoShow['data'], i, tableInfoShowTemp['data'][i])
        }

        this.loadingButton = false
      },
      delInputDataForSearch() {
        this.currentPage1 = 1
        this.inputDataForSearch = ''
        this.tableInfoTemp = this.tableInfoTotal
        this.tableInfoShow['data'] = []
        this.stuNum = this.tableInfoTemp['data'].length
        for (var i = 0; i < 10 && i < this.stuNum; i++) {
          this.$set(this.tableInfoShow['data'], i, this.tableInfoTemp['data'][i])
        }
      }
    },
    mounted() {
      this.loadingButton = true
      this.loadingTable = true
      //保存所有结果
      for (var i = 0; i < 10; i++) {
        this.tableInfoShow['data'].push()
      }
      let that = this
      getIndexTableInfo(this.$store.state.userid).then((data) => {
        that.tableInfoTotal = data['data']
        that.tableInfoTemp = that.tableInfoTotal
        that.stuNum = that.tableInfoTotal['data'].length
        that.tableInfoShow['colName'] = that.tableInfoTotal['colName']
        that.tableInfoShow['propName'] = that.tableInfoTotal['propName']
        for (var i = 0; i < 10 && i < this.stuNum; i++) {
          that.tableInfoShow['data'][i] = that.tableInfoTotal['data'][i]
        }
      })
      this.loadingTable = false
      this.loadingButton = false
    },
  }
</script>

<style scoped>
  .txt-blue {
    color: #13CE66
  }

  .cur-icon {
    cursor: pointer;
  }
</style>
