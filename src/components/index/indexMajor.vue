<template>
    <div>
        <el-row style="margin-top:30px">
            <el-col :span="20" :offset="2">
                <div id="indexMajorLine" style="width:100%;min-height:700px;height:100%;"></div>
            </el-col>
        </el-row>
    
        <el-row style="margin-top:40px">
            <el-col :span="20" :offset="2">
                <div id="indexMajorBar" style="width:100%;min-height:700px;height:100%;"></div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import { getIndexMajorLineInfo, getIndexMajorBarInfo } from '@/api/api'
import { drawIndexMajorLine, drawIndexMajorBar } from '@/api/echarts'

export default {
    data() {
        return {
            //var echarts = require('echarts');
            myChartLine: '',
            myChartBar: ''
        }
    },
    components: {
    },
    methods: {
        drawIndexMajorLine() {
            var echarts = require('echarts')
            this.myChartLine = echarts.init(document.getElementById('indexMajorLine'))
            let that = this
            getIndexMajorLineInfo(this.$store.state.userid).then((data) => {
                that.data = data['data']
                var option = drawIndexMajorLine(that.data)
                that.myChartLine.setOption(option)
            })
        },
        drawIndexMajorBar() {
            var echarts = require('echarts')
            this.myChartBar = echarts.init(document.getElementById('indexMajorBar'))
            let that = this
            getIndexMajorBarInfo(this.$store.state.userid).then((data) => {
                that.data = data['data']
                var option = drawIndexMajorBar(that.data)
                that.myChartBar.setOption(option)
            })
        },
    },
    mounted() {
        this.drawIndexMajorLine()
        this.drawIndexMajorBar()
        window.onresize = () => {
            this.myChartLine.resize()
            this.myChartBar.resize()
        }
    }
}
</script>

<style scoped>

</style>

