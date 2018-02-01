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
                <el-tooltip effect="light" content="添加用户" :enterable="false" :open-delay="300" placement="left">
                    <i :class="uploadCenter" @click="doUpload" @mousemove="funUploadCenter(0)" @mouseout="funUploadCenter(1)"></i>
                </el-tooltip>
            </el-col>
        </el-row>
        <el-row style="margin-top:30px">
            <el-col :span='20' :offset='2'>
                <el-table id="expore-table" :data="tableInfoShow['data']" style="width: 100%" highlight-current-row v-loading.body="loadingTable" fit>
                    <template v-for="(item, index) in tableInfoShow['colName']">
                        <el-table-column :prop="tableInfoShow['propName'][index]" :label="item" :key="item.key" v-if="tableInfoShow['propName'][index]!='passWord'" align='center'>
                        </el-table-column>
                    </template>
                    <el-table-column label="操作" align='center'>
                        <template slot-scope="scope">
                            <el-row>
                                <el-col :span="2" :offset="2">
                                    <el-tooltip content="更改内容" placement="left-start" effect="light" :enterable="false" :open-delay="400" transition="el-zoom-in-center">
                                        <i v-run="register(scope.$index, 'Change')" :class="iconClassMouseOutChange" @click="handleEdit(scope.$index, scope.row, 'Change')" @mousemove="changeIcon(0, scope.$index, 'Change')" @mouseout="changeIcon(1, scope.$index, 'Change')"></i>
                                    </el-tooltip>
                                </el-col>
                                <el-col :span="2" :offset="2">
                                    <el-tooltip content="删除该用户" placement="left-start" effect="light" :enterable="false" :open-delay="400" transition="el-zoom-in-center">
                                        <i v-run="register(scope.$index, 'Delete')" :class="iconClassMouseOutDelete" @click="handleEdit(scope.$index, scope.row, 'Delete')" @mousemove="changeIcon(0, scope.$index, 'Delete')" @mouseout="changeIcon(1, scope.$index, 'Delete')"></i>
                                    </el-tooltip>
                                </el-col>
                            </el-row>
                        </template>
                    </el-table-column>
                </el-table>
                <el-dialog :title="changePowerTitle" :visible.sync="eventDialogFormVisible" size='tiny' @open="resetForm(changePowerData)">
                    <el-row style="margin-top:10px">
                        <el-col :span="22" :offset="0">
                            <el-form :model="changePowerData" label-width="80px" :rules="rules" :ref="changePowerData">
                                <el-form-item label="用户名" prop="name">
                                    <el-input v-model="changePowerData.name" :disabled="nameDisable"></el-input>
                                </el-form-item>
                                <el-form-item label="用户组" prop="userTeamName">
                                    <el-select v-model="changePowerData.userTeamName" placeholder="请选择用户组">
                                        <template v-for="(item, index) in totalUserTeam['data']">
                                            <el-option :label="item['name']" :value="item['name']" :key="index"></el-option>
                                        </template>
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="角色组" prop="roleTeamName">
                                    <el-select v-model="changePowerData.roleTeamName" placeholder="请选择角色组">
                                        <template v-for="(item, index) in totalRoleTeam['data']">
                                            <el-option :label="item['name']" :value="item['name']" :key="index"></el-option>
                                        </template>
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="密码" prop="passWord">
                                    <el-input v-model="changePowerData.passWord" type="password"></el-input>
                                </el-form-item>
                                <el-form-item label="描述" prop="description">
                                    <el-input v-model="changePowerData.description" type="textarea" :autosize="{ minRows: 5, maxRows: 5}"></el-input>
                                </el-form-item>
                            </el-form>
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
                <el-dialog title="提示" :visible.sync="delRoleTeamDialogVisible" size="tiny">
                    <span>您即将删除用户:{{rowName}},删除后其数据无法恢复,请确认是否继续该操作</span>
                    <span slot="footer" class="dialog-footer">
                        <el-row>
                            <el-col :span="18" :offset="3">
                                <div style="display: flex;float:right">
                                    <el-button @click="ifDelUser(0)">取 消</el-button>
                                    <el-button type="primary" @click="ifDelUser(1)">确 定</el-button>
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
import { systemGetTotalUsers, systemSetOneUser, systemGetOneUser, systemDelOneUser, systemGetTotalRoleTeam, systemGetTotalUserTeam, systemAddOneUser } from '@/api/api'

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
            changePowerData: {
                name: '',
                description: '',
                passWord: '',
                userTeamName: '',
                roleTeamName: ''
            },
            inputDataForSearch: '',
            changePowerTitle: '',
            changePowerCheckList: [],
            //为0时表示当前打开的对话框是单击了更改权限按钮，为1表示当前打开的对话框是单击了添加用户按钮
            changePowerOrAddPowe: '0',
            rowName: '',
            totalUserTeam: '',
            totalRoleTeam: '',
            eventDialogFormVisible: false,
            delRoleTeamDialogVisible: false,
            rules: {
                name: [
                    { required: true, message: '请输入该用户的名称', trigger: 'blur' },
                ],
                passWord: [
                    { required: true, message: '请输入该用户的登录密码', trigger: 'blur' },
                    { min: 3, max: 12, message: '密码长度在 3 到 12 个字符', trigger: 'blur' }
                ],
                description: [
                    { required: true, message: '请输入该用户的相关描述', trigger: 'blur' },
                ],
                userTeamName: [
                    { required: true, message: '请选择用户组', trigger: 'blur' },
                ],
                roleTeamName: [
                    { required: true, message: '请选择角色组', trigger: 'blur' },
                ]
            },
            uploadCenter: "fa fa-user-plus fa-5x txt-blue",
            nameDisable: true,
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
        funUploadCenter(mode) {
            //转换添加用户按钮的class
            //mode为0是鼠标移动到了上面
            //mode为1是鼠标移动开了
            if (mode == 0) {
                this.uploadCenter = "fa fa-user-plus fa-5x txt-green"
            } else if (mode == 1) {
                this.uploadCenter = "fa fa-user-plus fa-5x txt-blue"
            }

        },
        delInputDataForSearch() {
            this.inputDataForSearch = ''
            this.tableInfoShow = this.tableInfoTotal
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
        resetForm(formName) {
            if (this.$refs[formName]) {
                this.$refs[formName].resetFields()
            }
        },
        handleEdit(index, row, name) {
            this.changePowerOrAddPowe = 0
            this.rowName = row['name']
            if (name == 'Change') {
                let that = this
                systemGetOneUser(this.$store.state.userid, row['name']).then(
                    (data) => {
                        that.changePowerData = data['data']
                        that.changePowerTitle = '修改 ' + row['name'] + ' 权限'
                        that.nameDisable = true
                        that.eventDialogFormVisible = true
                    }
                )
            } else if (name == 'Delete') {
                this.delRoleTeamDialogVisible = true
            }
        },
        changeIcon(mode, index, name) {
            let refValue = name + index
            if (mode == 0) {
                this.elements[refValue].className = this["iconClassMouseMove" + name]
            } else {
                this.elements[refValue].className = this["iconClassMouseOut" + name]
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
                this.$refs[this.changePowerData].validate((valid) => {
                    if (valid) {
                        if (this.changePowerOrAddPowe == 0) {
                            //修改权限
                            let that = this
                            systemSetOneUser(this.$store.state.userid, this.rowName, this.changePowerData).then(
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
                                })
                        } else if (this.changePowerOrAddPowe == 1) {
                            //添加用户
                            let that = this
                            systemAddOneUser(this.$store.state.userid, this.changePowerData).then(
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
                    } else {
                        return ''
                    }
                })
            }
            return ''
        },
        ifDelUser(mode) {
            //mode为0，表示取消，不进行删除角色组权限的操作
            //mode为1，表示确定，执行删除操作
            if (mode == 0) {
                this.delRoleTeamDialogVisible = false
                this.$notify.info({
                    title: '消息',
                    message: '您取消了本次操作'
                })
            } else if (mode == 1) {
                let that = this
                systemDelOneUser(this.$store.state.userid, this.rowName).then(
                    (data) => {
                        if (data['status'] == 1) {
                            that.initTable()
                            that.$notify({
                                title: '操作成功',
                                message: '您已删除了' + that.rowName,
                                type: 'success'
                            })
                            that.delRoleTeamDialogVisible = false
                        } else {
                            that.$notify({
                                title: '操作失败',
                                message: '系统返回了错误，错误信息为:' + data["errorInfo"],
                                type: 'warning'
                            })
                            that.delRoleTeamDialogVisible = false
                        }
                    }
                )

            }
        },
        doUpload() {
            //添加一个用户
            this.changePowerOrAddPowe = 1
            this.initChangePower()
            this.eventDialogFormVisible = true
        },
        initChangePower() {
            //为添加用户功能做初始化的准备
            this.changePowerTitle = "添加新用户"
            this.changePowerData = {
                name: '',
                description: '',
                passWord: '',
                userTeamName: '',
                roleTeamName: ''
            }
            this.nameDisable = false
        },
        initTable() {
            //从数据库中获取用户列表
            let that = this
            systemGetTotalUsers(this.$store.state.userid).then(function (data) {
                that.tableInfoTotal = data['data']
                if (data["status"] == 1) {
                    //成功
                    that.tableInfoShow = that.tableInfoTotal
                } else {
                    //失败
                    that.$notify({
                        title: '操作失败',
                        message: '系统返回了错误，错误信息为:' + that.tableInfoTotal["errorInfo"],
                        type: 'warning'
                    })
                }
            })
        }
    },
    mounted() {
        //this.loadingTable = true
        let that = this

        this.initTable()

        systemGetTotalRoleTeam(this.$store.state.userid).then(function (data) {
            if (data['status'] == 1) {
                that.totalRoleTeam = data['data']
            } else {
                that.$notify({
                    title: '操作失败',
                    message: '获取所有角色组时，系统返回了错误，错误信息为:' + data["errorInfo"],
                    type: 'warning'
                })
            }
        })

        systemGetTotalUserTeam(this.$store.state.userid).then(function (data) {
            if (data['status'] == 1) {
                that.totalUserTeam = data['data']
            } else {
                that.$notify({
                    title: '操作失败',
                    message: '获取所有用户组时，系统返回了错误，错误信息为:' + data["errorInfo"],
                    type: 'warning'
                })
            }
        })
        //this.loadingTable = false
    },
    watch: {

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
    cursor: pointer
}

.txt-blue {
    border: 1px;
    color: #20A0FF;
    cursor: pointer
}

.txt-green {
    border: 1px;
    color: #13CE66;
    cursor: pointer
}

body {
    text-align: center
}
</style>

