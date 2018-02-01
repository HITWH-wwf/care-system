<template>
    <div>
        <el-row style="margin-top:50px;padding:10px 10px" :gutter="40">
            <el-col :span="6" :offset="6" style="margin-top:35px">
                <el-input placeholder="模糊搜索" icon="search" v-model="inputDataForSearch" :on-icon-click="filterByInputDataForSearch" @keyup.enter.native="filterByInputDataForSearch">
                </el-input>
            </el-col>
            <el-col :span="3" style="margin-top:35px">
                <div style="display: flex">
                    <el-button type="primary" icon="search" @click="filterByInputDataForSearch" :loading="loadingButton">搜 索</el-button>
                    <el-button type="primary" icon="delete2" @click="delInputDataForSearch">清空条件</el-button>
                </div>
            </el-col>
            <el-col :span="3" :offset="5">
                <el-tooltip effect="light" content="添加用户组" :enterable="false" :open-delay="300" placement="left">
                    <i :class="uploadCenter" @click="doUpload" @mousemove="funUploadCenter(0)" @mouseout="funUploadCenter(1)"></i>
                </el-tooltip>
            </el-col>
        </el-row>
        <el-row style="margin-top:30px">
            <el-col :span='20' :offset='2'>
                <el-table id="expore-table" :data="tableInfoShow['data']" style="width: 100%" highlight-current-row v-loading.body="loadingTable" fit>
                    <template v-for="(item, index) in tableInfoShow['colName']">
                        <el-table-column :prop="tableInfoShow['propName'][index]" :label="item" :key="item.key" v-if="tableInfoShow['propName'][index]!='status'" align='center'>
                        </el-table-column>
                    </template>
                    <el-table-column label="操作" align='center'>
                        <template slot-scope="scope">
                            <el-row>
                                <el-col :span="2" :offset="2">
                                    <el-tooltip content="更改权限" placement="left-start" effect="light" :enterable="false" :open-delay="400" transition="el-zoom-in-center">
                                        <i v-run="register(scope.$index, 'Change')" :class="iconClassMouseOutChange" @click="handleEdit(scope.$index, scope.row, 'Change')" @mousemove="changeIcon(0, scope.$index, 'Change')" @mouseout="changeIcon(1, scope.$index, 'Change')"></i>
                                    </el-tooltip>
                                </el-col>
                                <el-col :span="2" :offset="2">
                                    <el-tooltip content="删除该用户组" placement="left-start" effect="light" :enterable="false" :open-delay="400" transition="el-zoom-in-center">
                                        <i v-run="register(scope.$index, 'Delete')" :class="iconClassMouseOutDelete" @click="handleEdit(scope.$index, scope.row, 'Delete')" @mousemove="changeIcon(0, scope.$index, 'Delete')" @mouseout="changeIcon(1, scope.$index, 'Delete')"></i>
                                    </el-tooltip>
                                </el-col>
                            </el-row>
                        </template>
                    </el-table-column>
                </el-table>
                <el-dialog :title="changePowerTitle" :visible.sync="eventDialogFormVisible" size='large' @open="initChangePowerCheckList">
                    <el-row>
                        <el-col :span="20" :offset="2">
                            <el-checkbox-group v-model="changePowerCheckList">
                                <template v-for="(item, index) in changePowerData['data']">
                                    <el-checkbox :label="index" :key="item" align='center' style="margin-top:10px;margin-left:10px">
                                    </el-checkbox>
                                </template>
                            </el-checkbox-group>
                        </el-col>
                    </el-row>
                    <div slot="footer" class="dialog-footer">
                        <el-row>
                            <el-col :span="18" :offset="3">
                                <div style="display: flex;float:right">
                                    <el-button @click="changePower(0)">取 消</el-button>
                                    <el-button type="primary" @click="changePower(1)">确 定</el-button>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                </el-dialog>

                <el-dialog title="添加一个用户组" :visible.sync="addEventDialogFormVisible" size='tiny'>
                    <el-row>
                        <el-col :span="20" :offset="2">
                            <el-form :model="addPowerData" label-width="80px" :rules="rulesForAddPower" :ref="addPowerData">
                                <el-form-item label="用户组名" prop="name">
                                    <el-input v-model="addPowerData.name"></el-input>
                                </el-form-item>
                                <el-form-item label="描述" prop="description">
                                    <el-input v-model="addPowerData.description"></el-input>
                                </el-form-item>
                            </el-form>
                        </el-col>
                    </el-row>
                    <div slot="footer" class="dialog-footer">
                        <el-row>
                            <el-col :span="18" :offset="3">
                                <div style="display: flex;float:right">
                                    <el-button @click="addPower(0)">取 消</el-button>
                                    <el-button type="primary" @click="addPower(1)">确 定</el-button>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                </el-dialog>

                <el-dialog title="提示" :visible.sync="delUserTeamDialogVisible" size="tiny">
                    <span>您即将删除{{rowName}},删除后其数据无法恢复,请确认是否继续该操作</span>
                    <span slot="footer" class="dialog-footer">
                        <el-row>
                            <el-col :span="18" :offset="3">
                                <div style="display: flex;float:right">
                                    <el-button @click="ifDelUserTeam(0)">取 消</el-button>
                                    <el-button type="primary" @click="ifDelUserTeam(1)">确 定</el-button>
                                </div>
                            </el-col>
                        </el-row>
                    </span>
                </el-dialog>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import { systemGetTotalUserTeam, systemGetOneUserTeam, systemSetOneUserTeam, systemDelOneUserTeam, systemAddOneUserTeam } from '@/api/api'

export default {
    data() {
        return {
            tableInfoShow: '',
            tableInfoTotal: '',
            elements: {},
            loadingTable: false,
            loadingButton: false,
            iconClassMouseMoveChange: 'fa fa-pagelines fa-2x txt-green cur-icon',
            iconClassMouseOutChange: 'fa fa-pagelines fa-lg txt-green',
            iconClassMouseMoveDelete: 'fa fa-trash fa-2x txt-blue cur-icon',
            iconClassMouseOutDelete: 'fa fa-trash fa-lg txt-blue',
            changePowerData: '',
            inputDataForSearch: '',
            changePowerTitle: '',
            changePowerCheckList: [],
            rowName: '',
            uploadCenter: "fa fa-users fa-5x txt-blue-upload",
            eventDialogFormVisible: false,
            delUserTeamDialogVisible: false,
            addEventDialogFormVisible: false,
            addPowerData: {
                name: '',
                description: ''
            },
            rulesForAddPower: {
                name: [
                    { required: true, message: '请输入该用户的用户名', trigger: 'blur' },
                ],
                description: [
                    { required: true, message: '请输入该用户的相关描述', trigger: 'blur' },
                ]
            }
        }
    },
    directives: {
        //将该dom注册进this中
        run(el, binding) {
            if (typeof binding.value == 'function')
                binding.value(el)
        }
    },
    methods: {
        register(index, name) {
            return (el) => {
                this.elements[name + index] = el
            }
        },
        resetForm(formName) {
            if (this.$refs[formName]) {
                this.$refs[formName].resetFields()
            }
        },
        handleEdit(index, row, name) {
            this.rowName = row['name']
            if (name == 'Change') {
                let that = this
                systemGetOneUserTeam(this.$store.state.userid, row['name']).then(
                    (data) => {
                        that.changePowerData = data
                        that.changePowerTitle = '修改 ' + row['name'] + ' 权限'
                        that.eventDialogFormVisible = true
                    }
                )
            } else if (name == 'Delete') {
                this.delUserTeamDialogVisible = true
            }
        },
        changeIcon(mode, index, name) {
            let refValue = name + index
            if (mode == 0) {
                //this.iconClass = "fa fa-search fa-2x txt-blue"
                this.elements[refValue].className = this["iconClassMouseMove" + name]
            } else {
                //this.iconClass = "fa fa-search fa-lg txt-blue"
                this.elements[refValue].className = this["iconClassMouseOut" + name]
            }
        },
        delInputDataForSearch() {
            this.inputDataForSearch = ''
            this.tableInfoShow = this.tableInfoTotal
        },
        addPower(mode) {
            //mode为0，单击了取消
            //mode为1，单击了确定，添加一个用户组
            if (mode == 0) {
                this.addEventDialogFormVisible = false
                this.$notify.info({
                    title: '消息',
                    message: '您取消了本次操作'
                })
                return ''
            } else if (mode == 1) {
                this.$refs[this.addPowerData].validate((valid) => {
                    if (valid) {
                        //添加一个用户组
                        let that = this
                        systemAddOneUserTeam(this.$store.state.userid, this.addPowerData).then(
                            (data) => {
                                that.addEventDialogFormVisible = false
                                if (data["status"].toString() == "1") {
                                    that.initTable()
                                    that.$notify.success({
                                        title: '消息',
                                        message: '操作已成功'
                                    })
                                } else {
                                    that.$notify.error({
                                        title: '消息',
                                        message: "系统返回失败，失败信息为:" + data["errorInfo"]
                                    })
                                }
                            }
                        )

                    } else {
                        return ''
                    }
                })
            }
        },
        doUpload() {
            //添加一个用户组
            this.addPowerData = {
                name: '',
                description: ''
            }
            this.resetForm(this.addPowerData)
            this.addEventDialogFormVisible = true
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
                    if (this.tableInfoTotal['data'][index][this.tableInfoTotal['propName'][indexProp]].match(this.inputDataForSearch) != null) {
                        ifpush = true
                        break
                    }
                }
                if (ifpush == true) {
                    tableInfoShowTemp['data'].push(this.tableInfoTotal['data'][index])
                }
            }
            this.tableInfoShow = tableInfoShowTemp
            this.loadingButton = false
        },
        funUploadCenter(mode) {
            //转换添加用户按钮的class
            //mode为0是鼠标移动到了上面
            //mode为1是鼠标移动开了
            if (mode == 0) {
                this.uploadCenter = "fa fa-users fa-5x txt-green-upload"
            } else if (mode == 1) {
                this.uploadCenter = "fa fa-users fa-5x txt-blue-upload"
            }
        },
        changePower(mode) {
            //0表示取消，不修改权限，
            //1表示接受，修改权限
            if (mode == 0) {
                this.eventDialogFormVisible = false
                this.$notify.info({
                    title: '消息',
                    message: '您取消了本次操作'
                });
                return ''
            } else if (mode == 1) {
                //将勾选的结果刷新到changePowerData中,传递给后端记录和保存
                var item = 0
                var index = 0
                for (item in this.changePowerData['data']) {
                    this.changePowerData['data'][item] = 0
                }
                for (index = 0; index < this.changePowerCheckList.length; index++) {
                    this.changePowerData['data'][this.changePowerCheckList[index]] = 1
                }
                let that = this
                systemSetOneUserTeam(this.$store.state.userid, this.rowName, this.changePowerData['data']).then(
                    (data) => {
                        that.eventDialogFormVisible = false
                        if (data["status"].toString() == "1") {
                            that.initTable()
                            that.$notify.success({
                                title: '消息',
                                message: '操作已成功'
                            })
                        } else {
                            that.$notify.error({
                                title: '消息',
                                message: "系统返回失败，失败信息为:" + data["errorInfo"]
                            })
                        }
                    }
                )
            }
            return '';
        },
        initChangePowerCheckList() {
            //对权限进行勾选状态的初始化
            this.changePowerCheckList = []
            for (var item in this.changePowerData['data']) {
                if (this.changePowerData['data'][item].toString() == "1") {
                    this.changePowerCheckList.push(item)
                }
            }
        },
        ifDelUserTeam(mode) {
            //mode为0，表示取消，不进行删除用户组权限的操作
            //mode为1，表示确定，执行删除操作
            if (mode == 0) {
                this.delUserTeamDialogVisible = false
                this.$notify.info({
                    title: '消息',
                    message: '您取消了本次操作'
                });
                return ''
            } else if (mode == 1) {
                let that = this
                systemDelOneUserTeam(this.$store.state.userid, this.rowName).then(
                    (data) => {
                        if (data['status'] == 1) {
                            this.initTable()
                            that.$notify({
                                title: '操作成功',
                                message: '您已删除了' + this.rowName,
                                type: 'success'
                            });
                            that.delUserTeamDialogVisible = false
                        } else {
                            that.$notify({
                                title: '操作失败',
                                message: '系统返回了错误，错误信息为:' + data["errorInfo"],
                                type: 'warning'
                            });
                            that.delUserTeamDialogVisible = false
                        }
                    }
                )
            }
            return ''
        },
        initTable() {
            let that = this
            //从数据库中获取用户组列表
            systemGetTotalUserTeam(this.$store.state.userid).then(function (data) {
                if (data['status'] == 1) {
                    that.tableInfoTotal = data['data']
                    that.tableInfoShow = that.tableInfoTotal
                } else {
                    that.$notify({
                        title: '操作失败',
                        message: '获取用户组时，系统返回了错误，错误信息为:' + data["errorInfo"],
                        type: 'warning'
                    })
                }
            })
            this.inputDataForSearch = ''
        }
    },
    mounted() {
        //this.loadingTable = true
        this.initTable()
        //this.loadingTable = false
    }
}

</script>

<style scoped>
.txt-green {
    color: #13CE66
}

.txt-blue {
    color: #1D8CE0
}

.cur-icon {
    cursor: pointer;
}

.txt-blue-upload {
    border: 1px;
    color: #20A0FF;
    cursor: pointer
}

.txt-green-upload {
    border: 1px;
    color: #13CE66;
    cursor: pointer
}
</style>

