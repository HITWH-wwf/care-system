<template>
    <div>
        <el-row type="flex" justify="center" style="margin-top:30px">
            <el-col :span="5">
                <el-button class="fa fa-question-circle-o" type="primary" @click="dialogVisible = true">
                    说 明
                </el-button>
                <el-button class="fa fa-cloud-download" type="primary" @click="downLoad">
                    下载基本数据模板
                </el-button>
            </el-col>
        </el-row>
        <el-row style="margin-top:30px" type="flex" justify="center">
            <el-col :span="6">
                <el-upload drag :action="dataUpdateBasicUrlT" multiple show-file-list name="file" :on-success="funGetSuccessResponse" :on-error="funGetErroeResponse" :before-upload="funBeforeUpload">
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">将文件拖到此处,或
                        <em>点击上传</em>
                    </div>
                </el-upload>
            </el-col>
        </el-row>
        <el-dialog title="使用说明" :visible.sync="dialogVisible" size="tiny">
            <span class="txt">请您单击下载模板按钮,将所需要导入的数据按照下载的模板格式填充完毕,然后通过拖拽或者单击上传的方式将该模板文件上传至服务端,待服务端校验完毕后会将您的数据添加入库。</span>
            </br>
            <span class="txt">您上传的数据将以学生学号为关键字进行覆盖/新增操作,即:若该学号已存在于当前数据库中,系统将依据您最新上传的数据更新旧的数据;若该学号并不存在于当前的数据库中,系统将数据新增入库。</span>
            </br>
            <span class="txt">请您严格遵守模板的限定,不要增加、删除、修改列名,也不要增加sheet(工作表)。</span>

            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="dialogVisible = false">关 闭</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { officeSuggestions, dataGetModeBasic, JSONToExcelConvertor, dataGetBasicFailed } from '@/api/api'
import { dataUpdateBasicUrl, dataUpdateBasicUrlGetModel } from '@/api/httpapi'

export default {
    data() {
        return {
            dialogVisible: false,
            dataUpdateBasicUrlT: dataUpdateBasicUrl,
            loadingInstance: ''
        }
    },
    methods: {
        downLoad() {
            window.location = dataUpdateBasicUrlGetModel
            return ''
            var model = dataGetModeBasic()
            var title = []
            var data = []
            for (var con in model) {
                title.push([con])
            }
            JSONToExcelConvertor(data, "学生关怀系统--基础数据导入模板", title)
        },
        funBeforeUpload(file) {
            this.loadingInstance = this.$loading({ 'text': '系统正在校验您上传的文件,请稍候' })
        },
        funGetSuccessResponse(response, file, fileList) {
            this.loadingInstance.close()
            if (response['status'] == 0) {
                this.$notify({
                    title: '警告',
                    message: '您的文件未通过系统校验，拒绝执行数据更新操作。检验错误信息为:' + response["errorInfo"],
                    type: 'error',
                    duration: 10000
                })
            } else if (response['status'] == 1) {
                this.$notify({
                    title: '成功',
                    message: '系统已接受您上传的文件并成功更新了数据库。其返回信息为: ' + response['errorInfo'],
                    type: 'success'
                })
            } else if (response['status'] == 2) {
                dataGetBasicFailed(response["file"])
                this.$notify({
                    title: '未全部完成',
                    message: '系统已接受您上传的文件并成功更新了数据库，但在添加至数据库过程中发现有无法插入的情况。详情请查看系统返回的信息: ' + response['errorInfo'],
                    type: 'warning'
                })
            }
        },
        funGetErroeResponse(err, file, fileList) {
            this.loadingInstance.close()
            this.$notify.error({
                title: '错误',
                message: '系统在向后端传递过程中遇到错误,请稍候重试'
            })
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
    font-size: 150px;
}

.row-bg {
    padding: 10px 0px;
}

.back-grap {
    background-color: #999999
}

.txt {
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    font-size: 14px;
}
</style>
