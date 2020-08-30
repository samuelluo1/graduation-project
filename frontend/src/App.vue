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
              <v-list-item-title>編輯資料</v-list-item-title>
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
          <v-list-item to="/result" active-class="light-green--text" link>
            <v-list-item-icon>
              <v-icon>mdi-chart-bar</v-icon>
            </v-list-item-icon>
            <v-list-item-title>分析結果</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-app-bar
        app
        color="white"
        clipped-left
      >
        <v-app-bar-nav-icon @click.stop="drawer = !drawer" class="light-green--text"></v-app-bar-nav-icon>
        <span class="display-1 light-green--text">Lilicoco</span>
      </v-app-bar>
      <v-content>
      <v-container
        fluid
      >
        <v-card>
          <router-view id="route"></router-view>
        </v-card>
      </v-container>
    </v-content>
    </v-app>
  </div>
</template>
<script>

export default {
  name: 'App',
  data: () => ({
    drawer: null
  }),
  methods: {
  }
}
</script>

<style scoped>
  .content-wrapper {
    padding: 10px;
  }
</style>
