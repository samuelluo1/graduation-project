<template>
  <div id="app">
    <v-app>
      <v-navigation-drawer
      v-model="drawer"
      clipped
      app
      >
        <v-list dense>
          <v-list-item to="/homepage" active-class="light-green--text" link>
            <v-list-item-icon>
              <v-icon>mdi-home</v-icon>
            </v-list-item-icon>
            <v-list-item-title>首頁</v-list-item-title>
          </v-list-item>
          <v-list-group
            no-action
            value="true"
            prepend-icon="mdi-pencil"
            active-class="light-green--text"
          >
            <template v-slot:activator>
              <v-list-item-title>作業成本管理</v-list-item-title>
            </template>
            <v-list-item to="/misc" active-class="light-green--text" link>
              <v-list-item-title>人事雜項</v-list-item-title>
            </v-list-item>
            <v-list-item to="/item" active-class="light-green--text" link>
              <v-list-item-title>品項菜單</v-list-item-title>
            </v-list-item>
            <v-list-item to="/ingredient" active-class="light-green--text" link>
              <v-list-item-title>原物料</v-list-item-title>
            </v-list-item>
          </v-list-group>
          <v-list-group
            no-action
            value="true"
            prepend-icon="mdi-pencil"
            active-class="light-green--text"
          >
            <template v-slot:activator>
              <v-list-item-title>庫存管理</v-list-item-title>
            </template>
            <v-list-item to="/inventory" active-class="light-green--text" link>
              <v-list-item-title>管理頁面</v-list-item-title>
            </v-list-item>
          </v-list-group>
          <v-list-group
            no-action
            value="true"
            prepend-icon="mdi-pencil"
            active-class="light-green--text"
          >
            <template v-slot:activator>
              <v-list-item-title>員工管理</v-list-item-title>
            </template>
            <v-list-item to="/employee" active-class="light-green--text" link>
              <v-list-item-title>管理頁面</v-list-item-title>
            </v-list-item>
          </v-list-group>
          <v-list-group
            no-action
            value="true"
            prepend-icon="mdi-chart-bar"
            active-class="light-green--text"
          >
            <template v-slot:activator>
              <v-list-item-title>分析結果</v-list-item-title>
            </template>
            <v-list-item to="/coordinate" active-class="light-green--text" link>
              <v-list-item-title>abc座標圖</v-list-item-title>
            </v-list-item>
            <v-list-item to="/turnover" active-class="light-green--text" link>
              <v-list-item-title>每月淨利變化圖</v-list-item-title>
            </v-list-item>
            <v-list-item to="/cost" active-class="light-green--text" link>
              <v-list-item-title>每月成本變化圖</v-list-item-title>
            </v-list-item>
            <v-list-item to="/ingredientCost" active-class="light-green--text" link>
              <v-list-item-title>每月各原物料成本變化圖</v-list-item-title>
            </v-list-item>
          </v-list-group>
        </v-list>
      </v-navigation-drawer>
      <v-app-bar
        app
        color="white"
        clipped-left
      >
        <v-app-bar-nav-icon @click.stop="drawer = !drawer" class="light-green--text"></v-app-bar-nav-icon>
        <img :src="imgUrl" height="30px" />
        <v-spacer></v-spacer>
        <v-btn
          color="light-green"
          dark
          @click="loginopen"
          v-show="!loginshow"
        >
          登入
        </v-btn>
        <v-btn
          color="light-green"
          dark
          @click="logout"
          v-show="loginshow"
        >
          登出
        </v-btn>
      </v-app-bar>
      <v-content>
      <v-container
        fluid
      >
        <v-card>
          <router-view id="route" v-if="isRouterAlive"></router-view>
        </v-card>
      </v-container>
    </v-content>
    <login ref="logindialog"></login>
    </v-app>
  </div>
</template>
<script>

export default {
  name: 'App',
  provide () {
    return {
      reload: this.reload
    }
  },
  components: {
    'login': resolve => require(['@/login'], resolve)
  },
  data: () => ({
    drawer: null,
    isRouterAlive: true,
    loginshow: localStorage.username,
    username: localStorage.username,
    imgUrl: 'static/lilicoco.jpg'
  }),
  methods: {
    reload () {
      this.isRouterAlive = false
      this.$nextTick(function () {
        this.isRouterAlive = true
      })
    },
    loginopen () {
      this.$refs.logindialog.open()
    },
    logout () {
      localStorage.setItem('username', '')
      localStorage.setItem('user_token', '')
      this.$router.go(0)
    }
  }
}
</script>

<style scoped>
  .content-wrapper {
    padding: 10px;
  }
</style>
