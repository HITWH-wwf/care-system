<template>
  <div class="login-part">
    <div class="login-main">
      <h1>学生关怀系统</h1>
      <div class="login-form">
        <div>
          <label>账号</label>
          <input type="text" name="username" v-model="username">
          <label>密码</label>
          <input type="password" name="password" v-model="password">
          <button type="submit" class="login-btn" @click="sub">登 录</button>
        </div>
      </div>
      <div class="register-tip">
        哈尔滨工业大学（威海）
        <!--                     <router-link to="/register">
                                 Create an account.
                            </router-link> -->
      </div>
    </div>
  </div>
</template>

<script>
  import {getPagePower, login} from '@/api/api'

  export default {
    data() {
      return {
        username: '',
        password: '',
      }
    },
    methods: {
      sub() {
        let data = {
          userId: this.username,
          password: this.password
        }
        login(data).then((res) => {
          if (res.status == 1) {
            this.$store.commit('setUserId', {"userid": this.username})
            this.$store.commit('setPagePower', res.data)
            this.$router.push({'path': '/home'})
            localStorage.userid = this.username
            localStorage.sessionid = res.session_id
          }
          else {
            this.$notify({
              title: '操作失败',
              message: res['errorInfo'],
              type: 'warning'
            })
          }
        })
      }
    },
    mounted() {
    }
  }
</script>

<style scoped>
  .login-part {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 100%;
    background-color: #F9F9F9;
    padding: 1px;
    box-sizing: border-box;
  }

  .login-main {
    width: 35%;
    height: 350px;
    margin: 160px auto;
    text-align: center;
  }

  .login-part h1 {
    font-size: 30px;
    font-weight: 300;
    letter-spacing: 2px;
  }

  .login-form {
    width: 320px;
    height: 290px;
    background-color: white;
    margin: 20px auto;
    border: 1px solid #d8dee2;
    border-radius: 5px;
    padding: 15px;
    text-align: left;
  }

  .login-form label {
    font-size: 16px;
    font-weight: 300;
  }

  .login-form input {
    width: 100%;
    height: 30px;
    display: block;
    border-radius: 3px;
    margin-top: 5px;
    margin-bottom: 15px;
    border: 1px solid #d8dee2;
    box-shadow: inset 0 1px 2px rgba(27, 31, 35, 0.075);
    font-size: 17px;
  }

  .login-form input:focus {
    border-color: #83C1F1;
  }

  .login-btn {
    width: 100%;
    height: 40px;
    margin-top: 25px;
    border-radius: 4px;
    border: none;
    background-color: #31C653;
    font-size: 16px;
    color: white;
    cursor: pointer;
  }

  .login-btn:hover {
    background-color: #28a846;
  }

  .forget-psd {
    color: #0366DC;
    font-size: 12px;
    margin-top: 12px;
    margin-left: 200px;
    cursor: pointer;
  }

  .register-tip {
    margin-top: 50px;
    font-weight: 300;
    font-size: 16px;
  }

  .register-tip a:link {
    color: #0366DC;
  }

  .register-tip a:hover {
    color: #0366DC;
  }

  .register-tip a:active {
    color: #0366DC;
  }

  .register-tip a:visited {
    color: #0366DC;
  }
</style>
