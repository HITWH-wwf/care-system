<template>
  <div>
    <el-row style="margin-top:30px">
      <el-col :offset="3">
        <el-checkbox v-model="freechecked" :disabled="fixedchecked">自由查询</el-checkbox>
        <el-checkbox v-model="fixedchecked" :disabled="freechecked">固定查询</el-checkbox>
        <el-checkbox v-model="listchecked" :disabled="recordchecked">学生名单</el-checkbox>
        <el-checkbox v-model="recordchecked" :disabled="listchecked">学生具体记录</el-checkbox>
        <el-button type="primary" style="margin-left: 30px" @click="excelExpore">导出数据</el-button>
      </el-col>
      <el-col :span="18" :offset="3">
        <el-tabs type="border-card" v-if="freechecked">
          <el-tab-pane label="一卡通消费查询">
            <el-row>
              <el-col :span="18" style="margin: 10px 10px 10px 10px">
                <el-checkbox v-model="classchecked" :disabled="numchecked||namechecked">班级</el-checkbox>
                <el-checkbox v-model="numchecked" :disabled="classchecked||namechecked">学号</el-checkbox>
                <el-checkbox v-model="namechecked" :disabled="numchecked||classchecked">姓名</el-checkbox>
                <el-checkbox v-model="datechecked">时间</el-checkbox>
              </el-col>
              <el-col :span="18" style="margin: 10px 10px 10px 10px">
                <el-button type="primary" @click="dialogVisible=true" v-if="classchecked">选择班级</el-button>
                <el-dialog
                  title="提示"
                  :visible.sync="dialogVisible"
                  width="30%">
                  <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
                  <div style="margin: 15px 0;"></div>
                  <el-checkbox-group v-model="checkedclass1" @change="handleCheckedClassChange">
                    <el-checkbox v-for="c in classList" :label="c" :key="c">{{c}}</el-checkbox>
                  </el-checkbox-group>
                  <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
                  </span>
                </el-dialog>
                <span v-if="numchecked">学号：<el-input v-model="stuid" placeholder="请输入内容"
                                                          style="width: 100px"></el-input></span>
                <span v-if="namechecked">姓名：<el-input v-model="stuname" placeholder="请输入内容"
                                                           style="width: 100px"></el-input></span>
                <el-date-picker
                  style="margin: 10px 10px 10px 10px"
                  v-if="datechecked"
                  v-model="date"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  :picker-options="pickerOptions0">
                </el-date-picker>
              </el-col>
              <el-col :span="18" style="margin: 10px 10px 10px 10px">
                额度范围：<el-input v-model="range1" placeholder="请输入内容" style="width: 100px"></el-input>
                -
                <el-input v-model="range2" placeholder="请输入内容" style="width: 100px"></el-input>
                <el-checkbox v-model="singlechecked" :disabled="sumchecked">单笔</el-checkbox>
                <el-checkbox v-model="sumchecked" :disabled="singlechecked">总计</el-checkbox>
              </el-col>
              <el-col style="margin: 10px 10px 10px 10px">
                <el-button @click="sub1" type="primary">提交</el-button>
              </el-col>
            </el-row>
          </el-tab-pane>
          <el-tab-pane label="归寝统计查询">
            <el-row>
              <el-col :span="18" style="margin: 10px 10px 10px 10px">
                <el-checkbox v-model="classchecked" :disabled="numchecked||namechecked">班级</el-checkbox>
                <el-checkbox v-model="numchecked" :disabled="classchecked||namechecked">学号</el-checkbox>
                <el-checkbox v-model="namechecked" :disabled="numchecked||classchecked">姓名</el-checkbox>
                <el-checkbox v-model="datechecked">时间</el-checkbox>
              </el-col>
              <el-col :span="18" style="margin: 10px 10px 10px 10px">
                <el-button type="primary" @click="dialogVisible1=true" v-if="classchecked">选择班级</el-button>
                <el-dialog
                  title="提示"
                  :visible.sync="dialogVisible1"
                  width="30%">
                  <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
                  <div style="margin: 15px 0;"></div>
                  <el-checkbox-group v-model="checkedclass2" @change="handleCheckedClassChange">
                    <el-checkbox v-for="c in classList" :label="c" :key="c">{{c}}</el-checkbox>
                  </el-checkbox-group>
                  <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="dialogVisible1 = false">确 定</el-button>
                  </span>
                </el-dialog>
                <span v-if="numchecked">学号：<el-input v-model="stuid2" placeholder="请输入内容"
                                                          style="width: 100px"></el-input></span>
                <span v-if="namechecked">姓名：<el-input v-model="stuname2" placeholder="请输入内容"
                                                           style="width: 100px"></el-input></span>
                <el-date-picker
                  style="margin: 10px 10px 10px 10px"
                  v-if="datechecked"
                  v-model="date2"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  :picker-options="pickerOptions0">
                </el-date-picker>
              </el-col>
              <el-col :span="18" style="margin: 10px 10px 10px 10px">
                <el-checkbox v-model="wanchecked" :disabled="weichecked">晚归</el-checkbox>
                <el-checkbox v-model="weichecked" :disabled="wanchecked">未归</el-checkbox>
                <span style="margin-left: 30px">次数：</span><el-input v-model="count1" style="width: 100px;"></el-input>-
                <el-input v-model="count2" style="width: 100px;"></el-input>
              </el-col>
              <el-col style="margin: 10px 10px 10px 10px">
                <el-button @click="sub2" type="primary">提交</el-button>
              </el-col>
            </el-row>
          </el-tab-pane>
          <el-tab-pane label="不及格科目查询">
            <el-row>
              <el-col style="margin: 10px 10px 10px 10px">
                <el-checkbox v-model="examchecked" :disabled="scorechecked">成绩查询</el-checkbox>
                <el-checkbox v-model="scorechecked" :disabled="examchecked">成绩统计</el-checkbox>
              </el-col>
              <el-col :span="18" style="margin: 10px 10px 10px 10px">
                <el-checkbox v-model="classchecked" :disabled="numchecked||namechecked">班级</el-checkbox>
                <el-checkbox v-model="numchecked" :disabled="classchecked||namechecked">学号</el-checkbox>
                <el-checkbox v-model="namechecked" :disabled="numchecked||classchecked">姓名</el-checkbox>
              </el-col>
              <el-col :span="18" style="margin: 10px 10px 10px 10px">
                <el-button type="primary" @click="dialogVisible3=true" v-if="classchecked">选择班级</el-button>
                <el-dialog
                  title="提示"
                  :visible.sync="dialogVisible3"
                  width="30%">
                  <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
                  <div style="margin: 15px 0;"></div>
                  <el-checkbox-group v-model="checkedclass3" @change="handleCheckedClassChange">
                    <el-checkbox v-for="c in classList" :label="c" :key="c">{{c}}</el-checkbox>
                  </el-checkbox-group>
                  <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="dialogVisible3 = false">确 定</el-button>
                  </span>
                </el-dialog>
                <span v-if="numchecked">学号：<el-input v-model="stuid3" placeholder="请输入内容"
                                                          style="width: 100px"></el-input></span>
                <span v-if="namechecked">姓名：<el-input v-model="stuname3" placeholder="请输入内容"
                                                           style="width: 100px"></el-input></span>
              </el-col>
              <el-col style="margin: 10px 10px 10px 10px">
                <el-checkbox v-model="courseNumchecked" :disabled="courseNamechecked">课序号</el-checkbox>
                <el-checkbox v-model="courseNamechecked" :disabled="courseNumchecked">课程名称</el-checkbox>
                <el-input v-model="coursedata" v-if="courseNumchecked||courseNamechecked" style="width: 100px"></el-input>
              </el-col>
              <el-col style="margin: 10px 10px 10px 10px" v-if="scorechecked">
                <el-checkbox v-model="coursechecked" :disabled="xfchecked||coursesumchecked">不及格科目查询</el-checkbox>
                <el-checkbox v-model="xfchecked" :disabled="coursechecked||coursesumchecked">整体学分查询</el-checkbox>
                <el-checkbox v-model="coursesumchecked" :disabled="coursechecked||xfchecked">不及格科目累计学分查询</el-checkbox>
              </el-col>
              <el-col v-if="scorechecked">
                <el-input v-model="range3" style="width: 100px"></el-input>
                -
                <el-input v-model="range4" style="width: 100px"></el-input>
              </el-col>
              <el-col v-if="examchecked" style="margin: 10px 10px 10px 10px">
                <el-button type="primary" @click="sub3">提交</el-button>
              </el-col>
              <el-col v-if="scorechecked" style="margin: 10px 10px 10px 10px">
                <el-button type="primary" @click="sub4">提交</el-button>
              </el-col>
            </el-row>
          </el-tab-pane>
        </el-tabs>
        <el-tabs type="border-card" v-if="fixedchecked">
          <el-tab-pane label="一卡通消费查询">
            <el-col style="margin: 10px 10px 10px 10px">
              累计消费额度小于1元，连续1天:<el-button type="primary" @click="sub5(1)">查询</el-button>
            </el-col>
            <el-col style="margin: 10px 10px 10px 10px">
              一次性消费超过50元，且一卡通额度小于3元:<el-button type="primary" @click="sub5(2)">查询</el-button>
            </el-col>
          </el-tab-pane>
          <el-tab-pane label="归寝统计查询">
            <el-col style="margin: 10px 10px 10px 10px">
              于23：30前无刷卡归宿舍记录:<el-button type="primary" @click="sub6(1)">查询</el-button>
            </el-col>
            <el-col style="margin: 10px 10px 10px 10px">
              24小时内无任何出入记录:<el-button type="primary" @click="sub6(2)">查询</el-button>
            </el-col>
            <el-col style="margin: 10px 10px 10px 10px">
              23:30-5：00归寝室记录:<el-button type="primary" @click="sub6(3)">查询</el-button>
            </el-col>
          </el-tab-pane>
          <el-tab-pane label="不及格科目查询">
            <el-col style="margin: 10px 10px 10px 10px">
              不及格科目超过3科:<el-button type="primary" @click="sub7(1)">查询</el-button>
            </el-col>
            <el-col style="margin: 10px 10px 10px 10px">
              不及格科目累计大于等于16学分小于等于20学分:<el-button type="primary" @click="sub7(2)">查询</el-button>
            </el-col>
            <el-col style="margin: 10px 10px 10px 10px">
              不及格科目累计大于20学分:<el-button type="primary" @click="sub7(3)">查询</el-button>
            </el-col>
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
    <el-row style="margin-top:30px">
      <el-col :span="22" :offset="1">
        <el-table :data="tableInfoShow['tableData']" style="width: 100%" highlight-current-row height="500" v-loading="load">
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
              <i class="hoverPoint" v-run="register(scope.$index)" :class="iconClassMouseOut"
                 @click="handleEdit(scope.$index, scope.row)" @mousemove="changeIcon(0, scope.$index)"
                 @mouseout="changeIcon(1, scope.$index)"></i>
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
  import {officeDataFilter,GetManagerClass, GetStuByCostFree, GetStuBySleepFree, GetExamResult, GetStuByScoreFree, GetStuByCostFixed, GetStuBySleepFixed, GetStuByScoreFixed} from '@/api/api'
  const _XLSX = require('xlsx');
  const X = typeof XLSX !== 'undefined' ? XLSX : _XLSX;
  export default {
    data() {
      return {
        rules: {
          range1: [
            { required: true, message: '请输入', trigger: 'blur' },
          ],
        },
        isIndeterminate: false,
        checkAll: false,
        checkedclass1: [],
        checkedclass2: [],
        checkedclass3: [],
        classList: [],
        wanchecked: false,
        weichecked: false,
        coursechecked: false,
        xfchecked: false,
        coursesumchecked: false,
        examchecked: false,
        scorechecked: false,
        courseNumchecked: false,
        courseNamechecked: false,
        count1: '',
        count2: '',
        dialogVisible: false,
        dialogVisible1: false,
        dialogVisible2: false,
        dialogVisible3: false,
        coursedata: '',
        stuid: '',
        stuid2: '',
        stuid3: '',
        stuname: '',
        stuname2: '',
        stuname3: '',
        range1: '',
        range2: '',
        range3: '',
        range4: '',
        listchecked: false,
        recordchecked: false,
        freechecked: false,
        fixedchecked: false,
        singlechecked: false,
        sumchecked: false,
        numchecked: false,
        namechecked: false,
        classchecked: false,
        datechecked: false,
        pickerOptions0: {
          disabledDate(time) {
            let curDate = (new Date()).getTime()
            let three = 93 * 24 * 3600 * 1000
            let threeMonths = curDate - three
            return time.getTime() > Date.now() || time.getTime() < threeMonths
          }
        },
        date: '',
        date2: '',
        date3: '',
        load: false,
        currentPage1: 1,
        stuNum: 0,
        tableInfo: [],
        tableInfoShow: {tableData: []},
        checkList: [],
        options: {},
        selectData: {
          card: {
            consume: '',
            number: ''
          },
          days: '',
          sbjNumber: '',
        },
        elements: {},
        iconClassMouseMove: 'fa fa-search fa-2x txt-blue cur-icon',
        iconClassMouseOut: 'fa fa-search fa-lg txt-blue',
      };
    },
    mounted() {
      console.log(this.$store.state.userid)
      GetManagerClass(this.$store.state.userid, localStorage.sessionid).then((res) => {
        if(res.status == 1)
        {
          this.classList = this.checkedclass1 = this.checkedclass2 = this.checkedclass3 = res.classList
        }
      })
    },
    watch: {
      sumchecked: function () {
        if (this.sumchecked == false)
          console.log('aaaaaaaaaaaa')
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
      handleCheckAllChange(val) {
        this.checkedclass1 = val ? this.classList : [];
        this.checkedclass2 = val ? this.classList : [];
        this.checkedclass3 = val ? this.classList : [];
        this.isIndeterminate = false;
      },
      handleCheckedClassChange(value) {
        let checkedCount = value.length;
        this.checkAll = checkedCount === this.classList.length;
        this.isIndeterminate = checkedCount > 0 && checkedCount < this.classList.length;
      },
      handleCurrentChange: function (val) {
        this.tableInfoShow['tableData'] = []
        for (var i = 0; i < 10; i++) {
          this.tableInfoShow['tableData'].push()
        }
        var j = 0
        for (var i = (val - 1) * 10; i < (val - 1) * 10 + 10 && i < this.stuNum; i++ , j++) {
          this.$set(this.tableInfoShow['tableData'], j, this.tableInfo['tableData'][i])
        }
      },
      changeOptions: function () {
        this.options = {};
        for (let item in this.checkList) {
          this.options[this.checkList[item]] = true;
          this.selectData = {
            card: {
              consume: '',
              number: ''
            },
            days: '',
            sbjNumber: ''
          }
        }
      },
      register: function (index) {
        return (el) => {
          this.elements["icon" + index] = el;
        }
      },
      handleEdit: function (index, row) {
        this.$store.commit("setStuId", {stuid: row['stuID']})
        localStorage.stuID = row['stuID']
        window.open("/#/person")
        //setStuId
      },
      tableRowStyle: function (row) {
        if (row['state'] == '推介关注') {
          return 'warning'
        } else if (row['state'] == '重点关注') {
          return 'danger'
        } else if (row['state'] == '毕业') {
          return 'success'
        }
        return ''
      },
      changeIcon: function (mode, index) {
        let refValue = 'icon' + index
        if (mode == 0) {
          //this.iconClass = "fa fa-search fa-2x txt-blue"
          this.elements[refValue].className = this.iconClassMouseMove
        } else {
          //this.iconClass = "fa fa-search fa-lg txt-blue"
          this.elements[refValue].className = this.iconClassMouseOut
        }
      },
      sub: function () {
        let data = this.selectData
        data["userId"] = this.$store.state.userid
        if ((data.card.consume != '' && data.card.number == '') || (data.card.consume == '' && data.card.number != '')) {
          this.$alert('查询信息不完整', '提示', {
            confirmButtonText: '确定'
          });
          return;
        }
        this.load = true
        officeDataFilter(data).then((res) => {
          if (res.status == 1) {
            for (var i = 0; i < 10; i++) {
              this.tableInfoShow['data'].push()
            }
            this.tableInfo = res.data
            this.stuNum = res.data.data.length
            this.tableInfoShow['colName'] = this.tableInfo['colName']
            this.tableInfoShow['propName'] = this.tableInfo['propName']
            for (let i = 0; i < 10 && i < this.stuNum; i++) {
              this.tableInfoShow['data'][i] = this.tableInfo['data'][i]
            }
            this.load = false
          }
          else {
            //console.log("error");
          }
        })
      },
      sub1: function () {
        if(this.range1 === '' || this.range2 === '')
        {
          this.$message.error('请输入额度范围')
          return
        }
        let returnKind = this.listchecked ? 'stuList' : 'stuRecord'
        let stuRange
        if (this.namechecked)
          stuRange = {'rangeKind':'useStuName','rangeData':this.stuname}
        else if (this.numchecked)
          stuRange = {'rangeKind':'useStuId', 'rangeData': this.stuid}
        else
          stuRange = {'rangeKind':'useClassId', 'rangeData': this.checkedclass1}
        let startDate
        let endDate
        let dateRange
        if(this.date!='' && this.datechecked == true) {
          startDate = String(this.date[0].getYear() + 1900) + '-' + String(this.date[0].getMonth() + 1) + '-' + this.date[0].getDate()
          endDate = String(this.date[1].getYear() + 1900) + '-' + String(this.date[1].getMonth() + 1) + '-' + this.date[1].getDate()
          dateRange = {'startDate': startDate, 'endDate': endDate}
        }
        else
          dateRange = 'threeMonth'
        let moneyRange = {'minMoney':Number(this.range1),'maxMoney':Number(this.range2)}
        let countKind
        if(this.singlechecked)
          countKind = 'single'
        else
          countKind = 'total'
        this.load = true
        GetStuByCostFree(this.$store.state.userid, returnKind, stuRange, dateRange, moneyRange, countKind).then((res)=> {
          console.log(res)
          if(res.status === 1) {
            this.tableInfoShow.tableData = []
            for (var i = 0; i < 10; i++) {
              this.tableInfoShow['tableData'].push()
            }
            this.tableInfo = res
            this.stuNum = res.tableData.length
            this.tableInfoShow['colName'] = this.tableInfo['colName']
            this.tableInfoShow['propName'] = this.tableInfo['propName']
            for (let i = 0; i < 10 && i < this.stuNum; i++) {
              this.tableInfoShow['tableData'][i] = this.tableInfo['tableData'][i]
            }
            this.currentPage1 = 1
          }
          else if(res.status === 0)
          {
            this.$notify({
              title: '操作失败',
              message: res['errorInfo'],
              type: 'warning'
            })
          }
          this.load = false
        })

      },
      sub2: function () {
        if(this.count1 === '' || this.count2 === '')
        {
          this.$message.error('请输入次数')
          return
        }
        let returnKind = this.listchecked ? 'stuList' : 'stuRecord'
        let stuRange
        if (this.namechecked)
          stuRange = {'rangeKind':'useStuName','rangeData':this.stuname2}
        else if (this.numchecked)
          stuRange = {'rangeKind':'useStuId', 'rangeData': this.stuid2}
        else
          stuRange = {'rangeKind':'useClassId', 'rangeData': this.checkedclass2}
        let startDate
        let endDate
        let dateRange
        if(this.date2!='' && this.datechecked == true) {
          startDate = String(this.date2[0].getYear() + 1900) + '-' + String(this.date2[0].getMonth() + 1) + '-' + this.date2[0].getDate()
          endDate = String(this.date2[1].getYear() + 1900) + '-' + String(this.date2[1].getMonth() + 1) + '-' + this.date2[1].getDate()
          dateRange = {'startDate': startDate, 'endDate': endDate}
        }
        else
          dateRange = 'threeMonth'
        let countKind = this.wanchecked ? 'laterReturn' : 'noReturn'
        let appearTimes
        if(this.count1===''&&this.count2==='')
          appearTimes = 1
        else
          appearTimes = {'minTimes':Number(this.count1),'maxTimes':Number(this.count2)}
        this.load = true
        GetStuBySleepFree(this.$store.state.userid, returnKind, stuRange, dateRange, countKind, appearTimes).then((res)=>{
          console.log(res)
          if(res.status === 1) {
            this.tableInfoShow.tableData = []
            for (var i = 0; i < 10; i++) {
              this.tableInfoShow['tableData'].push()
            }
            this.tableInfo = res
            this.stuNum = res.tableData.length
            this.tableInfoShow['colName'] = this.tableInfo['colName']
            this.tableInfoShow['propName'] = this.tableInfo['propName']
            for (let i = 0; i < 10 && i < this.stuNum; i++) {
              this.tableInfoShow['tableData'][i] = this.tableInfo['tableData'][i]
            }
            this.currentPage1 = 1
          }
          else if (res.status === 0)
          {
            this.$notify({
              title: '操作失败',
              message: res['errorInfo'],
              type: 'warning'
            })
          }
          this.load = false
        })
      },
      sub3: function () {
        if(this.range3 === '' || this.range4 === '')
        {
          this.$message.error('请输入科目数或学分')
          return
        }
        let returnKind = this.listchecked ? 'stuList' : 'stuRecord'
        let stuRange
        if (this.namechecked)
          stuRange = {'rangeKind':'useStuName','rangeData':this.stuname3}
        else if (this.numchecked)
          stuRange = {'rangeKind':'useStuId', 'rangeData': this.stuid3}
        else
          stuRange = {'rangeKind':'useClassId', 'rangeData': this.checkedclass3}
        let courseRange
        if(this.courseNamechecked)
          courseRange = {'rangeKind':'courseName','rangeData':this.coursedata}
        else if(this.courseNumchecked)
          courseRange = {'rangeKind':'courseNum','rangeData':this.coursedata}
        else
          courseRange = 'all'
        this.load = true
        GetExamResult(this.$store.state.userid, returnKind, stuRange, courseRange).then((res)=>{
          console.log(res)
          if(res.status === 1) {
            this.tableInfoShow.tableData = []
            for (var i = 0; i < 10; i++) {
              this.tableInfoShow['tableData'].push()
            }
            this.tableInfo = res
            this.stuNum = res.tableData.length
            this.tableInfoShow['colName'] = this.tableInfo['colName']
            this.tableInfoShow['propName'] = this.tableInfo['propName']
            for (let i = 0; i < 10 && i < this.stuNum; i++) {
              this.tableInfoShow['tableData'][i] = this.tableInfo['tableData'][i]
            }
            this.currentPage1 = 1
          }
          else if(res.status === 0)
          {
            this.$notify({
              title: '操作失败',
              message: res['errorInfo'],
              type: 'warning'
            })
          }
          this.load = false
        })
      },
      sub4: function () {
        let returnKind = this.listchecked ? 'stuList' : 'stuRecord'
        let stuRange
        if (this.namechecked)
          stuRange = {'rangeKind':'useStuName','rangeData':this.stuname3}
        else if (this.numchecked)
          stuRange = {'rangeKind':'useStuId', 'rangeData': this.stuid3}
        else
          stuRange = {'rangeKind':'useClassId', 'rangeData': this.checkedclass3}
        let courseRange
        if(this.courseNamechecked)
          courseRange = {'rangeKind':'courseName','rangeData':this.coursedata}
        else if(this.courseNumchecked)
          courseRange = {'rangeKind':'courseNum','rangeData':this.coursedata}
        else
          courseRange = 'all'
        let countKind
        if(this.coursechecked)
          countKind = 'failCourse'
        else if(this.xfchecked)
          countKind = 'totalCredit'
        else
          countKind = 'failCredit'
        let countRange = {'min':Number(this.range3),'max':Number(this.range4)}
        if(courseRange != 'all') {
          countKind = 'failCourse'
          countRange = {'min': 1,'max': 1}
        }
        this.load = true
        GetStuByScoreFree(this.$store.state.userid, returnKind, stuRange, courseRange, countKind, countRange).then((res)=>{
          console.log(res)
          if(res.status === 1) {
            this.tableInfoShow.tableData = []
            for (var i = 0; i < 10; i++) {
              this.tableInfoShow['tableData'].push()
            }
            this.tableInfo = res
            this.stuNum = res.tableData.length
            this.tableInfoShow['colName'] = this.tableInfo['colName']
            this.tableInfoShow['propName'] = this.tableInfo['propName']
            for (let i = 0; i < 10 && i < this.stuNum; i++) {
              this.tableInfoShow['tableData'][i] = this.tableInfo['tableData'][i]
            }
            this.currentPage1 = 1
          }
          else if(res.status === 0)
          {
            this.$notify({
              title: '操作失败',
              message: res['errorInfo'],
              type: 'warning'
            })
          }
          this.load = false
        })
      },
      sub5: function (val) {
        let returnKind = this.listchecked ? 'stuList' : 'stuRecord'
        let queryKind
        if(val === 1)
          queryKind = 'fixed1'
        if(val ===2)
          queryKind = 'fixed2'
        this.load = true
        GetStuByCostFixed(this.$store.state.userid, returnKind, localStorage.sessionid, queryKind).then((res)=>{
          console.log(res)
          if(res.status === 1) {
            this.tableInfoShow.tableData = []
            for (var i = 0; i < 10; i++) {
              this.tableInfoShow['tableData'].push()
            }
            this.tableInfo = res
            this.stuNum = res.tableData.length
            this.tableInfoShow['colName'] = this.tableInfo['colName']
            this.tableInfoShow['propName'] = this.tableInfo['propName']
            for (let i = 0; i < 10 && i < this.stuNum; i++) {
              this.tableInfoShow['tableData'][i] = this.tableInfo['tableData'][i]
            }
            this.currentPage1 = 1
          }
          else if (res.status === 0)
          {
            this.$notify({
              title: '操作失败',
              message: res['errorInfo'],
              type: 'warning'
            })
          }
          this.load = false
        })
      },
      sub6: function (val) {
        let returnKind = this.listchecked ? 'stuList' : 'stuRecord'
        let queryKind
        if(val=== 1)
          queryKind = 'fixed1'
        if(val === 2)
          queryKind = 'fixed2'
        if(val === 3)
          queryKind = 'fixed3'
        this.load = true
        GetStuBySleepFixed(this.$store.state.userid, returnKind, localStorage.sessionid, queryKind).then((res)=>{
          console.log(res)
          if(res.status === 1) {
            this.tableInfoShow.tableData = []
            for (var i = 0; i < 10; i++) {
              this.tableInfoShow['tableData'].push()
            }
            this.tableInfo = res
            this.stuNum = res.tableData.length
            this.tableInfoShow['colName'] = this.tableInfo['colName']
            this.tableInfoShow['propName'] = this.tableInfo['propName']
            for (let i = 0; i < 10 && i < this.stuNum; i++) {
              this.tableInfoShow['tableData'][i] = this.tableInfo['tableData'][i]
            }
            this.currentPage1 = 1
          }
          else if (res.status === 0)
          {
            this.$notify({
              title: '操作失败',
              message: res['errorInfo'],
              type: 'warning'
            })
          }
          this.load = false
        })
      },
      sub7:function (val) {
        let returnKind = this.listchecked ? 'stuList' : 'stuRecord'
        let queryKind
        if(val=== 1)
          queryKind = 'fixed1'
        if(val === 2)
          queryKind = 'fixed2'
        if(val === 3)
          queryKind = 'fixed3'
        this.load = true
        GetStuByScoreFixed(this.$store.state.userid, returnKind, localStorage.sessionid, queryKind).then((res)=>{
          console.log(res)
          if(res.status === 1) {
            this.tableInfoShow.tableData = []
            for (var i = 0; i < 10; i++) {
              this.tableInfoShow['tableData'].push()
            }
            this.tableInfo = res
            this.stuNum = res.tableData.length
            this.tableInfoShow['colName'] = this.tableInfo['colName']
            this.tableInfoShow['propName'] = this.tableInfo['propName']
            for (let i = 0; i < 10 && i < this.stuNum; i++) {
              this.tableInfoShow['tableData'][i] = this.tableInfo['tableData'][i]
            }
            this.currentPage1 = 1
          }
          else if(res.status ===0)
          {
            this.$notify({
              title: '操作失败',
              message: res['errorInfo'],
              type: 'warning'
            })
          }
          this.load = false
        })
      },
      s2ab(s) {
        const buf = new ArrayBuffer(s.length);
        const view = new Uint8Array(buf);
        for (let i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
        return buf;
      },
      excelExpore: function () {
        this.$prompt('请输入文件名', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputValue: 'report',
          inputValidator: this.judgeMessageIfEmpty
        }).then(({value}) => {
          let b = [[]]
          console.log(this.tableInfo.colName)
          for(let a in this.tableInfo.colName)
            b[0].push(this.tableInfo.colName[a])
          let l
          for (let i = 0; i < this.tableInfo.tableData.length; i++) {
            l = []
            for(var a in this.tableInfo.propName) {
              l.push(this.tableInfo.tableData[i][this.tableInfo.propName[a]])
            }
            b.push(l)
          }
          console.log(b)
          const ws = X.utils.aoa_to_sheet(b)
          const wb = X.utils.book_new()
          X.utils.book_append_sheet(wb, ws, "SheetJS")
          const wbout = X.write(wb, {type: "binary", bookType: "xlsx"})
          saveAs(new Blob([this.s2ab(wbout)], {type: "application/octet-stream"}), value + ".xlsx")
          this.$message({
            type: 'success',
            message: '已成功导出'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
        });
      },
      judgeMessageIfEmpty(value) {
        if (value.length == 0) {
          return "文件名不能为空"
        }
        return true
      },
      test: function () {
        let myDate=new Date()
        console.log(String(myDate.getYear() + 1900) + '-' + String(myDate.getMonth() + 1) + '-' + myDate.getDate())
      }
    }
  }
</script>

<style scoped>
  h1 {
    font-weight: 400;
    font-size: 22px;
  }

  .condition {
    width: 100%;
    border: 1px solid #e5e5e5;
    border-radius: 4px;
    min-height: 100px;
    overflow: hidden;
  }

  .uncheck {
    width: 100%;
    height: 100%;
    padding-top: 40px;
    text-align: center;
    color: grey;
    font-size: 16px;
  }

  .opt {
    box-sizing: border-box;
    padding-top: 10px;
    width: 100%;
    height: 50px;
    font-size: 16px;
    padding-left: 20px;
    line-height: 40px;
    border-bottom: 1px dashed #e5e5e5;
  }

  .opt-left {
    width: 30%;
    height: 100%;
    float: left;
  }

  .opt-right {
    width: 60%;
    height: 100%;
    float: left;
  }

  .btn {
    float: right;
    font-size: 16px;
    margin: 5px 40px 5px auto;
  }

  .hoverPoint {
    cursor: pointer;
  }
</style>
