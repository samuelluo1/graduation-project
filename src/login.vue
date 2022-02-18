<template>
  <v-dialog
    v-model="dialogLoginVisible"
    persistent
    max-width="600px"
  >
    <v-card>
      <v-card-title class="justify-center">
        <span class="headline light-green--text">登入畫面</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="username"
                color="light-green"
                label="請輸入帳號"
                single-line
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="password"
                :type="false ? 'text' : 'password'"
                color="light-green"
                label="請輸入密碼"
                single-line
                required
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="dialogLoginVisible = false">取消</v-btn>
        <v-btn 
          color="light-green"
          dark
          @click="loginClick"
        >登入</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import Vue from 'vue'
export default {
  name: "login",
  data() {
    return {
      dialogLoginVisible: false,
      username: "",
      password: ""
    };
  },
  methods: {
    open() {
      this.dialogLoginVisible = true;
    },
    async loginClick() {
      //await this.$axios
        //.post("/api-token-auth/", {
          //username: this.username,
          //password: this.password
        //}).then(response => {
          //localStorage.setItem("user_token", response.data.token)
          //console.log(response.data.token)
        //})
      await this.$axios
        .post("/user/login/", {
          username: this.username,
          password: this.password
        }, {headers: {'X-CSRFToken': localStorage.getItem('user_token')}})
        .then(response => {
          console.log(response.data)
        })
      await this.$axios
        .post("/login/", {
          username: this.username,
          password: this.password,
          //headers: {'X-CSRFToken': localStorage.getItem('user_token')}
        })
        .then(response => {
          console.log(response.data)
          if (response.data == "passworderror") {
            this.$message.error("密码错误");
            return;
          }
          this.$cookies.set("user_token",response.data)
          this.$cookies.set("username", this.username)
          localStorage.setItem("user_token",response.data)
          localStorage.setItem("username", this.username)
          this.dialogLoginVisible = false
          this.$router.go(0)
          if(this.$store.state.loginip==""){
            this.$store.state.loginip = "chrome" // 后台会处理
          }
          if(this.$store.state.loginip==""){
            this.$store.state.loginip = "chrome" // 后台会处理
          }
          if(this.$store.state.loginip==undefined){
            this.$store.state.loginip = "chrome" // 后台会处理
          }
        })
        .catch(error => {
          console.log("用户名不存在（" + error + "）");
        });
    }
  }
};
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
}
</style>