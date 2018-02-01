<template>
    <el-row class="center" type="flex" justify="center">
        <div>
            <i :class="iconClass" @mousemove="changeIcon(0)" @mouseout="changeIcon(1)" @click="upload"></i>
        </div>
    
        <el-dialog title="添加一条意见反馈" :visible.sync="addEventDialogFormVisible" size='tiny' @open="initAddSuggestions">
            <el-row>
                <el-col :span="20" :offset="1">
                    <el-form :model="addSuggestions" label-width="80px" :rules="rulesForAddPower" :ref="addSuggestions">
                        <el-form-item label="星级" prop="start">
                            <el-rate v-model="addSuggestions.start" :allow-half="true" :show-text="true" style="margin-top:5px"></el-rate>
                        </el-form-item>
                        <el-form-item label="您的意见" prop="suggestions">
                            <el-input v-model="addSuggestions.suggestions" :autosize="{ minRows: 15, maxRows: 15}" type="textarea"></el-input>
                        </el-form-item>
                    </el-form>
                </el-col>
            </el-row>
            <div slot="footer" class="dialog-footer">
                <el-row>
                    <el-col :span="18" :offset="3">
                        <div style="display: flex;float:right">
                            <el-button @click="funAddSuggestions(0)">取 消</el-button>
                            <el-button type="primary" @click="funAddSuggestions(1)">提 交</el-button>
                        </div>
                    </el-col>
                </el-row>
            </div>
        </el-dialog>
    
    </el-row>
</template>

<script>
import { officeSuggestions } from '@/api/api'

export default {
    data() {
        return {
            iconClass: "fa fa-thumbs-o-up big-icon cur-icon txt-blue",
            addEventDialogFormVisible: false,
            addSuggestions: {
                start: 5,
                suggestions: ''
            },
            rulesForAddPower: {
                suggestions: [
                    { required: true, message: '请输入您的意见', trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        changeIcon(mode) {
            if (mode == 0) {
                this.iconClass = "fa fa-thumbs-o-up big-icon cur-icon txt-green"
            } else if (mode == 1) {
                this.iconClass = "fa fa-thumbs-o-up big-icon cur-icon txt-blue"
            }
        },
        resetForm(formName) {
            if (this.$refs[formName]) {
                this.$refs[formName].resetFields()
            }
        },
        upload() {
            this.addEventDialogFormVisible = true
        },
        initAddSuggestions() {
            //初始化反馈意见的参数
            this.addSuggestions = {
                start: 5,
                suggestions: ''
            }
            this.resetForm(this.addSuggestions)
        },
        funAddSuggestions(mode) {
            //mode为0的时候，表示取消
            //mode为1的时候，表示提交
            if (mode == 0) {
                this.addEventDialogFormVisible = false
                this.$notify.info({
                    title: '消息',
                    message: '您取消了本次操作'
                })
                return ''
            } else if (mode == 1) {
                this.$refs[this.addSuggestions].validate((valid) => {
                    if (valid) {
                        this.addEventDialogFormVisible = false
                        let that = this
                        officeSuggestions(this.$store.state.userid, this.addSuggestions['suggestions'], this.addSuggestions['start']).then(
                            (data) => {
                                if (data["status"].toString() == "1") {
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
        }
    }
}
</script>

<style scoped>
.txt-green {
    color: #F7BA2A
}

.txt-blue {
    color: #1F2D3D
}

.cur-icon {
    cursor: pointer;
}

.center {
    width: 50%;
    height: 50%;
    overflow: auto;
    margin: auto;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
}

.big-icon {
    font-size: 300px;
}
</style>
