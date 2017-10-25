<template>
<div>
	<el-row>
		<el-col style="margin-top:50px" :span="18" :offset="3">
		  <h1>选择筛选条件</h1>
		  <el-checkbox-group v-model="checkList" @change="changeOptions">
		  	<el-checkbox v-for="item in events" :key="item.key" :label="item.value">{{item.name}}</el-checkbox>
		  </el-checkbox-group>
		</el-col>
	</el-row>
	<el-row>
		<el-col style="margin-top:50px" :span="18" :offset="3">
			<h1>详细条件</h1>
			<div class="condition">
				<div class="uncheck" v-if="!ifCheck">
					暂无选项
				</div>
				<div class="checked" v-if="ifCheck">
					<!-- 每个选项的不同导致必须写死 -->
					<div class="opt" v-if="options.card">
						<div class="opt-left">
							一卡通消费
						</div>
						<div class="opt-right">
							<span style="width:20%; display: inline-block;">日消费额</span> >=
							<el-input v-model="selectData.card.consume"style="width:60px;margin-left: 10px;" size="mini"></el-input>

							<span style="width:20%; display: inline-block; margin-left:60px;">超额次数</span> >=
							<el-input v-model="selectData.card.number"style="width:60px;margin-left: 10px;" size="mini"></el-input>

						</div>
					</div>
					<div class="opt" v-if="options.sleep">
						<div class="opt-left">
							归寝统计
						</div>
						<div class="opt-right">
							<span style="width:20%; display: inline-block;">异常归寝次数</span> >=
							<el-input v-model="selectData.days" style="width:60px;margin-left: 10px;" size="mini"></el-input>
						</div>
					</div>
					<div class="opt" v-if="options.fail">
						<div class="opt-left">
							不及格科目
						</div>
						<div class="opt-right">
							<span style="width:20%; display: inline-block;">补考不及格科目数量</span> >=
							<el-input v-model="selectData.sbjNumber" style="width:60px;margin-left: 10px;" size="mini"></el-input>
						</div>
					</div>
					<!-- 选项结束 -->

					<el-button type="primary" class="btn" @click="sub">提 交</el-button>
				</div>
			</div>
		</el-col>
	</el-row>
    <el-row style="margin-top:30px">
        <el-col :span="22" :offset="1">
            <el-table :data="tableInfoShow['data']" style="width: 100%" highlight-current-row  height="700">
                <template v-for="(item, index) in tableInfoShow['colName']">
                    <el-table-column :prop="tableInfoShow['propName'][index]" :label="item" :key="item.key" v-if="tableInfoShow['propName'][index]!='state'" align='center'>
                    </el-table-column>
                    <el-table-column :prop="tableInfoShow['propName'][index]" :label="item" :key="item.key" v-else align='center'>
                        <template slot-scope="scope">
                            <el-tag :color="tableRowStyle(scope.row)" close-transition>{{scope.row.state}}</el-tag>
                        </template>
                    </el-table-column>
                </template>
                <el-table-column label="操作" align='center'>
                    <template slot-scope="scope">
                        <i class="hoverPoint" v-run="register(scope.$index)" :class="iconClassMouseOut" @click="handleEdit(scope.$index, scope.row)" @mousemove="changeIcon(0, scope.$index)" @mouseout="changeIcon(1, scope.$index)"></i>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
</div>
</template>

<script>
	import {officeDataFilter} from '@/api/api'
	export default{
		data(){
			return{
				tableInfoShow:[],
				checkList: [],
				events:[{"name":"一卡通消费","value":"card"},
						{"name":"归寝统计","value":"sleep"},
						{"name":"不及格科目","value":"fail"},
				],
				options:{},
				selectData:{
					card:{
						consume:'',
						number:''
					},
					days:'',
					sbjNumber:'',
				},
				elements: {},
				iconClassMouseMove: 'fa fa-search fa-2x txt-blue cur-icon',
				iconClassMouseOut: 'fa fa-search fa-lg txt-blue',
			};
		},
		computed:{
			ifCheck:function(){
				return this.checkList.length == 0 ? false:true;
			},
		},
		directives: {
	        //将该dom注册进this中
	        run(el, binding) {
	            if (typeof binding.value == 'function')
	                binding.value(el);
	        }
	    },
		methods:{
			changeOptions:function(){
				this.options = {};
				for (let item in this.checkList){
					this.options[this.checkList[item]] = true;
					this.selectData = {
						card:{
							consume:'',
							number:''
						},
						days:'',
						sbjNumber:''
					}
				};
			},
			register:function(index) {
	            return (el) => {
	                this.elements["icon" + index] = el;
	            }
	        },
	        handleEdit:function(index, row) {
	            this.$store.commit("setStuId", { stuid: row['stuID'] })
	            this.$router.push({ path: "/person" })
	            //setStuId
	        },
	        tableRowStyle:function(row) {
	            if (row['state'] == '推介关注') {
	                return '#F7BA2A'
	            } else if (row['state'] == '重点关注') {
	                return '#FF4949'
	            } else if (row['state'] == '毕业') {
	                return '#13CE66'
	            }
	            return '#1D8CE0'
	        },
	        changeIcon:function(mode, index) {
	            let refValue = 'icon' + index
	            if (mode == 0) {
	                //this.iconClass = "fa fa-search fa-2x txt-blue"
	                this.elements[refValue].className = this.iconClassMouseMove
	            } else {
	                //this.iconClass = "fa fa-search fa-lg txt-blue"
	                this.elements[refValue].className = this.iconClassMouseOut
	            }
	        },
			sub:function(){
				let data = this.selectData
				data["userId"] = this.$store.state.userid
				if((data.card.consume !='' && data.card.number =='')||(data.card.consume =='' && data.card.number != '')){
					this.$alert('查询信息不完整', '提示', {
			          confirmButtonText: '确定'});
					return;
				}
				officeDataFilter(data).then((res) => {
					if(res.status == 1){
						this.tableInfoShow = res.data;
					}
					else{
						//console.log("error");
					}
				})
			}
		}
	}
</script>

<style scoped>
	h1{
		font-weight: 400;
		font-size: 22px;
	}
	.condition{
		width: 100%;
		border: 1px solid #e5e5e5;
		border-radius: 4px;
		min-height: 100px;
		overflow: hidden;
	}
	.uncheck{
		width: 100%;
		height: 100%;
		padding-top: 40px;
		text-align: center;
		color:grey;
		font-size: 16px;
	}
	.opt{
		box-sizing: border-box;
		padding-top: 10px;
		width: 100%;
		height: 50px;
		font-size: 16px;
		padding-left: 20px;
		line-height: 40px;
		border-bottom: 1px dashed #e5e5e5;
	}
	.opt-left{
		width: 30%;
		height: 100%;
		float: left;
	}
	.opt-right{
		width: 60%;
		height: 100%;
		float: left;
	}
	.btn{
		float: right;
		font-size: 16px;
		margin:5px 40px 5px auto;
	}
	.hoverPoint{
	    cursor: pointer;
	}
</style>
