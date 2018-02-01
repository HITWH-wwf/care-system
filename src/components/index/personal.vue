<template>
  <div>
    <el-row style="margin-top:30px">
      <el-col :span='20' :offset='2'>
        <el-card class="box-card">
          <el-row slot="header">
            <el-col :span='4' :offset='2' class="txt-big">
              <span>
                姓名：{{stuBicData['data']['stuName']}}
              </span>
            </el-col>
            <el-col :span='4' class="txt-big">
              <span>
                关注级别：{{stuFocusInfo['focusLevel']}}
              </span>
            </el-col>
            <el-col :span='4'>
              <div style="display: flex;margin-left:10px">
                <el-tooltip effect="light" content="新建事件" :enterable="false" :open-delay="300" placement="top">
                  <i :class="addNewEventClass" @click="eventDialogFormVisible = true"
                     @mousemove="changeIcon(0 , 'addNewEventClass')" @mouseout="changeIcon(1, 'addNewEventClass')"
                     style="padding-top: 6px;"></i>
                </el-tooltip>
                <div style="margin-left:30px"></div>
                <el-tooltip effect="light" content="取消关注" :enterable="false" :open-delay="300" placement="top">
                  <i :class="cancelFocusClass" @click="cancelFocusDialogVisible = true"
                     @mousemove="changeIcon(0, 'cancelFocusClass')" @mouseout="changeIcon(1, 'cancelFocusClass')"
                     style="padding-top: 6px;"></i>
                </el-tooltip>
                <div style="margin-left:30px"></div>
                <el-tooltip effect="light"
                            v-if="!((this.stuFocusInfo['focusLevel']!='正常')&&(this.stuFocusInfo['focusLevel']!='毕业'))"
                            content="添加关注" :enterable="false" :open-delay="300" placement="top">
                  <i :class="addFocusClass" @click="addFocusDialogVisible = true"
                     @mousemove="changeIcon(0, 'addFocusClass')" @mouseout="changeIcon(1, 'addFocusClass')"
                     style="padding-top: 6px;"></i>
                </el-tooltip>
              </div>
            </el-col>
          </el-row>

          <el-dialog title="提示" :visible.sync="cancelFocusDialogVisible" size="tiny">
            <span>您即将取消对{{stuBicData['data']['stuName']}}的关注，取消后其状态将改为正常</span>
            <span slot="footer" class="dialog-footer">
              <el-row>
                <el-col :span="18" :offset="3">
                  <div style="display: flex;float:right">
                    <el-button @click="ifCancelFocus(0)">取 消</el-button>
                    <el-button type="primary" @click="ifCancelFocus(1)">确 定</el-button>
                  </div>
                </el-col>
              </el-row>
            </span>
          </el-dialog>

          <el-dialog title="新建事件" :visible.sync="eventDialogFormVisible" size='tiny'
                     @open="resetForm(eventFormContent)">
            <!-- <el-row class="tiny-line"></el-row> -->
            <el-row>
              <el-col :span="18" :offset="3">
                <el-form :model="eventFormContent" :ref="eventFormContent" label-position="right" :rules="rules">
                  <el-form-item label="事件主题:" :label-width="formLabelWidth" prop="theme">
                    <el-input v-model="eventFormContent.theme"></el-input>
                  </el-form-item>
                  <el-form-item label="事件时间:" :label-width="formLabelWidth" prop="time">
                    <el-date-picker v-model="eventFormContent.time" type="datetime" placeholder="请选择时间"
                                    style="width: 100%;">
                    </el-date-picker>
                  </el-form-item>
                  <el-form-item label="事件内容:" :label-width="formLabelWidth" prop="content">
                    <el-input v-model="eventFormContent.content" :autosize="{ minRows: 5, maxRows: 10}"
                              type="textarea"></el-input>
                  </el-form-item>
                </el-form>
              </el-col>
            </el-row>
            <div slot="footer" class="dialog-footer">
              <el-row>
                <el-col :span="18" :offset="3">
                  <div style="display: flex;float:right">
                    <el-button @click="ifAddEvent(0)">取 消</el-button>
                    <el-button type="primary" @click="ifAddEvent(1)">确 定</el-button>
                  </div>
                </el-col>
              </el-row>
            </div>
          </el-dialog>

          <el-dialog title="新建关注" :visible.sync="addFocusDialogVisible" size='tiny' @open="delFocusFormContent">
            <el-row>
              <el-col :span="18" :offset="3">
                <el-form :model="addFocusFormContent" :ref="addFocusFormContent" label-position="right">
                  <el-form-item label="姓名:" :label-width="formLabelWidth">
                    <span>{{stuBicData['data']['stuName']}}</span>
                  </el-form-item>
                  <el-form-item label="学号:" :label-width="formLabelWidth">
                    <span>{{stuBicData['data']['stuID']}}</span>
                  </el-form-item>
                  <el-form-item label="关注级别:" :label-width="formLabelWidth" prop="focusLevel">
                    <el-radio class="radio" v-model="addFocusFormContent.focusLevel" label="1">推介关注</el-radio>
                    <el-radio class="radio" v-model="addFocusFormContent.focusLevel" label="2">重点关注</el-radio>
                  </el-form-item>
                  <el-form-item label="是否校内住宿:" :label-width="formLabelWidth" prop="sleepInOrOut">
                    <el-radio class="radio" v-model="addFocusFormContent.sleepInOrOut" label="1">是</el-radio>
                    <el-radio class="radio" v-model="addFocusFormContent.sleepInOrOut" label="0">否</el-radio>
                  </el-form-item>
                  <el-form-item label="是否家长陪读:" :label-width="formLabelWidth" prop="studyWithParent">
                    <el-radio class="radio" v-model="addFocusFormContent.studyWithParent" label="0">否</el-radio>
                    <el-radio class="radio" v-model="addFocusFormContent.studyWithParent" label="1">是</el-radio>
                  </el-form-item>
                  <el-form-item label="关注原因:" :label-width="formLabelWidth" prop="focusReason"
                                :rules="[{ required: true, message: '原因不能为空' }, { min: 8, message: '长度至少 8 个字符', trigger: 'blur' }]">
                    <el-input v-model="addFocusFormContent.focusReason" :autosize="{ minRows: 5, maxRows: 10}"
                              type="textarea"></el-input>
                  </el-form-item>
                </el-form>
              </el-col>
            </el-row>
            <div slot="footer" class="dialog-footer">
              <el-row>
                <el-col :span="18" :offset="3">
                  <div style="display: flex;float:right">
                    <el-button @click="ifAddFocus(0)">取 消</el-button>
                    <el-button type="primary" @click="ifAddFocus(1)">确 定</el-button>
                  </div>
                </el-col>
              </el-row>
            </div>
          </el-dialog>

          <el-row style="margin-top:30px">
            <el-col>
              <el-form label-width="100px" :inline="true">
                <el-form-item v-for="(domain, index) in stuBicData.propName" :label="stuBicData['colName'][index] + ':'"
                              :key="index" v-if="stuBicData['colName'][index]!='姓名'">
                  <el-input v-model="stuBicData.data[stuBicData['propName'][index]]" readonly></el-input>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>
          <el-row v-if="((this.stuFocusInfo['focusLevel']!='正常')&&(this.stuFocusInfo['focusLevel']!='毕业'))"
                  style="margin-top:30px">
            <el-col :span="24" class="tiny-line"></el-col>
            <el-col :span='23' :offset='1' style="margin-top:30px">
              <el-form label-width="80px" label-position="top">
                <el-form-item :label="stuFocusInfo['focusLevel'] + '--原因:'">
                  <span>{{stuFocusInfo['focusReason']}}</span>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    <el-row style="margin-top:30px">
      <el-col :span="22" :offset="1">
        <h4>成绩统计</h4>
        <div class="tiny-line"></div>
        <el-row :gutter="40" justify style="position: relative; left: 20%; top: 20px">
          <el-col :span="5" :offset="6">
            <el-input placeholder="模糊搜索" icon="search" v-model="inputDataForSearch1"
                      :on-icon-click="filterByInputDataForSearch1" @keyup.enter.native="filterByInputDataForSearch1">
            </el-input>
          </el-col>
          <el-col :span="3">
            <div style="display: flex">
              <el-button type="primary" icon="search" @click="filterByInputDataForSearch1" :loading="loadingButton1">搜 索
              </el-button>
              <el-button type="primary" icon="delete2" @click="delInputDataForSearch1">清空条件</el-button>
            </div>
          </el-col>
        </el-row>
        <el-col :span="8" :offset="1">
          <div id="personalScorePie" style="width:100%;min-height:500px;height:50%;"></div>
        </el-col>
        <el-col :span="13" style="margin-top:30px">
          <el-table :data="stuScoreShow['data']" style="width: 100%" highlight-current-row height="400">
            <template v-for="(item, index) in stuScore['colName']">
              <el-table-column :prop="stuScore['propName'][index]" :label="item" :key="item.key" align='center'>
              </el-table-column>
            </template>
          </el-table>
        </el-col>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="22" :offset="1">
        <el-pagination style="float:right" @current-change="handleCurrentChange" :current-page.sync="currentPage1"
                       :page-size="10" layout="total, prev, pager, next, jumper" :total="stuScoreNum">
        </el-pagination>
      </el-col>
    </el-row>
    <el-row style="margin-top:30px">
      <el-col :span="22" :offset="1">
        <h4>进出公寓统计</h4>
        <div class="tiny-line"></div>
      </el-col>
      <el-row style="position: relative; left: 55%; top: 20px">
        <el-col>
          <el-date-picker v-model="value1" type="daterange" @change="change1" placeholder="选择日期范围">
          </el-date-picker>
        </el-col>
      </el-row>
      <el-col :span="8" :offset="1">
        <div id="personalTripPie" style="width:100%;min-height:500px;height:50%;"></div>
      </el-col>
      <el-col :span="13" style="margin-top:30px">
        <el-table :data="stuTripShow['data']" style="width: 100%" highlight-current-row height="400">
          <template v-for="(item, index) in stuTrip['colName']">
            <el-table-column :prop="stuTrip['propName'][index]" :label="item" :key="item.key" align='center'>
            </el-table-column>
          </template>
        </el-table>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="22" :offset="1">
        <el-pagination style="position: relative;left: 60%" @current-change="handleCurrentChange3"
                       :current-page.sync="currentPage3" :page-size="10" layout="total, prev, pager, next, jumper"
                       :total="stuTripNum">
        </el-pagination>
      </el-col>
    </el-row>
    <el-row style="margin-top:30px">
      <el-col :span="22" :offset="1">
        <h4>一卡通消费统计</h4>
        <div class="tiny-line"></div>
      </el-col>
      <el-row style="position: relative; left: 70%; top: 20px">
        <el-col>
          <el-date-picker v-model="value2" type="daterange" @change="change2" placeholder="选择日期范围">
          </el-date-picker>
        </el-col>
      </el-row>
      <el-col :span="14" :offset="1">
        <div id="personalCardLine" style="width:100%;min-height:500px;height:50%;"></div>
      </el-col>
      <el-col :span="7" style="margin-top:30px">
        <el-table :data="stuCardShow['data']" style="width: 100%" highlight-current-row height="450">
          <template v-for="(item, index) in stuCard['colName']">
            <el-table-column :prop="stuCard['propName'][index]" :label="item" :key="item.key" align='center'>
            </el-table-column>
          </template>
        </el-table>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="22" :offset="1">
        <el-pagination style="position: relative;left: 60%" @current-change="handleCurrentChange2"
                       :current-page.sync="currentPage2" :page-size="10" layout="total, prev, pager, next, jumper"
                       :total="stuCardNum">
        </el-pagination>
      </el-col>
    </el-row>
    <el-row style="margin-top:30px">
      <el-col :span="22" :offset="1">
        <h4>事件记录</h4>
        <div class="tiny-line"></div>
      </el-col>
      <el-col :span="22" :offset="1" style="margin-top:30px">
        <el-table :data="stuEvent['data']" style="width: 100%" highlight-current-row height="400">
          <template v-for="(item, index) in stuEvent['colName']">
            <el-table-column :prop="stuEvent['propName'][index]" :label="item" :key="item.key" align='center'>
            </el-table-column>
          </template>
        </el-table>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import {
    getPersonBasicInfo,
    getPersonScoreInfo,
    postPersonCancelFocus,
    postPersonAddFocus,
    getPersonTripInfo,
    getPersonCardInfo,
    getPersonEventInfo,
    postPersonAddEvent
  } from '@/api/api'
  import {drawPersonalScorePie, drawPersonalTripPie, drawPersonalCardLine} from '@/api/echarts'

  export default {
    data() {
      return {
        myChartCardLine: '',
        myChartTripPie: '',
        myChartScorePie: '',
        currentPage3: 1,
        currentPage2: 1,
        currentPage1: 1,
        value1: '',
        value2: '',
        loadingButton1: false,
        inputDataForSearch1: '',
        stuBicTotalData: '',
        stuBicData: {
          data: {
            stuName: ''
          }
        },
        stuFocusInfo: '',
        stuEvent: '',
        stuScore: '',
        stuScoreShow: {data: []},
        stuScoreTemp: '',
        stuScoreNum: 0,
        stuTrip: '',
        stuTripShow: {data: []},
        stuTripTemp: {data: []},
        stuTripNum: 0,
        stuCard: '',
        stuCardShow: {data: []},
        stuCardTemp: {data: []},
        stuCardNum: 0,
        loadingTable: true,
        addNewEventClass: 'fa fa-address-book-o fa-lg txt-green cur-icon',
        cancelFocusClass: 'fa fa-eye-slash fa-lg txt-green cur-icon',
        addFocusClass: 'fa fa-eye fa-lg txt-green cur-icon',
        eventDialogFormVisible: false,
        cancelFocusDialogVisible: false,
        addFocusDialogVisible: false,
        eventFormContent: {
          theme: '',
          time: '',
          content: ''
        },
        addFocusFormContent: {
          focusLevel: '1',
          focusReason: '',
          sleepInOrOut: '0',//是否校外住宿
          studyWithParent: '0'//是否家长陪读
        },
        formLabelWidth: '120',
        rules: {
          theme: [{required: true, message: '主题不能为空'}],
          time: [{required: true, message: '事件时间不能为空'}],
          content: [{required: true, message: '事件内容不能为空'}, {min: 8, message: '长度至少 8 个字符', trigger: 'blur'}]
        },
        myChartScorePie: '',
        myChartTripPie: ''
      }
    },
    methods: {
      handleCurrentChange3(val) {
        this.stuTripShow['data'] = []
        for (var i = (val - 1) * 10; i < (val - 1) * 10 + 10 && i < this.stuTripNum; i++) {
          this.stuTripShow['data'].push(this.stuTripTemp['data'][i])
        }
      },
      handleCurrentChange2(val) {
        this.stuCardShow['data'] = []
        for (var i = (val - 1) * 10; i < (val - 1) * 10 + 10 && i < this.stuCardNum; i++) {
          this.stuCardShow['data'].push(this.stuCardTemp['data'][i])
        }
      },
      change2() {
        if (this.value2[0] == null) {
          this.currentPage2 = 1
          this.stuCardTemp['data'] = this.stuCard['data']
          this.stuCardNum = this.stuCard['data'].length
          for (var i = 0; i < 10 && i < this.stuCardNum; i++) {
            this.stuCardShow['data'].push(this.stuCard['data'][i])
          }
        }
        else {
          this.currentPage2 = 1
          this.stuCardShow['data'] = []
          this.stuCardTemp['data'] = []
          let flag = false
          for (let i in this.stuCard['data']) {
            if ((new Date(this.stuCard['data'][i]['tradingTime'].slice(0, 10))).getTime() > this.value2[0].getTime() && (new Date(this.stuCard['data'][i]['tradingTime'].slice(0, 10))).getTime() < this.value2[1].getTime() + 86400000) {
              this.stuCardTemp['data'].push(this.stuCard['data'][i])
            }
          }
          this.stuCardNum = this.stuCardTemp['data'].length
          for (var i = 0; i < 10 && i < this.stuCardNum; i++) {
            this.stuCardShow['data'].push(this.stuCardTemp['data'][i])
          }
        }
      },
      handleCurrentChange(val) {
        this.stuScoreShow['data'] = []
        for (var i = (val - 1) * 10; i < (val - 1) * 10 + 10 && i < this.stuScoreNum; i++) {
          this.stuScoreShow['data'].push(this.stuScoreTemp['data'][i])
        }
        //console.log(this.tableInfoShow['data'])
      },
      change1() {
        if (this.value1[0] == null) {
          this.currentPage3 = 1
          this.stuTripTemp['data'] = this.stuTrip['data']
          this.stuTripNum = this.stuTrip['data'].length
          for (var i = 0; i < 10 && i < this.stuTripNum; i++) {
            this.stuTripShow['data'].push(this.stuTrip['data'][i])
          }
        }
        else {
          this.currentPage3 = 1
          this.stuTripShow['data'] = []
          this.stuTripTemp['data'] = []
          let flag = false
          for (let i in this.stuTrip['data']) {
            if ((new Date(this.stuTrip['data'][i]['entryDate'].slice(0, 10))).getTime() > this.value1[0].getTime() && (new Date(this.stuTrip['data'][i]['entryDate'].slice(0, 10))).getTime() < this.value1[1].getTime() + 86400000) {
              this.stuTripTemp['data'].push(this.stuTrip['data'][i])
            }
          }
          this.stuTripNum = this.stuTripTemp['data'].length
          for (var i = 0; i < 10 && i < this.stuTripNum; i++) {
            this.stuTripShow['data'].push(this.stuTripTemp['data'][i])
          }
        }
      },
      filterByInputDataForSearch1() {
        var index
        var indexProp
        var tableInfoShowTemp = JSON.parse(JSON.stringify(this.stuScore))
        var ifpush
        this.loadingButton1 = true
        tableInfoShowTemp['data'] = new Array()
        for (index in this.stuScore['data']) {
          ifpush = false
          for (indexProp in this.stuScore['propName']) {
            if (String(this.stuScore['data'][index][this.stuScore['propName'][indexProp]]).match(this.inputDataForSearch1) != null) {
              ifpush = true
              break
            }
          }
          if (ifpush == true) {
            tableInfoShowTemp['data'].push(this.stuScore['data'][index])
          }
        }
        this.currentPage1 = 1
        this.stuScoreShow['data'] = []
        this.stuScoreNum = tableInfoShowTemp['data'].length
        for (var i = 0; i < 10 && i < this.stuScoreNum; i++) {
          this.stuScoreShow['data'].push(tableInfoShowTemp['data'][i])
        }
        this.loadingButton1 = false
      },
      delInputDataForSearch1() {
        this.currentPage1 = 1
        this.inputDataForSearch1 = ''
        this.stuScoreTemp = this.stuScore
        this.stuScoreShow['data'] = []
        this.stuScoreNum = this.stuScoreTemp['data'].length
        for (var i = 0; i < 10 && i < this.stuScoreNum; i++) {
          this.$set(this.stuScoreShow['data'], i, this.stuScoreTemp['data'][i])
        }
      },
      drawPersonalScorePie() {
        var echarts = require('echarts');
        var myChart = echarts.init(document.getElementById('personalScorePie'));

        let option = drawPersonalScorePie(this.stuScore)
        myChart.setOption(option)
        return myChart
      },
      drawPersonalCardLine() {
        var echarts = require('echarts');
        var myChart = echarts.init(document.getElementById('personalCardLine'));

        let option = drawPersonalCardLine(this.stuCard)
        myChart.setOption(option)
        return myChart
      },
      drawPersonalTripPie() {
        var echarts = require('echarts');
        var myChart = echarts.init(document.getElementById('personalTripPie'));

        let option = drawPersonalTripPie(this.stuTrip)
        myChart.setOption(option)
        return myChart
      },
      removeDomain(item) {
        var index = this.dynamicValidateForm.domains.indexOf(item)
        if (index !== -1) {
          this.dynamicValidateForm.domains.splice(index, 1)
        }
      },
      addDomain() {
        this.dynamicValidateForm.domains.push({
          value: '',
          key: Date.now()
        });
      },
      ifCancelFocus(mode) {
        //mode为0，表示取消，不对该学生进行取消关注的操作
        //mode为1，表示确定，取消对该学生的关注，将状态制成正常
        if (mode == 0) {
          this.cancelFocusDialogVisible = false
          this.$notify.info({
            title: '消息',
            message: '您取消了本次操作'
          })
        } else if (mode == 1) {
          let data = {
            stuId: this.$store.state.stuid,
            userId: this.$store.state.userid,
          }
          postPersonCancelFocus(data).then((res) => {
            if (res['status'] == 1) {
              this.$notify({
                title: '操作成功',
                message: '您已取消了对' + this.stuBicData['data']['stuName'] + '的关注',
                type: 'success'
              })
              this.cancelFocusDialogVisible = false
              let that = this
              getPersonBasicInfo(this.$store.state.userid, this.$store.state.stuid).then((data) => {
                that.stuBicTotalData = data
                that.stuBicData = that.stuBicTotalData['basicInfo']
                that.stuFocusInfo = that.stuBicTotalData['focusInfo']
              })
            } else {
              this.$notify({
                title: '操作失败',
                message: '系统拒绝或无响应，请稍后重试',
                type: 'warning'
              })
              this.cancelFocusDialogVisible = false
            }
          })
        }
        return ''
      },
      changeIcon(mode, elementName) {
        var icon
        if (elementName == 'addNewEventClass') {
          icon = 'fa-address-book-o'
        } else if (elementName == 'cancelFocusClass') {
          icon = 'fa-eye-slash'
        } else if (elementName == 'addFocusClass') {
          icon = 'fa-eye'
        }
        if (mode == 0) {
          this[elementName] = 'fa ' + icon + ' fa-lg txt-blue cur-icon'
        } else {
          this[elementName] = 'fa ' + icon + ' fa-lg txt-green cur-icon'
        }
      },
      delEventFormContent() {
        //清空事件表单内的数据
        this.eventFormContent = {
          theme: '',
          time: '',
          content: ''
        }
      },
      delFocusFormContent() {
        //清空添加关注表单内的数据
        this.addFocusFormContent = {
          focusLevel: '1',
          focusReason: '',
          sleepInOrOut: '0',//是否校外住宿
          studyWithParent: '0'//是否家长陪读
        }
        //清空上次校验的结果
        this.resetForm(this.addFocusFormContent)
      },
      resetForm(formName) {
        if (this.$refs[formName]) {
          this.$refs[formName].resetFields()
        }
      },
      ifAddEvent(mode) {
        //0表示取消，不添加事件，
        //1表示接受，添加事件
        if (mode == 0) {
          this.eventDialogFormVisible = false
          this.delEventFormContent()
          this.$notify.info({
            title: '消息',
            message: '您取消了本次操作'
          })
          return ''
        }
        this.$refs[this.eventFormContent].validate((valid) => {
          if (valid) {
            let data = {
              stuId: this.$store.state.stuid,
              userId: this.$store.state.userid,
              theme: this.eventFormContent.theme,
              time: this.eventFormContent.time,
              content: this.eventFormContent.content
            }
            postPersonAddEvent(data).then((res) => {
              if (res['status'] == 1) {
                this.$notify({
                  title: '操作成功',
                  message: '成功添加了事件',
                  type: 'success'
                })
                this.addFocusDialogVisible = false

                getPersonEventInfo(this.$store.state.userid, this.$store.state.stuid).then((data) => {
                  this.stuEvent = data['data']
                })
              } else {
                this.$notify({
                  title: '操作失败',
                  message: res['errorInfo'],
                  type: 'warning'
                })
                this.addFocusDialogVisible = false
              }
            })
            this.eventDialogFormVisible = false
          } else {
          }
        })
        return ''
      },
      ifAddFocus(mode) {
        //0表示取消，不添加关注，
        //1表示接受，添加关注
        if (mode == 0) {
          this.addFocusDialogVisible = false
          this.$notify.info({
            title: '消息',
            message: '您取消了本次操作'
          })
          return ''
        } else if (mode == 1) {
          this.$refs[this.addFocusFormContent].validate((valid) => {
            if (valid) {
              let data = {
                stuId: this.$store.state.stuid,
                userId: this.$store.state.userid,
                focusLevel: this.addFocusFormContent['focusLevel'],
                reson: this.addFocusFormContent['focusReason'],
                sleepInOrOut: this.addFocusFormContent['sleepInOrOut'],
                studyWithParent: this.addFocusFormContent['studyWithParent']
              }
              postPersonAddFocus(data).then((res) => {
                if (res['status'] == 1) {
                  this.$notify({
                    title: '操作成功',
                    message: '成功添加了对' + this.stuBicData['data']['stuName'] + '的关注',
                    type: 'success'
                  })
                  let that = this
                  getPersonBasicInfo(this.$store.state.userid, this.$store.state.stuid).then((data) => {
                    that.stuBicTotalData = data
                    that.stuBicData = that.stuBicTotalData['basicInfo']
                    that.stuFocusInfo = that.stuBicTotalData['focusInfo']
                  })
                } else {
                  this.$notify({
                    title: '操作失败',
                    message: '原因：' + res['errorInfo'],
                    type: 'warning'
                  })
                }
                this.addFocusDialogVisible = false
              })
            } else {
              //console.log('error submit!!');
            }
          })

        }
      }
    },
    mounted() {
      let that = this
      window.onresize = () => {
        /*             myChartScorePie.resize() */
        /* myChartTripPie.resize() */
        if (that.myChartCardLine != "") {
          that.myChartCardLine.resize()
        }
        if (that.myChartTripPie != "") {
          that.myChartTripPie.resize()
        }
        if (that.myChartScorePie != "") {
          that.myChartScorePie.resize()
        }
      }
      if (this.$store.state.stuid == '') {
        this.$store.state.stuid = localStorage.stuID
      }
      getPersonBasicInfo(this.$store.state.userid, this.$store.state.stuid).then((data) => {
        that.stuBicTotalData = data
        that.stuBicData = that.stuBicTotalData['basicInfo']
        that.stuFocusInfo = that.stuBicTotalData['focusInfo']
      })
      getPersonEventInfo(this.$store.state.userid, this.$store.state.stuid).then((data) => {
        that.stuEvent = data['data']
      })
      //this.stuScore = this.stuBicTotalData['score']

      //画成绩统计部分
      getPersonScoreInfo(this.$store.state.userid, this.$store.state.stuid).then((data) => {
        that.stuScore = data['data']
        that.stuScoreTemp = data['data']
        that.stuScoreShow['colName'] = that.stuScore['colName']
        that.stuScoreShow['propName'] = that.stuScore['propName']
        that.stuScoreNum = that.stuScore['data'].length
        for (var i = 0; i < 10 && i < this.stuScoreNum; i++) {
          that.stuScoreShow['data'].push(that.stuScore['data'][i])
        }
        that.myChartScorePie = that.drawPersonalScorePie(that.stuScore)
      })

      //画进出寝室统计部分
      getPersonTripInfo(this.$store.state.userid, this.$store.state.stuid).then((data) => {
        that.stuTrip = data['data']
        that.stuTripNum = that.stuTrip['data'].length
        that.stuTripTemp['data'] = that.stuTrip['data']
        for (var i = 0; i < 10 && i < this.stuTripNum; i++) {
          that.stuTripShow['data'].push(that.stuTrip['data'][i])
        }
        that.myChartTripPie = that.drawPersonalTripPie(that.stuTrip)
      })

      //画一卡通消费统计部分
      getPersonCardInfo(this.$store.state.userid, this.$store.state.stuid).then((data) => {
        that.stuCard = data['data']
        that.stuCardTemp['data'] = that.stuCard['data']
        that.stuCardNum = that.stuCard['data'].length
        for (var i = 0; i < 10 && i < this.stuCardNum; i++) {
          that.stuCardShow['data'].push(that.stuCard['data'][i])
        }
        that.myChartCardLine = that.drawPersonalCardLine(that.stuCard)
      })

      //标志加载完毕
      this.loadingTable = false
    }
  }

</script>

<style scoped>
  .txt-big {
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    font-size: 17px;
  }

  .txt-blue {
    color: #0099CC;
    font-size: 25px;
  }

  .txt-green {
    color: #339933;
    font-size: 25px;
  }

  .cur-icon {
    cursor: pointer;
  }

  .tiny-line {
    height: 1px;
    background: #CCCCCC;
    overflow: hidden;
  }

  #h3 {
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  }
</style>

