<template>
  <el-row class="top-header">
    <el-col :span="3" class="logo-basic">
      <i class="fa fa-home fa-fw fa-lg cur-icon" @click="routerLink('home')"></i>
      <span class="cur-icon" @click="routerLink('home')">{{sysName}}</span>
    </el-col>
    <el-col :span="2" :offset="7">
      <el-dropdown @command="handleCommand">
                <span :class="indexState=='0'?elDropdownSpanSelect:elDropdownSpan">
                    <i class="fa fa-area-chart fa-lg"></i> 首 页
                </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="indexMajor" v-if="$store.state.pagePower['indexMajor']">
            {{$store.state.pageName['indexMajor']}}
          </el-dropdown-item>
          <el-dropdown-item command="indexStudents" v-if="$store.state.pagePower['indexStudents']">
            {{$store.state.pageName['indexStudents']}}
          </el-dropdown-item>
          <!--
          <el-dropdown-item command="person" v-if="$store.state.pagePower['person']">
            {{$store.state.pageName['person']}}
          </el-dropdown-item>
          -->
        </el-dropdown-menu>
      </el-dropdown>
    </el-col>
    <el-col :span="2">
      <el-dropdown @command="handleCommand">
                <span :class="indexState=='1'?elDropdownSpanSelect:elDropdownSpan">
                    <i class="fa fa-cubes fa-lg"></i> 办 公
                </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="officeDataExpore" v-if="$store.state.pagePower['officeDataExpore']">
            {{$store.state.pageName['officeDataExpore']}}
          </el-dropdown-item>
          <el-dropdown-item command="officeSuggestions" v-if="$store.state.pagePower['officeSuggestions']">
            {{$store.state.pageName['officeSuggestions']}}
          </el-dropdown-item>
          <el-dropdown-item command="dataFilter" v-if="$store.state.pagePower['dataFilter']">
            {{$store.state.pageName['dataFilter']}}
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-col>
    <el-col :span="2">
      <el-dropdown @command="handleCommand">
                <span :class="indexState=='2'?elDropdownSpanSelect:elDropdownSpan">
                    <i class="fa fa-cog fa-lg"></i> 系统管理
                </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="systemUserTeam" v-if="$store.state.pagePower['systemUserTeam']">
            {{$store.state.pageName['systemUserTeam']}}
          </el-dropdown-item>
          <el-dropdown-item command="systemRoleTeam" v-if="$store.state.pagePower['systemRoleTeam']">
            {{$store.state.pageName['systemRoleTeam']}}
          </el-dropdown-item>
          <el-dropdown-item command="systemUsers" v-if="$store.state.pagePower['systemUsers']">
            {{$store.state.pageName['systemUsers']}}
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-col>
    <el-col :span="2">
      <el-dropdown @command="handleCommand">
                <span :class="indexState=='3'?elDropdownSpanSelect:elDropdownSpan" style="margin-left:13px">
                    <i class="fa fa-database fa-lg"></i> 数据维护
                </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="dataUpdateBasic" v-if="$store.state.pagePower['dataUpdateBasic']">学生基本数据增量导入
          </el-dropdown-item>
          <el-dropdown-item command="dataUpdateScore" v-if="$store.state.pagePower['dataUpdateScore']">学生成绩数据增量导入
          </el-dropdown-item>
          <el-dropdown-item command="dataUpdateFocus" v-if="$store.state.pagePower['dataUpdateFocus']">重点关注数据增量导入
          </el-dropdown-item>

        </el-dropdown-menu>
      </el-dropdown>
    </el-col>
    <el-col :span="2" style="float:right">
      <el-dropdown @command="handleCommand1" style="cursor: pointer">
        <span style="color:#CCFF99;font-size:15px;">
          {{ this.$store.state.userid }}
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>注销</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-col>
  </el-row>
</template>

<script>

  import ElCol from "element-ui/packages/col/src/col";

  export default {
    components: {ElCol},
    data() {
      return {
        sysName: "学生关怀系统",
        elDropdownSpan: this.getElDropdownSpan(0),
        elDropdownSpanSelect: this.getElDropdownSpan(1),
        indexState: -1
      }
    },
    mounted() {
      //console.log(this.$store.state.pagePower['dataUpdateScore'])
      /*       console.log(this.$router);
            var i;
            var v;
            for (i in this.$router.options.routes)
            {
                  console.log(this.$router.options.routes[i]);
            } */
    },
    methods: {
      handleCommand(command) {
        if (command == 'indexMajor' | command == 'indexStudents' | command == 'person') {
          this.$store.commit('setIndexState', {'index': 0})
        } else if (command == "officeDataExpore" | command == "officeSuggestions" | command == "dataFilter") {
          this.$store.commit('setIndexState', {'index': 1})
        } else if (command == "systemUserTeam" | command == "systemUsers" | command == "systemRoleTeam") {
          this.$store.commit('setIndexState', {'index': 2})
        } else if (command == "dataUpdateBasic" | command == "dataUpdateScore" | command == "dataUpdateFocus") {
          this.$store.commit('setIndexState', {'index': 3})
        }
        this.routerLink(command)
      },
      handleCommand1() {
        this.$store.commit('delUserId')
        localStorage.clear()
        location.reload()
      },
      getElDropdownSpan(mode) {
        if (mode == 0) {
          return "cur-icon txt-blue el-dropdown-link";
        } else {
          return "cur-icon txt el-dropdown-link";
        }
      },
      routerLink(pathWant) {
        this.$router.push({path: '/' + pathWant})
      },
    },
    watch: {
      getIndexState(val) {
        this.indexState = val
      }
    },
    computed: {
      getIndexState() {
        return this.$store.state.indexState
      }
    }
  }
</script>

<style scoped>
  .top-header {
    height: 60px;
    width: 100%;
    background: #3399FF;
    top: 0px;
    height: 60px;
    font-size: 22px;
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 15px;
    border-color: rgba(238, 241, 146, 0.3);
    border-right-width: 1px;
    border-right-style: solid;

    overflow: hidden;
  }

  .logo-basic {
    overflow: hidden;
    color: #fff;
    min-width: 30px;
  }

  .cur-icon {
    cursor: pointer;
  }

  .txt {
    color: #fff;
    font-size: 18px;
  }

  .txt-blue {
    color: #000000;
    font-size: 16px;
  }

  .el-dropdown-menu {
    background: #3399FF;
  }
</style>

